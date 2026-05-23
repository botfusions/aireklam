"""
GSC → NocoDB Agentic Pipeline
==============================
Google Search Console verilerini çekip NocoDB'ye aktarır.
Botfusions ve müşteri projeleri için ortak kullanım.

Kullanım:
    python gsc_nocodb_pipeline.py --client botfusions --days 30
    python gsc_nocodb_pipeline.py --client horecamark --days 7 --report

Env değişkenleri (.env):
    GSC_CREDENTIALS_PATH   → Service account JSON yolu
    NOCODB_BASE_URL        → NocoDB URL (ör: http://localhost:8080)
    NOCODB_API_TOKEN       → NocoDB API token
"""

import os
import sys
import json
import requests
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

# Mevcut modülü import et
sys.path.insert(0, str(Path(__file__).parent.parent / "04-araclar" / "seo-machine-modules" / "modules"))
from google_search_console import GoogleSearchConsole


# ─────────────────────────────────────────────
# NocoDB Client
# ─────────────────────────────────────────────

class NocoDBClient:
    """NocoDB REST API wrapper"""

    def __init__(self, base_url: str = None, api_token: str = None):
        self.base_url = (base_url or os.getenv("NOCODB_BASE_URL", "https://nocodb.turklawai.com")).rstrip("/")
        self.token = api_token or os.getenv("NOCODB_API_TOKEN")
        if not self.token:
            raise ValueError("NOCODB_API_TOKEN bulunamadı. .env dosyasını kontrol et.")
        self.headers = {
            "xc-token": self.token,
            "Content-Type": "application/json"
        }

    def list_tables(self, base_id: str) -> List[Dict]:
        """Base içindeki tabloları listele"""
        r = requests.get(f"{self.base_url}/api/v1/db/meta/projects/{base_id}/tables", headers=self.headers)
        r.raise_for_status()
        return r.json().get("list", [])

    def get_table_id(self, base_id: str, table_name: str) -> Optional[str]:
        """Tablo adına göre ID döndür"""
        tables = self.list_tables(base_id)
        for t in tables:
            if t["title"] == table_name:
                return t["id"]
        return None

    def create_table(self, base_id: str, table_name: str, columns: List[Dict]) -> str:
        """Yeni tablo oluştur, ID döndür"""
        payload = {"title": table_name, "columns": columns}
        r = requests.post(
            f"{self.base_url}/api/v1/db/meta/projects/{base_id}/tables",
            headers=self.headers,
            json=payload
        )
        r.raise_for_status()
        return r.json()["id"]

    def upsert_rows(self, base_id: str, table_id: str, rows: List[Dict]) -> Dict:
        """
        Satır ekle — önce bulk dener, olmazsa tek tek insert yapar.
        """
        if not rows:
            return {"inserted": 0}

        # Önce bulk dene
        try:
            r = requests.post(
                f"{self.base_url}/api/v1/db/data/noco/{base_id}/{table_id}/bulk",
                headers=self.headers,
                json=rows,
                timeout=30
            )
            if r.status_code == 200:
                return {"inserted": len(rows)}
        except Exception:
            pass

        # Bulk olmadı, tek tek insert
        total_inserted = 0
        for row in rows:
            r = requests.post(
                f"{self.base_url}/api/v1/db/data/noco/{base_id}/{table_id}",
                headers=self.headers,
                json=row,
                timeout=15
            )
            r.raise_for_status()
            total_inserted += 1
        return {"inserted": total_inserted}

    def insert_rows(self, base_id: str, table_name: str, rows: List[Dict]) -> Dict:
        """Tablo adıyla satır ekle (table_id lookup yapar)"""
        table_id = self.get_table_id(base_id, table_name)
        if not table_id:
            raise ValueError(f"Tablo bulunamadı: {table_name}")
        return self.upsert_rows(base_id, table_id, rows)

    def list_bases(self) -> List[Dict]:
        """Tüm base'leri listele"""
        r = requests.get(f"{self.base_url}/api/v1/db/meta/projects/", headers=self.headers)
        r.raise_for_status()
        return r.json().get("list", [])

    def get_base_id(self, base_name: str) -> Optional[str]:
        """Base adına göre ID döndür"""
        bases = self.list_bases()
        for b in bases:
            if b["title"] == base_name:
                return b["id"]
        return None


# ─────────────────────────────────────────────
# Tablo Şemaları
# ─────────────────────────────────────────────

