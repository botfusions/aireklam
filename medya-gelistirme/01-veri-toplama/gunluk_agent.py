"""
Gunluk Veri Toplama Agenti — Medya Gelistirme Pipeline Faz 3
============================================================
Kullanim: python gunluk_agent.py [--skip-ads] [--skip-trend]
Flask API'den Google Ads verisini ceker, hafiza/ altina gunluk rapor yazar.
"""
import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path

try:
    import requests as req_lib
except ImportError:
    sys.exit("requests gerekli: pip install requests")

ROOT = Path(__file__).resolve().parent.parent.parent
API = "http://localhost:8765"
HAZIFA_DIR = ROOT / "hafiza"

# ── Klasor sabitleri ────────────────────────────────────────
RAKIP_DIR = HAZIFA_DIR / "rakip-arsivi"
TREND_DIR = HAZIFA_DIR / "trend-log"
PERF_DIR = HAZIFA_DIR / "performans-tarihi"
ICERIK_DIR = HAZIFA_DIR / "icerik-arsivi"

# ── Supabase sosyal post verisi ─────────────────────────────
OMNI_ACCOUNTS = ["881407_instagram", "881407_facebook", "881407_x",
                 "881407_tiktok", "881407_pinterest", "881407_youtube"]


def ensure_dirs():
    """Gerekli klasorleri olustur."""
    for d in [RAKIP_DIR, TREND_DIR, PERF_DIR, ICERIK_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def fetch_ads_summary() -> dict:
    """Flask API'den Google Ads ozetini cek."""
    try:
        r = req_lib.get(f"{API}/api/google-ads/summary", timeout=30)
        r.raise_for_status()
        return r.json()
    except req_lib.ConnectionError:
        return {"error": "Flask API calismiyor. Once: python gsc_api_server.py"}
    except Exception as e:
        return {"error": str(e)}


def fetch_omni_posts() -> list:
    """OmniSocials uzerinden son yayinlanan postlari cek."""
    try:
        r = req_lib.get(f"{API}/api/omni/posts", timeout=15)
        r.raise_for_status()
        data = r.json()
        return data.get("posts", data.get("data", []))
    except Exception:
        return []


def fetch_pipeline_stats() -> dict:
    """Pipeline istatistiklerini cek."""
    try:
        r = req_lib.get(f"{API}/api/pipeline/stats", timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return {}


def write_ads_performance(ads_data: dict) -> Path:
    """Google Ads performans raporu yaz."""
    today = date.today().isoformat()
    path = PERF_DIR / f"{today}-ads-performans.md"

    lines = [
        f"# Google Ads Performans — {today}",
        "",
        f"Tarih: {today}",
        "",
    ]

    if "error" in ads_data:
        lines.append(f"**Hata:** {ads_data['error']}")
    else:
        summary = ads_data.get("summary", ads_data)
        if isinstance(summary, dict):
            lines.append("## Ozet")
            for key, val in summary.items():
                lines.append(f"- **{key}:** {val}")
            lines.append("")

        campaigns = ads_data.get("campaigns", [])
        if campaigns:
            lines.append("## Kampanya Detaylari")
            lines.append("")
            lines.append("| Kampanya | Harcama | Tiklama | Gosterim | CTR |")
            lines.append("|----------|---------|---------|----------|-----|")
            for c in campaigns[:10]:
                name = c.get("campaign_name", c.get("name", "N/A"))
                cost = c.get("cost", c.get("spend", "N/A"))
                clicks = c.get("clicks", "N/A")
                imps = c.get("impressions", "N/A")
                ctr = c.get("ctr", "N/A")
                lines.append(f"| {name} | {cost} | {clicks} | {imps} | {ctr} |")

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_trend_snapshot(trends: list, omni_posts: list) -> Path:
    """Trend ve sosyal medya snapshot'i yaz."""
    today = date.today().isoformat()
    path = TREND_DIR / f"{today}-trend.md"

    lines = [
        f"# Trend Snapshot — {today}",
        "",
        f"Tarih: {today}",
        "",
        "## Sosyal Medya Son Postlar",
        "",
    ]

    if omni_posts:
        for p in omni_posts[:15]:
            platform = p.get("platform", p.get("account_id", "N/A"))
            caption = str(p.get("caption", p.get("text", "")))[:80]
            status = p.get("status", "N/A")
            lines.append(f"- **{platform}:** {caption}... ({status})")
    else:
        lines.append("- Veri alinamadi — OmniSocials API'yi kontrol et")

    lines.append("")

    if trends:
        lines.append("## Tespit Edilen Trendler")
        for t in trends:
            lines.append(f"- {t}")

    lines.append("")
    lines.append("---")
    lines.append(f"*Otomatik uretim: gunluk_agent.py — {today}*")

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def fetch_competitor_snapshot() -> dict:
    """Rakip sosyal medya aktivitesini analiz et.

    OmniSocials hesaplarindan botfusions postlarini ceker,
    rakip listesine gore karsilastirmali snapshot olusturur.
    """
    # ── Botfusions son postlar (karsilastirma icin) ──
    our_posts = fetch_omni_posts()
    our_count = len(our_posts)

    # ── Rakip listesi (hafiza/rakip-arsivi/rakip-listesi.md'den) ──
    COMPETITORS = {
        "geo": [
            {"name": "Lein Digital", "handle": "leindigital", "platform": "instagram",
             "threat": "YUKSEK", "notes": "Türkiye'nin ilk GEO ajansi iddia, 100+ marka"},
            {"name": "ROIPUBLIC", "handle": "roipublic", "platform": "linkedin",
             "threat": "ORTA-YUKSEK", "notes": "GEO + yapay zeka ajansi iddialari, aktif icerik"},
            {"name": "Seobaz", "handle": "seobaz", "platform": "linkedin",
             "threat": "ORTA", "notes": "AI Visibility hizmeti ekledi"},
            {"name": "Dijitanya / Kursad Sualp", "handle": "kursadsualp", "platform": "youtube",
             "threat": "ORTA", "notes": "SEO Sohbetleri, pazar egitimi"},
            {"name": "Webtures", "handle": "webtures", "platform": "linkedin",
             "threat": "DUSUK", "notes": "Geleneksel SEO, GEO'ya yeni girdi"},
        ],
        "seo_arac": [
            {"name": "Semust", "handle": "semust", "platform": "web",
             "threat": "ORTA", "notes": "4000+ marka, keyword tracking + audit, AI onerileri, GEO'ya kayabilir"},
            {"name": "Seobaz (arac)", "handle": "seobaz", "platform": "web",
             "threat": "ORTA", "notes": "Hem danismanlik hem arac platformu"},
        ],
        "chatbot": [
            {"name": "Gurizon", "handle": "gurizon", "platform": "web",
             "threat": "ORTA", "notes": "WhatsApp + Instagram + Web bot"},
            {"name": "Chatbotto", "handle": "chatbotto", "platform": "web",
             "threat": "ORTA", "notes": "Otomatik mesaj + randevu sistemi"},
            {"name": "Palmate AI", "handle": "palmateai", "platform": "linkedin",
             "threat": "ORTA", "notes": "Kurumsal chatbot platformu"},
            {"name": "Etkin.ai", "handle": "etkinai", "platform": "web",
             "threat": "ORTA", "notes": "E-ticaret satis otomasyonu"},
            {"name": "Supsis", "handle": "supsis", "platform": "web",
             "threat": "DUSUK", "notes": "Sosyal medya yonetim + bot combo"},
        ],
        "agentic": [
            {"name": "Lighthouse Group", "handle": "lighthousegroupnet", "platform": "linkedin",
             "threat": "YUKSEK", "notes": "AI Ajan + GEO + MCP + n8n, tam rakip"},
        ],
    }

    return {
        "our_post_count": our_count,
        "competitors": COMPETITORS,
        "date": date.today().isoformat(),
    }


def write_competitor_snapshot(comp_data: dict) -> Path:
    """Rakip analiz snapshot'i yaz."""
    today = date.today().isoformat()
    path = RAKIP_DIR / f"{today}-rakip-snapshot.md"

    lines = [
        f"# Rakip Analiz Snapshot — {today}",
        "",
        f"Tarih: {today}",
        f"Botfusions son post sayisi: {comp_data.get('our_post_count', 0)}",
        "",
    ]

    for niche, comps in comp_data.get("competitors", {}).items():
        lines.append(f"## {niche.upper()} Rakipleri")
        lines.append("")
        lines.append("| Rakip | Platform | Tehdit | Not |")
        lines.append("|-------|----------|--------|-----|")
        for c in comps:
            lines.append(f"| {c['name']} | {c['platform']} | {c['threat']} | {c['notes']} |")
        lines.append("")

    lines.append("## Yapilacaklar")
    lines.append("- [ ] Rakip hesaplarini Instagram/LinkedIn'de kontrol et")
    lines.append("- [ ] Yeni rakip kesfedildi ise rakip-listesi.md'ye ekle")
    lines.append("- [ ] Rakip icerik formatlarini not al (reel mi, carousel mi, post mu)")
    lines.append("")
    lines.append("---")
    lines.append(f"*Otomatik uretim: gunluk_agent.py — {today}*")

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_daily_summary(ads_path: Path, trend_path: Path,
                        pipeline_stats: dict, ads_data: dict) -> Path:
    """Gunluk ozet raporu yaz."""
    today = date.today().isoformat()
    path = HAZIFA_DIR / f"{today}-gunluk-ozet.md"

    lines = [
        f"# Gunluk Ozet — {today}",
        "",
        f"Tarih: {today}",
        f"Olusturulma: {datetime.now().strftime('%H:%M')}",
        "",
        "## Google Ads",
        "",
    ]

    if "error" in ads_data:
        lines.append(f"- **Durum:** Hata — {ads_data['error']}")
    else:
        lines.append(f"- **Rapor:** [{ads_path.name}](../performans-tarihi/{ads_path.name})")

    lines.append("")
    lines.append("## Sosyal Medya")
    lines.append(f"- **Trend raporu:** [{trend_path.name}](../trend-log/{trend_path.name})")

    if pipeline_stats:
        stats = pipeline_stats.get("stats", pipeline_stats)
        lines.append("")
        lines.append("## Pipeline Durumu")
        if isinstance(stats, dict):
            for key, val in stats.items():
                lines.append(f"- **{key}:** {val}")

    lines.append("")
    lines.append("## Icerik Firsatlari")
    lines.append("")
    lines.append("- [ ] Strateji modulu calistir: `python strateji_olustur.py --send`")
    lines.append("- [ ] Onay bekleyen paketleri kontrol et: CMO Dashboard > Pipeline")
    lines.append("- [ ] Rakip snapshot: [rakip-arsivi/](../rakip-arsivi/) — yeni aktivite kontrol et")
    lines.append("")

    # Uyari kurallari
    lines.append("## Uyarilar")
    ads_summary = ads_data.get("summary", {})
    if isinstance(ads_summary, dict):
        spend_today = ads_summary.get("spend", ads_summary.get("cost", 0))
        if spend_today and isinstance(spend_today, (int, float)) and spend_today > 0:
            lines.append(f"- Harcama bugun: {spend_today}")

    lines.append("")
    lines.append("---")
    lines.append(f"*Otomatik uretim: gunluk_agent.py — {today}*")

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def append_to_log(message: str):
    """hafiza/log.md'ye append."""
    log_path = HAZIFA_DIR / "log.md"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"{timestamp} | gunluk-agent | {message}\n"

    if log_path.exists():
        existing = log_path.read_text(encoding="utf-8")
        log_path.write_text(existing + entry, encoding="utf-8")
    else:
        log_path.write_text(entry, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Botfusions Gunluk Veri Toplama Agenti")
    parser.add_argument("--skip-ads", action="store_true", help="Google Ads verisini atla")
    parser.add_argument("--skip-trend", action="store_true", help="Trend taramasini atla")
    parser.add_argument("--dry-run", action="store_true", help="Dosya yazmadan goster")
    args = parser.parse_args()

    ensure_dirs()
    today = date.today().isoformat()

    print("\n" + "=" * 55)
    print("  BOTFUSIONS — Gunluk Veri Toplama Agenti")
    print("=" * 55)
    print(f"  Tarih: {today}")
    print("=" * 55)

    # ── 1. Google Ads ──
    ads_data = {}
    ads_path = PERF_DIR / f"{today}-ads-performans.md"
    if not args.skip_ads:
        print("  [1/4] Google Ads verisi cekiliyor...")
        ads_data = fetch_ads_summary()
        if "error" in ads_data:
            print(f"         HATA: {ads_data['error']}")
        else:
            print("         OK")
    else:
        print("  [1/4] Google Ads -- atlandi")

    # ── 2. Sosyal Medya + Trend ──
    omni_posts = []
    trend_path = TREND_DIR / f"{today}-trend.md"
    if not args.skip_trend:
        print("  [2/4] OmniSocials postlari cekiliyor...")
        omni_posts = fetch_omni_posts()
        print(f"         {len(omni_posts)} post bulundu")
    else:
        print("  [2/4] Trend -- atlandi")

    # ── 3. Pipeline stats ──
    print("  [3/4] Pipeline istatistikleri...")
    pipeline_stats = fetch_pipeline_stats()
    print("         OK")

    # ── 4. Rakip Analizi ──
    print("  [4/4] Rakip analiz snapshot'i...")
    comp_data = fetch_competitor_snapshot()
    comp_path = RAKIP_DIR / f"{today}-rakip-snapshot.md"
    if not args.dry_run:
        comp_path = write_competitor_snapshot(comp_data)
        print(f"         OK → {comp_path.name}")
    else:
        print("         DRY-RUN")

    print()

    if args.dry_run:
        print("[DRY RUN] Dosya yazilmadi.")
        print(f"  Ads data: {json.dumps(ads_data, ensure_ascii=False, indent=2)[:200]}...")
        print(f"  Omni posts: {len(omni_posts)}")
        print(f"  Pipeline stats: {json.dumps(pipeline_stats, ensure_ascii=False)[:200]}...")
        return

    # ── Dosyalari yaz ──
    print("  Dosyalar yaziliyor...")
    if not args.skip_ads and "error" not in ads_data:
        ads_path = write_ads_performance(ads_data)
        print(f"    Ads: {ads_path}")

    if not args.skip_trend:
        trend_path = write_trend_snapshot([], omni_posts)
        print(f"    Trend: {trend_path}")

    summary_path = write_daily_summary(ads_path, trend_path, pipeline_stats, ads_data)
    print(f"    Ozet: {summary_path}")

    append_to_log(
        f"ads-performans + trend + ozet → tamamlandi "
        f"(ads={'OK' if 'error' not in ads_data else 'HATA'}, "
        f"posts={len(omni_posts)})"
    )
    print(f"    Log guncellendi")

    print()
    print("  Tamamlandi.")
    print()


if __name__ == "__main__":
    main()
