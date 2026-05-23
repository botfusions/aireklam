"""
Performans Toplama — Yayınlanan içeriklerin performansını toplar ve sisteme geri besler.
=======================================================================================
Kullanim:
  python performans_topla.py                  # gunluk performans raporu
  python performans_topla.py --dry-run        # goster ama kaydetme
  python performans_topla.py --haftalik       # haftalik ozet
  python performans_topla.py --aylik          # aylik rapor
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

import requests

API = "http://127.0.0.1:8765"
ROOT = Path(__file__).resolve().parent.parent.parent  # proje root
PERF_DIR = ROOT / "hafiza" / "performans-tarihi"
HOOK_DIR = ROOT / "hafiza" / "hook-kutuphanesi"


def ensure_dirs():
    """Gerekli klasörleri olustur."""
    PERF_DIR.mkdir(parents=True, exist_ok=True)
    HOOK_DIR.mkdir(parents=True, exist_ok=True)


def fetch_pipeline_stats():
    """Pipeline istatistiklerini çek."""
    try:
        r = requests.get(f"{API}/api/pipeline/stats", timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[UYARI] Pipeline stats alinamadi: {e}")
        return {}


def fetch_published_packages(days=7):
    """Son N gunde yayinlanan paketleri çek."""
    try:
        r = requests.get(
            f"{API}/api/pipeline/packages",
            params={"status": "published", "limit": "100"},
            timeout=10,
        )
        r.raise_for_status()
        packages = r.json().get("packages", [])
        # Client-side filtre: son N gun
        cutoff = datetime.now() - timedelta(days=days)
        filtered = []
        for p in packages:
            pub_date = p.get("published_at") or p.get("updated_at") or p.get("created_at", "")
            if pub_date:
                try:
                    dt = datetime.fromisoformat(pub_date.replace("Z", "+00:00"))
                    if dt.replace(tzinfo=None) >= cutoff:
                        filtered.append(p)
                except (ValueError, TypeError):
                    filtered.append(p)
        return filtered
    except Exception as e:
        print(f"[UYARI] Yayinlanan paketler alinamadi: {e}")
        return []


def fetch_ads_summary():
    """Google Ads performans özetini çek."""
    try:
        r = requests.get(f"{API}/api/google-ads/summary", timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[UYARI] Google Ads verisi alinamadi: {e}")
        return {}


def analyze_hook_performance(packages):
    """Hook tipi bazında performans analizi."""
    hook_stats = {}
    niche_stats = {}
    type_stats = {}

    for p in packages:
        hook_type = p.get("hook_type", "unknown")
        niche = p.get("niche", "unknown")
        post_type = p.get("post_type", "unknown")

        hook_stats[hook_type] = hook_stats.get(hook_type, 0) + 1
        niche_stats[niche] = niche_stats.get(niche, 0) + 1
        type_stats[post_type] = type_stats.get(post_type, 0) + 1

    return {
        "by_hook_type": hook_stats,
        "by_niche": niche_stats,
        "by_post_type": type_stats,
        "total_published": len(packages),
    }


def generate_report(packages, stats, ads_data, mode="gunluk"):
    """Performans raporu olustur."""
    hook_analysis = analyze_hook_performance(packages)
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")

    report = {
        "tarih": date_str,
        "mod": mode,
        "pipeline_stats": stats,
        "ads_summary": ads_data,
        "yayin_analiz": hook_analysis,
    }

    # En iyi hook tipini bul
    by_hook = hook_analysis.get("by_hook_type", {})
    if by_hook:
        best_hook = max(by_hook, key=by_hook.get)
        report["en_iyi_hook"] = best_hook

    # En iyi niche
    by_niche = hook_analysis.get("by_niche", {})
    if by_niche:
        best_niche = max(by_niche, key=by_niche.get)
        report["en_iyi_niche"] = best_niche

    return report


def save_report(report, mode="gunluk"):
    """Raporu dosyaya kaydet."""
    date_str = report["tarih"]
    filename = f"{date_str}-performans-{mode}.json"
    filepath = PERF_DIR / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return filepath


def save_hook_analysis(report):
    """Hook performans özetini hook-kutuphanesi'ne kaydet."""
    date_str = report["tarih"]
    by_hook = report.get("yayin_analiz", {}).get("by_hook_type", {})

    if not by_hook:
        return

    hook_file = HOOK_DIR / "hook-performans.json"

    # Mevcut veriyi oku (varsa)
    existing = {}
    if hook_file.exists():
        try:
            with open(hook_file, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except Exception:
            pass

    # Güncelle
    existing[date_str] = by_hook

    with open(hook_file, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    return hook_file


def format_markdown_report(report):
    """JSON raporu markdown formatına çevir."""
    lines = [
        f"# Performans Raporu — {report['tarih']}",
        f"Mod: {report['mod']}",
        "",
        "## Pipeline Durumu",
        f"- Toplam paket: {report.get('pipeline_stats', {}).get('total', 0)}",
    ]

    by_status = report.get("pipeline_stats", {}).get("by_status", {})
    for status, count in by_status.items():
        lines.append(f"- {status}: {count}")

    lines.append("")
    lines.append("## Yayın Analizi")
    lines.append(f"- Toplam yayınlanan: {report.get('yayin_analiz', {}).get('total_published', 0)}")

    by_hook = report.get("yayin_analiz", {}).get("by_hook_type", {})
    if by_hook:
        lines.append("")
        lines.append("### Hook Tipi Dağılımı")
        for hook, count in sorted(by_hook.items(), key=lambda x: -x[1]):
            lines.append(f"- {hook}: {count}")

    by_niche = report.get("yayin_analiz", {}).get("by_niche", {})
    if by_niche:
        lines.append("")
        lines.append("### Niche Dağılımı")
        for niche, count in sorted(by_niche.items(), key=lambda x: -x[1]):
            lines.append(f"- {niche}: {count}")

    if report.get("en_iyi_hook"):
        lines.append(f"\n**En iyi hook tipi:** {report['en_iyi_hook']}")
    if report.get("en_iyi_niche"):
        lines.append(f"**En iyi niche:** {report['en_iyi_niche']}")

    lines.append("")
    lines.append(f"---\n*Otomatik üretim: performans_topla.py — {report['tarih']}*")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Performans toplama")
    parser.add_argument("--dry-run", action="store_true", help="Goster ama kaydetme")
    parser.add_argument("--haftalik", action="store_true", help="Haftalik ozet (7 gun)")
    parser.add_argument("--aylik", action="store_true", help="Aylik rapor (30 gun)")
    args = parser.parse_args()

    if args.haftalik:
        mode, days = "haftalik", 7
    elif args.aylik:
        mode, days = "aylik", 30
    else:
        mode, days = "gunluk", 1

    print(f"{'[DRY-RUN] ' if args.dry_run else ''}Performans Toplama — {mode}")
    print(f"Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("-" * 50)

    # API sağlık kontrolü
    try:
        r = requests.get(f"{API}/api/health", timeout=5)
        r.raise_for_status()
    except Exception:
        print(f"[HATA] Flask API calismiyor. Once: python gsc_api_server.py")
        sys.exit(1)

    # Veri çek
    stats = fetch_pipeline_stats()
    packages = fetch_published_packages(days=days)
    ads_data = fetch_ads_summary()

    print(f"Pipeline: {stats.get('total', 0)} toplam paket")
    print(f"Son {days} gunde yayinlanan: {len(packages)} paket")
    print(f"Google Ads: {'var' if ads_data else 'yok'}")

    # Rapor olustur
    report = generate_report(packages, stats, ads_data, mode=mode)
    md = format_markdown_report(report)

    print("\n" + md)

    if not args.dry_run:
        ensure_dirs()
        json_path = save_report(report, mode=mode)
        hook_path = save_hook_analysis(report)
        print(f"\n[OK] JSON rapor: {json_path}")
        if hook_path:
            print(f"[OK] Hook analizi: {hook_path}")

        # Markdown raporu da kaydet
        md_path = PERF_DIR / f"{report['tarih']}-performans-{mode}.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"[OK] MD rapor: {md_path}")
    else:
        print("\n[DRY-RUN] Kaydedilmedi.")


if __name__ == "__main__":
    main()