SCHEMAS = {

    "gsc_keywords": [
        {"title": "client",         "uidt": "SingleLineText"},
        {"title": "date_fetched",   "uidt": "Date"},
        {"title": "period_days",    "uidt": "Number"},
        {"title": "keyword",        "uidt": "SingleLineText"},
        {"title": "clicks",         "uidt": "Number"},
        {"title": "impressions",    "uidt": "Number"},
        {"title": "ctr",            "uidt": "Decimal"},
        {"title": "position",       "uidt": "Decimal"},
        {"title": "intent",         "uidt": "SingleLineText"},
        {"title": "opportunity_score", "uidt": "Decimal"},
        {"title": "priority",       "uidt": "SingleLineText"},
    ],

    "gsc_pages": [
        {"title": "client",         "uidt": "SingleLineText"},
        {"title": "date_fetched",   "uidt": "Date"},
        {"title": "period_days",    "uidt": "Number"},
        {"title": "url",            "uidt": "URL"},
        {"title": "clicks",         "uidt": "Number"},
        {"title": "impressions",    "uidt": "Number"},
        {"title": "ctr",            "uidt": "Decimal"},
        {"title": "avg_position",   "uidt": "Decimal"},
        {"title": "missed_clicks",  "uidt": "Number"},
        {"title": "priority",       "uidt": "SingleLineText"},
    ],

    "gsc_trends": [
        {"title": "client",             "uidt": "SingleLineText"},
        {"title": "date_fetched",       "uidt": "Date"},
        {"title": "query",              "uidt": "SingleLineText"},
        {"title": "recent_impressions", "uidt": "Number"},
        {"title": "prev_impressions",   "uidt": "Number"},
        {"title": "change_pct",         "uidt": "Decimal"},
        {"title": "clicks",             "uidt": "Number"},
        {"title": "position",           "uidt": "Decimal"},
    ],

    "gsc_summary": [
        {"title": "client",         "uidt": "SingleLineText"},
        {"title": "date_fetched",   "uidt": "Date"},
        {"title": "period_days",    "uidt": "Number"},
        {"title": "total_clicks",   "uidt": "Number"},
        {"title": "total_impressions", "uidt": "Number"},
        {"title": "avg_ctr",        "uidt": "Decimal"},
        {"title": "avg_position",   "uidt": "Decimal"},
        {"title": "quick_wins",     "uidt": "Number"},
        {"title": "low_ctr_pages",  "uidt": "Number"},
        {"title": "trending_queries", "uidt": "Number"},
        {"title": "notes",          "uidt": "LongText"},
    ],
}


# ─────────────────────────────────────────────
# Pipeline
# ─────────────────────────────────────────────

