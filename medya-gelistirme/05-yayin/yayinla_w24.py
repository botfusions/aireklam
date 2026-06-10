# -*- coding: utf-8 -*-
"""2026-W24 paket yayini — OmniSocials (X haric).

Kullanim:
  python yayinla_w24.py --paket 4,2,3,6      # secili paketleri yayinla
  python yayinla_w24.py --paket 1 --dry-run  # goster ama yayinlama

Akis: media upload -> create-and-publish -> Supabase status=published + social_posts log
Pinterest: nested {"pinterest": {"board_id": ...}} formati (Oturum 9 kaniti).
Image post: IG+FB (+Pinterest ayri cagri). Reel: IG+FB+TikTok+YouTube.
"""
import argparse
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent.parent
API_BASE = "https://api.omnisocials.com"
FLASK = "http://localhost:8765"

BOARD_GEO = "1091067515915706441"
BOARD_PROFIL = "1091067515915706431"


def _read_secret(name):
    for env_file in [ROOT / "05-gsc-nocodb" / ".env", ROOT / "secrets.env"]:
        if not env_file.exists():
            continue
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith(f"{name}="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


OMNI_KEY = _read_secret("OMNISOCIALS_API_KEY")
SUPA_URL = _read_secret("SUPABASE_URL")
SUPA_KEY = _read_secret("SUPABASE_ANON_KEY")

GORSEL = ROOT / "02-gorseller" / "w24-gorseller"

# Paket -> medya ve yayin tipi eslemesi
MEDIA_MAP = {
    1: {"file": GORSEL / "geo-5ten-az-1x1.png", "kind": "post", "board": BOARD_GEO},
    2: {"file": GORSEL / "chatbot-gece3-1x1.png", "kind": "post", "board": BOARD_PROFIL},
    3: {"file": GORSEL / "agentic-2hafta-1x1.png", "kind": "post", "board": BOARD_PROFIL},
    4: {"file": GORSEL / "geo-trend40-1x1.png", "kind": "post", "board": BOARD_GEO},
    5: {"file": GORSEL / "chatbot-maliyet80-1x1.png", "kind": "post", "board": BOARD_PROFIL},
    6: {"file": ROOT / "04-araclar" / "hyperframes" / "geo-reklam-20s" / "output" / "geo-reklam-20s.mp4",
        "kind": "reel",
        "yt_title": "Musteriniz ChatGPT'ye Soruyor, Siz Cikmiyorsunuz | GEO | Botfusions"},
    7: {"file": GORSEL / "agentic-teslim-1x1.png", "kind": "post", "board": BOARD_PROFIL},
    8: {"file": GORSEL / "geo-trafik-dusuyor-1x1.png", "kind": "post", "board": BOARD_GEO},
}


def supa_headers(representation=False):
    h = {"Authorization": f"Bearer {SUPA_KEY}", "apikey": SUPA_KEY,
         "Content-Type": "application/json"}
    h["Prefer"] = "return=representation" if representation else "return=minimal"
    return h


def get_package(pkg_id):
    r = requests.get(f"{SUPA_URL}/rest/v1/content_packages?id=eq.{pkg_id}",
                     headers=supa_headers(), timeout=15)
    r.raise_for_status()
    rows = r.json()
    if not rows:
        sys.exit(f"Paket #{pkg_id} bulunamadi")
    return rows[0]


def upload_media(path: Path):
    mime = "video/mp4" if path.suffix == ".mp4" else "image/png"
    with open(path, "rb") as f:
        r = requests.post(
            f"{API_BASE}/v1/media/upload",
            headers={"Authorization": f"Bearer {OMNI_KEY}"},
            files={"file": (path.name, f, mime)},
            timeout=300,
        )
    r.raise_for_status()
    media_id = r.json().get("data", {}).get("id")
    if not media_id:
        sys.exit(f"Medya upload basarisiz: {r.text[:300]}")
    return media_id


def publish(payload):
    r = requests.post(
        f"{API_BASE}/v1/posts/create-and-publish",
        headers={"Authorization": f"Bearer {OMNI_KEY}", "Content-Type": "application/json"},
        json=payload,
        timeout=120,
    )
    try:
        data = r.json()
    except Exception:
        data = {"raw": r.text[:300]}
    return r.status_code, data


def mark_published(pkg_id, post_ids, errors):
    status = "published" if post_ids and not errors else ("failed" if not post_ids else "published")
    patch = {"status": status, "published_post_ids": post_ids}
    if status == "published":
        patch["published_at"] = "now()"
    requests.patch(f"{SUPA_URL}/rest/v1/content_packages?id=eq.{pkg_id}",
                   headers=supa_headers(), json=patch, timeout=15)
    return status


def log_social_post(pkg, omni_id, accounts):
    try:
        requests.post(f"{SUPA_URL}/rest/v1/social_posts", headers=supa_headers(), json={
            "omnisocials_post_id": str(omni_id),
            "caption": pkg["caption_default"][:1000],
            "platforms": accounts,
            "post_type": pkg.get("post_type", "post"),
            "status": "published",
            "campaign": pkg.get("campaign", ""),
        }, timeout=15)
    except Exception:
        pass


def yayinla_paket(pkg_id, dry_run=False):
    pkg = get_package(pkg_id)
    media = MEDIA_MAP[pkg_id]
    caption = pkg["caption_default"]
    print(f"\n--- Paket #{pkg_id} ({pkg['niche']}/{media['kind']}) ---")
    print(f"  Medya : {media['file'].name}")
    print(f"  Hook  : {pkg['hook_text'][:60]}")

    if not media["file"].exists():
        sys.exit(f"  HATA: medya dosyasi yok: {media['file']}")
    if dry_run:
        print("  [DRY-RUN] yayinlanmadi")
        return

    media_id = upload_media(media["file"])
    print(f"  Medya ID: {media_id}")

    post_ids, errors = [], []

    if media["kind"] == "reel":
        payload = {
            "content": {"default": caption, "youtube": caption},
            "accounts": ["881407_instagram", "881407_facebook", "881407_youtube", "881407_tiktok"],
            "media_ids": [media_id],
            "type": "reel",
            "youtube": {"title": media["yt_title"], "privacy_status": "public"},
            "tiktok": {"privacy_level": "PUBLIC_TO_EVERYONE"},
        }
        code, data = publish(payload)
        omni_id = data.get("data", {}).get("id") or data.get("post", {}).get("id") or data.get("id")
        if code in (200, 201) and omni_id:
            post_ids.append(omni_id)
            log_social_post(pkg, omni_id, payload["accounts"])
            print(f"  Reel OK: #{omni_id} (IG+FB+YT+TikTok)")
        else:
            errors.append(data)
            print(f"  Reel HATA {code}: {str(data)[:200]}")
    else:
        # 1) IG + FB post
        payload = {
            "content": {"default": caption},
            "accounts": ["881407_instagram", "881407_facebook"],
            "media_ids": [media_id],
            "type": "post",
        }
        code, data = publish(payload)
        omni_id = data.get("data", {}).get("id") or data.get("post", {}).get("id") or data.get("id")
        if code in (200, 201) and omni_id:
            post_ids.append(omni_id)
            log_social_post(pkg, omni_id, payload["accounts"])
            print(f"  Post OK: #{omni_id} (IG+FB)")
        else:
            errors.append(data)
            print(f"  Post HATA {code}: {str(data)[:200]}")

        # 2) Pinterest (ayri cagri, nested board_id)
        pin_payload = {
            "content": {"default": caption},
            "accounts": ["881407_pinterest"],
            "media_ids": [media_id],
            "type": "post",
            "pinterest": {"board_id": media["board"]},
        }
        code, data = publish(pin_payload)
        omni_id = data.get("data", {}).get("id") or data.get("post", {}).get("id") or data.get("id")
        if code in (200, 201) and omni_id:
            post_ids.append(omni_id)
            log_social_post(pkg, omni_id, ["881407_pinterest"])
            print(f"  Pinterest OK: #{omni_id}")
        else:
            errors.append(data)
            print(f"  Pinterest HATA {code}: {str(data)[:200]}")

    status = mark_published(pkg_id, post_ids, errors)
    print(f"  Durum: {status} | post_ids: {post_ids}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--paket", required=True, help="Virgullu paket ID listesi, orn: 4,2,3,6")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not OMNI_KEY:
        sys.exit("OMNISOCIALS_API_KEY bulunamadi")

    ids = [int(x) for x in args.paket.split(",")]
    for pkg_id in ids:
        yayinla_paket(pkg_id, args.dry_run)
    print("\nTamamlandi.")


if __name__ == "__main__":
    main()
