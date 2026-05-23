"""
GSC Agentic Workflow Orchestrator
==================================
Claude Code / Cowork üzerinden çağrılabilir otonom ajan.
GSC verileri çeker, analiz eder, anomali tespit eder,
NocoDB'ye kaydeder ve özet üretir.

Kullanım (tek seferlik):
    python agent.py --client botfusions
    python agent.py --all                  # tüm müşteriler
    python agent.py --client horecamark --alert-threshold 20

Zamanlı çalıştırma (cron örneği):
    0 8 * * * cd /path/to/05-gsc-nocodb && python agent.py --all
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

from gsc_nocodb_pipeline import GSCNocoPipeline, CLIENT_PROFILES


# ─────────────────────────────────────────────
# Anomali Tespiti
# ─────────────────────────────────────────────

class AnomalyDetector:
    """Basit kural tabanlı anomali tespiti"""

    def __init__(self, threshold_pct: float = 20.0):
        self.threshold = threshold_pct

    def detect(self, summary: Dict, prev_summary: Dict = None) -> List[Dict]:
        anomalies = []

        if not prev_summary:
            return anomalies

        checks = [
            ("total_clicks",      "Tıklama",      "düşüş",  "artış"),
            ("total_impressions", "Görüntüleme",  "düşüş",  "artış"),
            ("avg_ctr",           "CTR",           "düşüş",  "artış"),
            ("avg_position",      "Ortalama Pozisyon", "artış", "düşüş"),  # pozisyon için ters
        ]

        for field, label, bad_word, good_word in checks:
            curr = summary.get(field, 0)
            prev = prev_summary.get(field, 0)
            if prev == 0:
                continue

            change_pct = ((curr - prev) / prev) * 100

            # Pozisyon için kötü = artış (sayı büyürse kötü)
            is_bad = change_pct <= -self.threshold if field != "avg_position" else change_pct >= self.threshold
            is_good = change_pct >= self.threshold if field != "avg_position" else change_pct <= -self.threshold

            if is_bad or is_good:
                anomalies.append({
                    "field": field,
                    "label": label,
                    "current": curr,
                    "previous": prev,
                    "change_pct": round(change_pct, 1),
                    "severity": "🔴 ALARM" if is_bad else "🟢 İYİ",
                    "message": f"{label}: {prev} → {curr} ({change_pct:+.1f}%)"
                })

        return anomalies


# ─────────────────────────────────────────────
# Rapor Üretici
# ─────────────────────────────────────────────

def generate_report(client_id: str, summary: Dict, anomalies: List[Dict]) -> str:
    lines = []
    lines.append(f"{'═'*55}")
    lines.append(f"📊 GSC RAPORU: {client_id.upper()}")
    lines.append(f"   Tarih: {summary['date_fetched']} | Dönem: Son {summary['period_days']} gün")
    lines.append(f"{'═'*55}")
    lines.append(f"  Toplam Tıklama    : {summary['total_clicks']:,}")
    lines.append(f"  Toplam Görüntüleme: {summary['total_impressions']:,}")
    lines.append(f"  Ortalama CTR      : %{summary['avg_ctr']}")
    lines.append(f"  Ortalama Pozisyon : {summary['avg_position']}")
    lines.append(f"  Quick Win Fırsatı : {summary['quick_wins']}")
    lines.append(f"  Düşük CTR Sayfası : {summary['low_ctr_pages']}")
    lines.append(f"  Trend Sorgu       : {summary['trending_queries']}")

    if anomalies:
        lines.append(f"\n⚠️  ANOMALİLER ({len(anomalies)}):")
        for a in anomalies:
            lines.append(f"  {a['severity']} {a['message']}")
    else:
        lines.append(f"\n✅ Anomali tespit edilmedi.")

    lines.append(f"{'═'*55}")
    return "\n".join(lines)


def save_report(client_id: str, report_text: str):
    """Raporu logs/ klasörüne kaydet"""
    logs_dir = Path(__file__).parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    path = logs_dir / f"{client_id}_{date_str}.txt"
    path.write_text(report_text, encoding="utf-8")
    return str(path)


# ─────────────────────────────────────────────
# Ajan
# ─────────────────────────────────────────────

class GSCAgent:
    """
    Otonom GSC analiz ajanı.

    Adımlar:
    1. Pipeline çalıştır → NocoDB'ye aktar
    2. Anomali tespit et
    3. Rapor üret → logs/ klasörüne kaydet
    4. (Opsiyonel) Gmail bildirimi gönder
    """

    def __init__(self, alert_threshold: float = 20.0):
        self.detector = AnomalyDetector(threshold_pct=alert_threshold)

    def run_client(self, client_id: str, days: int = 30) -> Dict:
        """Tek bir müşteri için pipeline çalıştır"""
        print(f"\n🤖 AJAN: {client_id}")

        if client_id not in CLIENT_PROFILES:
            return {"error": f"Bilinmeyen client: {client_id}"}

        config = CLIENT_PROFILES[client_id].copy()
        config["days"] = days

        # Pipeline çalıştır
        pipeline = GSCNocoPipeline(config)
        summary = pipeline.run(report=False)

        # Anomali tespiti (önceki özet olmadan basit analiz)
        anomalies = self.detector.detect(summary)

        # Rapor üret
        report_text = generate_report(client_id, summary, anomalies)
        report_path = save_report(client_id, report_text)

        print(report_text)
        print(f"\n📁 Rapor kaydedildi: {report_path}")

        return {
            "client": client_id,
            "summary": summary,
            "anomalies": anomalies,
            "report_path": report_path,
        }

    def run_all(self, days: int = 30) -> List[Dict]:
        """Tüm müşteriler için çalıştır"""
        results = []
        for client_id in CLIENT_PROFILES.keys():
            try:
                result = self.run_client(client_id, days=days)
                results.append(result)
            except Exception as e:
                print(f"❌ {client_id} hatası: {e}")
                results.append({"client": client_id, "error": str(e)})
        return results


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="GSC Agentic Workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  python agent.py --client botfusions
  python agent.py --client horecamark --days 7
  python agent.py --all --days 30 --alert-threshold 15
        """
    )
    parser.add_argument("--client",           help="Tek müşteri ID (ör: botfusions)")
    parser.add_argument("--all",              action="store_true", help="Tüm müşteriler")
    parser.add_argument("--days",             type=int, default=30, help="Analiz dönemi (gün)")
    parser.add_argument("--alert-threshold",  type=float, default=20.0, help="Anomali eşiği %%")
    args = parser.parse_args()

    if not args.client and not args.all:
        parser.print_help()
        sys.exit(1)

    agent = GSCAgent(alert_threshold=args.alert_threshold)

    if args.all:
        agent.run_all(days=args.days)
    else:
        agent.run_client(args.client, days=args.days)


if __name__ == "__main__":
    main()