class GSCNocoPipeline:
    """
    GSC verilerini çekip NocoDB'ye aktaran ana pipeline.

    Her müşteri için:
      - client_id      : slug (ör: botfusions, horecamark)
      - site_url       : GSC'deki site URL
      - nocodb_base    : NocoDB base adı (ör: "Botfusions SEO")
      - credentials    : Service account JSON yolu
    """

    def __init__(self, client_config: Dict):
        self.client_id = client_config["client_id"]
        self.site_url  = client_config["site_url"]
        self.days      = client_config.get("days", 30)
        self.creds     = client_config.get("credentials_path") or os.getenv("GSC_CREDENTIALS_PATH")
        self.nocodb_base = client_config.get("nocodb_base", "GSC Analytics")

        # Lazy init
        self._gsc  = None
        self._noco = None

    @property
    def gsc(self):
        if not self._gsc:
            self._gsc = GoogleSearchConsole(
                site_url=self.site_url,
                credentials_path=self.creds
            )
        return self._gsc

    @property
    def noco(self):
        if not self._noco:
            self._noco = NocoDBClient()
        return self._noco

    def _get_or_create_base(self) -> str:
        """NocoDB base ID'yi al, yoksa hata ver"""
        base_id = self.noco.get_base_id(self.nocodb_base)
        if not base_id:
            raise ValueError(
                f"NocoDB base '{self.nocodb_base}' bulunamadı. "
                "Önce NocoDB'de bu base'i oluştur."
            )
        return base_id

    def ensure_tables(self, base_id: str):
        """Gerekli tabloları yoksa oluştur"""
        existing = {t["title"] for t in self.noco.list_tables(base_id)}
        for table_name, columns in SCHEMAS.items():
            if table_name not in existing:
                self.noco.create_table(base_id, table_name, columns)
                print(f"  ✓ Tablo oluşturuldu: {table_name}")
            else:
                print(f"  · Tablo mevcut: {table_name}")

    # ── Veri çekme & dönüştürme ──────────────────────────────

    def fetch_keywords(self) -> List[Dict]:
        today = datetime.now().strftime("%Y-%m-%d")
        rows = []
        # Quick wins (pozisyon 11-20)
        for kw in self.gsc.get_quick_wins(days=self.days):
            rows.append({
                "client": self.client_id,
                "date_fetched": today,
                "period_days": self.days,
                "keyword": kw["keyword"],
                "clicks": kw["clicks"],
                "impressions": kw["impressions"],
                "ctr": round(kw["ctr"] * 100, 2),
                "position": kw["position"],
                "intent": kw.get("commercial_intent_category", ""),
                "opportunity_score": kw.get("opportunity_score", 0),
                "priority": kw.get("priority", ""),
            })
        # Tüm keyword'ler (top 500)
        all_kw = self.gsc.get_keyword_positions(days=self.days, limit=500)
        quick_win_set = {r["keyword"] for r in rows}
        for kw in all_kw:
            if kw["keyword"] not in quick_win_set:
                rows.append({
                    "client": self.client_id,
                    "date_fetched": today,
                    "period_days": self.days,
                    "keyword": kw["keyword"],
                    "clicks": kw["clicks"],
                    "impressions": kw["impressions"],
                    "ctr": round(kw["ctr"] * 100, 2),
                    "position": kw["position"],
                    "intent": "",
                    "opportunity_score": 0,
                    "priority": "",
                })
        return rows

    def fetch_pages(self) -> List[Dict]:
        today = datetime.now().strftime("%Y-%m-%d")
        rows = []
        for page in self.gsc.get_low_ctr_pages(days=self.days, path_filter=None):
            rows.append({
                "client": self.client_id,
                "date_fetched": today,
                "period_days": self.days,
                "url": page["url"],
                "clicks": page["clicks"],
                "impressions": page["impressions"],
                "ctr": page["ctr"],
                "avg_position": page["avg_position"],
                "missed_clicks": page.get("missed_clicks", 0),
                "priority": page.get("priority", ""),
            })
        return rows

    def fetch_trends(self) -> List[Dict]:
        today = datetime.now().strftime("%Y-%m-%d")
        rows = []
        for t in self.gsc.get_trending_queries(days_recent=7, days_comparison=self.days):
            rows.append({
                "client": self.client_id,
                "date_fetched": today,
                "query": t["query"],
                "recent_impressions": t["recent_impressions"],
                "prev_impressions": t["previous_impressions"],
                "change_pct": t["change_percent"],
                "clicks": t["clicks"],
                "position": t["position"],
            })
        return rows

    def build_summary(self, keywords: List, pages: List, trends: List) -> Dict:
        today = datetime.now().strftime("%Y-%m-%d")
        total_clicks = sum(k["clicks"] for k in keywords)
        total_impressions = sum(k["impressions"] for k in keywords)
        avg_ctr = round(total_clicks / total_impressions * 100, 2) if total_impressions else 0
        avg_pos = round(sum(k["position"] for k in keywords) / len(keywords), 1) if keywords else 0
        quick_wins = sum(1 for k in keywords if k.get("priority"))
        return {
            "client": self.client_id,
            "date_fetched": today,
            "period_days": self.days,
            "total_clicks": total_clicks,
            "total_impressions": total_impressions,
            "avg_ctr": avg_ctr,
            "avg_position": avg_pos,
            "quick_wins": quick_wins,
            "low_ctr_pages": len(pages),
            "trending_queries": len(trends),
            "notes": f"Otomatik çekildi: {today} | {len(keywords)} keyword, {len(pages)} sayfa, {len(trends)} trend",
        }

    # ── Ana çalıştırma ────────────────────────────────────────

    def run(self, report: bool = False) -> Dict:
        print(f"\n{'─'*50}")
        print(f"Client: {self.client_id} | Site: {self.site_url} | {self.days} gün")
        print(f"{'─'*50}")

        base_id = self._get_or_create_base()
        print(f"\n[1/5] Tablolar kontrol ediliyor...")
        self.ensure_tables(base_id)

        print(f"\n[2/5] GSC → Keyword verileri çekiliyor...")
        keywords = self.fetch_keywords()
        print(f"  → {len(keywords)} keyword")

        print(f"\n[3/5] GSC → Sayfa (düşük CTR) verileri çekiliyor...")
        pages = self.fetch_pages()
        print(f"  → {len(pages)} sayfa")

        print(f"\n[4/5] GSC → Trend sorguları çekiliyor...")
        trends = self.fetch_trends()
        print(f"  → {len(trends)} trend")

        print(f"\n[5/5] NocoDB'ye aktarılıyor...")
        if keywords:
            self.noco.insert_rows(base_id, "gsc_keywords", keywords)
            print(f"  ✓ gsc_keywords: {len(keywords)} satır")
        if pages:
            self.noco.insert_rows(base_id, "gsc_pages", pages)
            print(f"  ✓ gsc_pages: {len(pages)} satır")
        if trends:
            self.noco.insert_rows(base_id, "gsc_trends", trends)
            print(f"  ✓ gsc_trends: {len(trends)} satır")

        summary = self.build_summary(keywords, pages, trends)
        self.noco.insert_rows(base_id, "gsc_summary", [summary])
        print(f"  ✓ gsc_summary: 1 satır")

        print(f"\n✅ Pipeline tamamlandı: {self.client_id}")

        if report:
            self._print_report(summary, keywords, pages, trends)

        return summary

    def _print_report(self, summary, keywords, pages, trends):
        print(f"\n{'═'*50}")
        print(f"📊 RAPOR: {self.client_id.upper()} — {summary['date_fetched']}")
        print(f"{'═'*50}")
        print(f"  Toplam Tıklama  : {summary['total_clicks']:,}")
        print(f"  Toplam Görüntüleme: {summary['total_impressions']:,}")
        print(f"  Ortalama CTR    : %{summary['avg_ctr']}")
        print(f"  Ortalama Pozisyon: {summary['avg_position']}")
        print(f"  Quick Win Fırsatı: {summary['quick_wins']}")
        print(f"  Düşük CTR Sayfası: {summary['low_ctr_pages']}")
        print(f"  Trend Sorgu     : {summary['trending_queries']}")

        if keywords:
            print(f"\n🔑 TOP 5 QUICK WIN:")
            for kw in sorted(keywords, key=lambda x: x.get("opportunity_score", 0), reverse=True)[:5]:
                if kw.get("priority"):
                    print(f"  - {kw['keyword']} | Pozisyon: {kw['position']} | Skor: {kw['opportunity_score']}")

        if trends:
            print(f"\n📈 TOP 5 TREND:")
            for t in sorted(trends, key=lambda x: x["change_pct"], reverse=True)[:5]:
                print(f"  - {t['query']} | +%{t['change_pct']} artış")

        print(f"{'═'*50}\n")


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

