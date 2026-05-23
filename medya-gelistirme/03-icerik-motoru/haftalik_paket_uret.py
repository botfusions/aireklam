"""
Haftalik Plan → Paket Uretim Koprugu
=====================================
02-strateji/haftalik-plan.md dosyasini okur,
her satir icin icerik_uret.py fonksiyonunu cagirarak
pipeline'a paket olarak kaydeder.

Kullanim:
  python haftalik_paket_uret.py                 # bu haftanin planindan paket uret
  python haftalik_paket_uret.py --dry-run       # goster ama kaydetme
  python haftalik_paket_uret.py --gun sali      # sadece sali icin uret
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import requests as req_lib
except ImportError:
    sys.exit("requests gerekli: pip install requests")

ROOT = Path(__file__).resolve().parent.parent.parent
API = "http://localhost:8765"
PLAN_PATH = ROOT / "medya-gelistirme" / "02-strateji" / "haftalik-plan.md"

# Niche eslemeleri (Turkce → ingilizce)
NICHE_MAP = {
    "geo": "geo",
    "agentic": "agentic",
    "chatbot": "chatbot",
}

# Hook tipi eslemeleri (Turkce → ingilizce)
HOOK_MAP = {
    "number": "number",
    "pain_point": "pain_point",
    "curiosity": "curiosity",
    "social_proof": "social_proof",
    "rakam": "number",
    "aci nokta": "pain_point",
    "merak": "curiosity",
    "sosyal kanit": "social_proof",
}

# Format → post_type eslemesi
FORMAT_MAP = {
    "carousel": "carousel",
    "reel": "reel",
    "post": "post",
    "story": "story",
}

# Platform → OmniSocials account ID
PLATFORM_MAP = {
    "instagram": "881407_instagram",
    "facebook": "881407_facebook",
    "youtube": "881407_youtube",
    "tiktok": "881407_tiktok",
    "pinterest": "881407_pinterest",
    "x": "881407_x",
    "linkedin": None,  # OmniSocials'ta LinkedIn yok
}


def parse_haftalik_plan(plan_path: Path, gun_filter: str = None) -> list[dict]:
    """haftalik-plan.md dosyasini parse et → satir listesi."""
    if not plan_path.exists():
        print(f"[HATA] Plan dosyasi bulunamadi: {plan_path}")
        return []

    content = plan_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Tablo satirlarini bul (| ile baslayan,Gun iceren)
    rows = []
    in_table = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|") and "Gun" in stripped:
            in_table = True
            continue
        if stripped.startswith("|") and "---" in stripped:
            continue
        if in_table and stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")]
            cells = [c for c in cells if c]  # boslari temizle
            if len(cells) >= 6:
                rows.append({
                    "gun": cells[0],
                    "niche": cells[1],
                    "hook_type": cells[2],
                    "hook_text": cells[3],
                    "platformlar": cells[4],
                    "format": cells[5],
                })

    # Gun filtresi
    if gun_filter:
        gun_filter_lower = gun_filter.lower()
        rows = [r for r in rows if gun_filter_lower in r["gun"].lower()]

    return rows


def row_to_package(row: dict) -> dict:
    """Plan satirini pipeline paket formatina cevir."""
    niche = NICHE_MAP.get(row["niche"].lower(), "geo")
    hook_type = HOOK_MAP.get(row["hook_type"].lower(), "curiosity")
    hook_text = row["hook_text"]
    fmt = FORMAT_MAP.get(row["format"].lower(), "post")

    # Platformlari account ID'lere cevir
    platform_names = [p.strip().lower() for p in row["platformlar"].split(",")]
    platform_ids = []
    for p in platform_names:
        if p in PLATFORM_MAP and PLATFORM_MAP[p]:
            platform_ids.append(PLATFORM_MAP[p])

    # Caption olustur
    niche_data = {
        "geo": {"proof": "%527 organik trafik artisi", "landing": "botfusions.com/geo-hizmet"},
        "agentic": {"proof": "7/24 calisan otonom AI agent", "landing": "botfusions.com"},
        "chatbot": {"proof": "%80 musteri hizmetleri maliyet dususu", "landing": "botfusions.com"},
    }
    nd = niche_data.get(niche, niche_data["geo"])

    caption = (
        f"{nd['proof']}\n\n"
        f"{hook_text}\n\n"
        f"Daha fazla bilgi: {nd['landing']}\n"
        f"Iletisim: info@botfusions.com | +90 850 302 74 60\n\n"
        f"#Botfusions #AI #{niche.upper()}"
    )

    return {
        "niche": niche,
        "hook_type": hook_type,
        "hook_text": hook_text,
        "caption_default": caption,
        "platforms": platform_ids,
        "post_type": fmt,
        "strategy_reason": f"Haftalik plan: {row['gun']} - {niche}/{hook_type}",
        "campaign": niche,
    }


def submit_package(package: dict, dry_run=False) -> dict:
    """Paketi Flask API'ye gonder."""
    if dry_run:
        hook = package["hook_text"][:50]
        plats = ", ".join(package["platforms"])
        print(f"  [DRY-RUN] {package['niche']}/{package['hook_type']}: \"{hook}...\" → {plats}")
        return {"ok": True, "dry_run": True}

    try:
        r = req_lib.post(
            f"{API}/api/pipeline/packages",
            json=package,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        r.raise_for_status()
        result = r.json()
        pkg_id = result.get("package", {}).get("id", "?")
        hook = package["hook_text"][:50]
        print(f"  [OK] #{pkg_id} {package['niche']}/{package['hook_type']}: \"{hook}...\"")
        return result
    except req_lib.ConnectionError:
        print(f"  [HATA] Flask API calismiyor")
        return {"ok": False, "error": "API connection failed"}
    except Exception as e:
        print(f"  [HATA] {e}")
        return {"ok": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Haftalik plan → pipeline paket uretimi")
    parser.add_argument("--dry-run", action="store_true", help="Goster ama kaydetme")
    parser.add_argument("--gun", default=None, help="Sadece belirli gun (orn: sali, persembe)")
    args = parser.parse_args()

    print(f"{'[DRY-RUN] ' if args.dry_run else ''}Haftalik Plan → Paket Uretimi")
    print(f"Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("-" * 50)

    # API kontrol
    try:
        r = req_lib.get(f"{API}/api/health", timeout=5)
        r.raise_for_status()
    except Exception:
        print(f"[HATA] Flask API calismiyor. Once: python gsc_api_server.py")
        sys.exit(1)

    # Plani oku
    rows = parse_haftalik_plan(PLAN_PATH, gun_filter=args.gun)
    if not rows:
        print("Plan bos veya bulunamadi.")
        print(f"Beklenen dosya: {PLAN_PATH}")
        return

    print(f"{len(rows)} plan satiri bulundu.\n")

    ok_count = 0
    fail_count = 0
    for row in rows:
        package = row_to_package(row)
        result = submit_package(package, dry_run=args.dry_run)
        if result.get("ok"):
            ok_count += 1
        else:
            fail_count += 1

    print("-" * 50)
    print(f"Sonuc: {ok_count} paket olusturuldu, {fail_count} basarisiz")
    if not args.dry_run:
        print("\nSonraki adim: CMO Dashboard > Pipeline > Onayla")


if __name__ == "__main__":
    main()
