"""
Gorsel Brief Uretici — Onaylı paketlerden görsel brief + WaveSpeed task olusturur.
=================================================================================
Kullanim:
  python gorsel_brief_uret.py                       # bekleyen brief'leri uret
  python gorsel_brief_uret.py --dry-run             # goster ama gonderme
  python gorsel_brief_uret.py --id 5                # belirli paket
  python gorsel_brief_uret.py --model nano-banana   # model sec (gpt-image / nano-banana / seedream)
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

API = "http://127.0.0.1:8765"

# ── Botfusions Marka Renkleri ──
BRAND_COLORS = {
    "primary_purple": "#A855F7",
    "dark_purple":    "#7C3AED",
    "blue":           "#3B82F6",
    "orange":         "#F97316",
    "yellow":         "#FDE047",
}

# ── Platform Boyutlari ──
PLATFORM_SIZES = {
    "instagram_feed":  {"w": 1080, "h": 1080, "aspect": "1:1"},
    "instagram_story": {"w": 1080, "h": 1920, "aspect": "9:16"},
    "instagram_reel":  {"w": 1080, "h": 1920, "aspect": "9:16"},
    "tiktok":          {"w": 1080, "h": 1920, "aspect": "9:16"},
    "youtube_thumb":   {"w": 1280, "h": 720,  "aspect": "16:9"},
    "pinterest":       {"w": 1000, "h": 1500, "aspect": "2:3"},
    "x_facebook":      {"w": 1200, "h": 628,  "aspect": "1.91:1"},
}

# ── Model Eslemeleri ──
MODELS = {
    "gpt-image":   "openai/gpt-image-2-text-to-image",
    "nano-banana": "google/nano-banana-2-text-to-image",
    "seedream":    "bytedance/seedream-v4.5",
}

# Niche → Gorsel stil kilavuzu
NICHE_STYLES = {
    "geo": "modern, tech, data visualization style, clean geometric shapes, AI-themed",
    "agentic": "futuristic, autonomous systems, circuit patterns, blue-purple gradient",
    "chatbot": "friendly, conversational UI, speech bubbles, warm colors, approachable",
}


def build_visual_prompt(pkg, platform_key=None):
    """Paket verisinden görsel üretim promptu olustur."""
    niche     = pkg.get("niche", "geo")
    hook      = pkg.get("hook_text", "")
    post_type = pkg.get("post_type", "post")
    caption   = pkg.get("caption_default", "")

    style = NICHE_STYLES.get(niche, NICHE_STYLES["geo"])

    prompt_parts = [
        f"Professional marketing image for {niche} AI service",
        f"Brand colors: purple {BRAND_COLORS['primary_purple']}, dark purple {BRAND_COLORS['dark_purple']}, blue {BRAND_COLORS['blue']}",
        f"Style: {style}",
        f"Text overlay: \"{hook[:80]}\"",
        "Company: Botfusions",
        "Clean layout, modern typography, no clutter",
    ]

    if post_type == "carousel":
        prompt_parts.append("Carousel card design, single slide")
    elif post_type == "reel":
        prompt_parts.append("Vertical format, video thumbnail style")

    return ". ".join(prompt_parts)


def build_brief(pkg):
    """Tam görsel brief JSON'u olustur."""
    platforms = pkg.get("platforms", [])
    post_type = pkg.get("post_type", "post")

    # Platform boyut eslemesi
    sizes = {}
    for p in platforms:
        if "instagram" in p:
            key = "instagram_story" if post_type in ("reel", "story") else "instagram_feed"
            sizes[key] = PLATFORM_SIZES.get(key)
        elif "tiktok" in p:
            sizes["tiktok"] = PLATFORM_SIZES["tiktok"]
        elif "youtube" in p:
            sizes["youtube_thumb"] = PLATFORM_SIZES["youtube_thumb"]
        elif "pinterest" in p:
            sizes["pinterest"] = PLATFORM_SIZES["pinterest"]
        elif p in ("x", "facebook"):
            sizes["x_facebook"] = PLATFORM_SIZES["x_facebook"]

    if not sizes:
        sizes["instagram_feed"] = PLATFORM_SIZES["instagram_feed"]

    return {
        "prompt": build_visual_prompt(pkg),
        "sizes": sizes,
        "niche": pkg.get("niche"),
        "hook_text": pkg.get("hook_text"),
        "post_type": post_type,
        "brand_colors": BRAND_COLORS,
        "model_suggestion": "nano-banana",  # varsayılan: hızlı + ucuz
    }