# Müşteri profilleri — buraya yeni müşteri ekle
CLIENT_PROFILES = {
    "botfusions": {
        "client_id": "botfusions",
        "site_url": "sc-domain:botfusions.com",
        "nocodb_base": "Botfusions SEO",
    },
    "horecamark": {
        "client_id": "horecamark",
        "site_url": "https://horecamark.com",  # gerçek URL ile güncelle
        "nocodb_base": "HorecaMark SEO",
    },
}


def main():
    parser = argparse.ArgumentParser(description="GSC → NocoDB Pipeline")
    parser.add_argument("--client",  required=True, help="Client ID (ör: botfusions)")
    parser.add_argument("--days",    type=int, default=30, help="Kaç günlük veri (varsayılan: 30)")
    parser.add_argument("--report",  action="store_true", help="Konsola rapor yazdır")
    parser.add_argument("--creds",   help="Service account JSON yolu (opsiyonel)")
    args = parser.parse_args()

    if args.client not in CLIENT_PROFILES:
        print(f"❌ Bilinmeyen client: {args.client}")
        print(f"   Mevcut: {', '.join(CLIENT_PROFILES.keys())}")
        sys.exit(1)

    config = CLIENT_PROFILES[args.client].copy()
    config["days"] = args.days
    if args.creds:
        config["credentials_path"] = args.creds

    # .env yükle
    try:
        from dotenv import load_dotenv
        env_path = Path(__file__).parent / ".env"
        load_dotenv(env_path)
    except ImportError:
        pass

    pipeline = GSCNocoPipeline(config)
    pipeline.run(report=args.report)


if __name__ == "__main__":
    main()
