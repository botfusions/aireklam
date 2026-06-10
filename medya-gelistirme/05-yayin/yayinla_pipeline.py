"""
Pipeline Yayın Scripti — Onaylı paketleri OmniSocials ile yayınlar.
===============================================================
Kullanim:
  python yayinla_pipeline.py                     # bekleyenleri yayinla
  python yayinla_pipeline.py --dry-run           # goster ama yayinlama
  python yayinla_pipeline.py --status visual_approved  # belirli durumu filtrele
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

API = "http://127.0.0.1:8765"
ROOT = Path(__file__).resolve().parent.parent.parent


def _read_cmo_key() -> str:
    """secrets.env'den CMO_API_KEY oku — POST endpoint'ler icin zorunlu."""
    secrets_path = ROOT / "secrets.env"
    if not secrets_path.exists():
        return ""
    for line in secrets_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("CMO_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


CMO_KEY = _read_cmo_key()


def fetch_pending(status="visual_approved"):
    """Bekleyen paketleri Flask API'den çek."""
    try:
        r = requests.get(f"{API}/api/pipeline/packages", params={"status": status, "limit": "50"}, timeout=10)
        r.raise_for_status()
        return r.json().get("packages", [])
    except Exception as e:
        print(f"[HATA] Paket cekilemedi: {e}")
        return []


def fetch_detail(pkg_id):
    """Tek paket detayını çek."""
    try:
        r = requests.get(f"{API}/api/pipeline/packages/{pkg_id}", timeout=10)
        r.raise_for_status()
        return r.json().get("package")
    except Exception as e:
        print(f"[HATA] Paket {pkg_id} detay alinamadi: {e}")
        return None


def publish_package(pkg, dry_run=False):
    """Tek paketi yayınla."""
    pkg_id = pkg.get("id")
    hook   = pkg.get("hook_text", "")[:50]
    plats  = ", ".join(pkg.get("platforms", []))

    if dry_run:
        print(f"  [DRY-RUN] #{pkg_id}: \"{hook}...\" → {plats}")
        return {"ok": True, "dry_run": True}

    try:
        r = requests.post(
            f"{API}/api/pipeline/packages/{pkg_id}/publish",
            json={},
            headers={"Content-Type": "application/json", "X-CMO-Key": CMO_KEY},
            timeout=30,
        )
        r.raise_for_status()
        result = r.json()
        ok = result.get("ok", False)
        published = result.get("published", [])
        errors = result.get("errors", [])

        if ok:
            published_platforms = [p["platform"] for p in published]
            print(f"  [OK] #{pkg_id}: \"{hook}...\" → {', '.join(published_platforms)}")
        else:
            print(f"  [FAIL] #{pkg_id}: {errors}")

        return result
    except Exception as e:
        print(f"  [HATA] #{pkg_id} yayinlanamadi: {e}")
        return {"ok": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Pipeline yayin scripti")
    parser.add_argument("--dry-run", action="store_true", help="Goster ama yayinlama")
    parser.add_argument("--status", default="visual_approved",
                        help="Hangi durumdaki paketler yayinlansin (default: visual_approved)")
    parser.add_argument("--id", type=int, help="Sadece belirli bir paketi yayinla")
    args = parser.parse_args()

    print(f"{'[DRY-RUN] ' if args.dry_run else ''}Pipeline Yayin — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Durum filtresi: {args.status}")
    print("-" * 50)

    # API sağlık kontrolü
    try:
        r = requests.get(f"{API}/api/health", timeout=5)
        r.raise_for_status()
    except Exception:
        print(f"[HATA] Flask API calismiyor. Once: python gsc_api_server.py")
        sys.exit(1)

    # Paketleri çek
    if args.id:
        pkg = fetch_detail(args.id)
        if not pkg:
            print(f"[HATA] Paket #{args.id} bulunamadi")
            sys.exit(1)
        packages = [pkg]
    else:
        packages = fetch_pending(args.status)

    if not packages:
        print("Yayinlanacak paket yok.")
        return

    print(f"{len(packages)} paket bulundu.\n")

    results = {"ok": 0, "fail": 0, "dry_run": 0}
    for pkg in packages:
        result = publish_package(pkg, dry_run=args.dry_run)
        if result.get("dry_run"):
            results["dry_run"] += 1
        elif result.get("ok"):
            results["ok"] += 1
        else:
            results["fail"] += 1
        time.sleep(1)  # rate limit koruması

    print("-" * 50)
    print(f"Sonuc: {results['ok']} yayinlandi, {results['fail']} basarisiz, {results['dry_run']} dry-run")


if __name__ == "__main__":
    main()