def submit_wavespeed(brief, model_key="nano-banana", dry_run=False):
    """WaveSpeed'e görsel üretim taski gönder."""
    model_id = MODELS.get(model_key, MODELS["nano-banana"])
    prompt = brief["prompt"]

    payload = {
        "model": model_id,
        "prompt": prompt,
    }
    # Maliyet kontrolü: GPT Image ve Nano Banana icin zorunlu ayarlar
    if model_key in ("gpt-image", "nano-banana"):
        payload["resolution"] = "1K"
        payload["quality"] = "low"
        payload["aspect_ratio"] = "auto"
        payload["format"] = "png"

    if dry_run:
        print(f"  [DRY-RUN] Model: {model_id}")
        print(f"  [DRY-RUN] Prompt: {prompt[:100]}...")
        return {"dry_run": True, "model": model_id}

    try:
        r = requests.post(
            f"{API}/api/wavespeed/generate",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30,
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"  [HATA] WaveSpeed gonderilemedi: {e}")
        return {"error": str(e)}


def update_package_status(pkg_id, status, visual_brief=None, dry_run=False):
    """Paket durumunu Supabase'de güncelle."""
    if dry_run:
        print(f"  [DRY-RUN] Paket #{pkg_id} → {status}")
        return

    try:
        payload = {"status": status}
        if visual_brief:
            payload["visual_brief"] = visual_brief
        requests.post(
            f"{API}/api/pipeline/packages/{pkg_id}/approve",
            json={"status_override": status, "visual_brief": visual_brief},
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
    except Exception:
        pass  # status update hatasi ana akisi durdurmamali


def fetch_pending():
    """content_approved durumundaki paketleri çek."""
    try:
        r = requests.get(
            f"{API}/api/pipeline/packages",
            params={"status": "content_approved", "limit": "50"},
            timeout=10,
        )
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


def main():
    parser = argparse.ArgumentParser(description="Gorsel brief uretici")
    parser.add_argument("--dry-run", action="store_true", help="Goster ama gonderme")
    parser.add_argument("--id", type=int, help="Belirli paket ID")
    parser.add_argument("--model", default="nano-banana",
                        choices=list(MODELS.keys()),
                        help="WaveSpeed modeli (default: nano-banana)")
    args = parser.parse_args()

    print(f"{'[DRY-RUN] ' if args.dry_run else ''}Gorsel Brief Uretici — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Model: {args.model}")
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
        packages = fetch_pending()

    if not packages:
        print("Gorsel uretilecek paket yok (content_approved bekleniyor).")
        return

    print(f"{len(packages)} paket icin brief olusturuluyor.\n")

    for pkg in packages:
        pkg_id = pkg.get("id")
        hook = pkg.get("hook_text", "")[:50]
        niche = pkg.get("niche")

        print(f"#{pkg_id} [{niche}] \"{hook}...\"")

        # Brief olustur
        brief = build_brief(pkg)
        print(f"  Brief: {json.dumps(brief['sizes'], ensure_ascii=False)}")

        # WaveSpeed'e gönder
        result = submit_wavespeed(brief, model_key=args.model, dry_run=args.dry_run)

        if result.get("dry_run"):
            print(f"  → DRY-RUN tamam\n")
        elif result.get("error"):
            print(f"  → HATA: {result['error']}\n")
        elif result.get("taskId"):
            task_id = result["taskId"]
            print(f"  → WaveSpeed task: {task_id}")
            # Brief'i pakete kaydet + durum güncelle
            brief["wave_task_id"] = task_id
            brief["wave_model"] = args.model
            update_package_status(pkg_id, "producing_visual", visual_brief=brief, dry_run=args.dry_run)
            print(f"  → Durum: producing_visual\n")
        else:
            print(f"  → Bilinmeyen yanit: {json.dumps(result, ensure_ascii=False)[:100]}\n")

        time.sleep(2)  # rate limit

    print("-" * 50)
    print("Tamam. Gorsel urestikten sonra /api/wavespeed/status/{taskId} ile kontrol edin.")


if __name__ == "__main__":
    main()
