"""
Icerik Uretim Motoru — Medya Gelistirme Pipeline
=================================================
Kullanim: python icerik_uret.py --niche geo --hook-type number --topic "GEO nedir"
Flask API'ye (localhost:8765) gonderir.
"""
import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

try:
    import requests as req_lib
except ImportError:
    sys.exit("requests gerekli: pip install requests")

# ── Dizinler ──────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent.parent
API = "http://localhost:8765"
HAZIFA_DIR = ROOT / "hafiza"
ICERIK_ARSIV = HAZIFA_DIR / "icerik-arsivi"

# ── Platform karakter limitleri ──────────────────────
# Kaynak: .agents/OMNISOCIALS.md + SISTEM-KONTEKST.md
# X Premium hesap = 25000 karakter (standart X = 280)
LIMITS = {
    "x": 25000,         # X Premium (@botfusionss)
    "pinterest": 500,
    "instagram": 2200,
    "tiktok": 2200,
    "facebook": 63206,
    "linkedin": 3000,
    "youtube": 5000,    # YouTube aciklama
}

# ── Niche tanimlari ──────────────────────────────────
NICHES = {
    "geo": {
        "name": "GEO / AI SEO",
        "landing": "botfusions.com/geo-hizmet",
        "proof": "%527 organik trafik artisi",
        "hooks": {
            "number": [
                "%527 organik trafik artisi — 90 gunde, yapay zeka optimizasyonuyla",
                "Turkiye'de GEO bilen ajans sayisi: 5'ten az. Biz biriyiz.",
                "$500 Tanisma Paketi — global rakip $1.499'dan basliyor",
            ],
            "pain_point": [
                "Musteriniz ChatGPT'ye soruyor. Rakibiniz cikiyor. Siz cikmiyorsunuz.",
                "Google'da 1. sayfadasiniz ama ChatGPT'de hic gorunmuyorsunuz.",
                "SEO butceniz bosa gidiyor cunku AI aramalarda yoksunuz.",
            ],
            "curiosity": [
                "Bu ay kacinca soru isinizle ilgili ChatGPT'den gecti? Bilmiyorsunuz.",
                "SEO'nun yeri degisti: artik sayfalar degil, AI'lar siraliyor.",
                "Google trafiginiz dusuyor mu? Sorun sizde degil, arama degisti.",
            ],
            "social_proof": [
                "Musteri #1: '%527 organik trafik artisi, 90 gunde' — GEO calismasi sonucu",
                "Turkiye'nin ilk GEO ajanslarindan biri: Botfusions",
                "Dunya capinda GEO trendi: 2026'da aramalarin %40'i AI'dan gelecek",
            ],
        }
    },
    "agentic": {
        "name": "Agentic Sistemler",
        "proof": "7/24 calisan otonom AI agent",
        "hooks": {
            "number": [
                "7/24 calisan, hic yorulmayan dijital calisan — 5K-50K USD kurulum",
            ],
            "pain_point": [
                "Operasyonunuz tekrar eden islerle bogusuyor mu? AI agent bunu cozer.",
                "3 kisiye yaptiginiz isi 1 AI agent yapabilir.",
            ],
            "curiosity": [
                "Claude SDK ile kendi AI agentinizi kurmak ne kadar surer? Yanit: 2 hafta.",
            ],
            "social_proof": [
                "Botfusions: Claude SDK + MCP ile otonom is akislari kuruyor",
            ],
        }
    },
    "chatbot": {
        "name": "AI Chatbot & Asistanlar",
        "proof": "%80 musteri hizmetleri maliyet dususu",
        "hooks": {
            "number": [
                "Musteri hizmetleri maliyetini %80 dusurun — AI chatbot ile",
            ],
            "pain_point": [
                "Gece 3'te gelen musterinize kim cevap veriyor? Chatbot'unuz.",
            ],
            "curiosity": [
                "E-ticarette her 100 zfxiyerin 70'i soru soruyor. Kaci cevap aliyor?",
            ],
            "social_proof": [
                "Aylık 500-2.000 USD retainer ile 7/24 musteri destegi",
            ],
        }
    },
}


def truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def adapt_for_platforms(default_caption: str, hook_text: str) -> dict:
    """Her platform icin caption adapt et."""
    adapted = {}
    for platform, limit in LIMITS.items():
        caption = f"{hook_text}\n\n{default_caption}"
        adapted[f"caption_{platform}"] = truncate(caption, limit)
    return adapted


def generate_content_package(niche: str, hook_type: str, topic: str) -> dict:
    """Icerik paketi olustur."""
    niche_data = NICHES.get(niche)
    if not niche_data:
        sys.exit(f"Bilinmeyen niche: {niche}. Secenekler: {list(NICHES.keys())}")

    hooks = niche_data["hooks"].get(hook_type)
    if not hooks:
        sys.exit(f"Bilinmeyen hook_type: {hook_type}. Secenekler: {list(niche_data['hooks'].keys())}")

    hook_text = hooks[0]
    if topic:
        hook_text = f"{topic} | {hook_text}"

    default_caption = (
        f"{niche_data.get('proof', '')}\n\n"
        f"Daha fazla bilgi: {niche_data.get('landing', 'botfusions.com')}\n"
        f"İletişim: info@botfusions.com | +90 850 302 74 60\n\n"
        f"#Botfusions #AI #{niche.upper()}"
    )

    platform_captions = adapt_for_platforms(default_caption, hook_text)

    return {
        "niche": niche,
        "hook_type": hook_type,
        "hook_text": hook_text,
        "caption_default": default_caption,
        **platform_captions,
        "platforms": [
            "881407_instagram", "881407_facebook",
            "881407_x", "881407_pinterest",
            "881407_tiktok",
        ],
        "post_type": "post",
        "strategy_reason": f"Otomatik uretim: niche={niche}, hook={hook_type}, topic={topic}",
        "campaign": niche,
    }


def save_to_pipeline(package: dict) -> dict:
    """Flask API'ye gonder."""
    try:
        r = req_lib.post(
            f"{API}/api/pipeline/packages",
            json=package,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        r.raise_for_status()
        return r.json()
    except req_lib.ConnectionError:
        sys.exit("Flask API calismiyor. Once: python gsc_api_server.py")
    except Exception as e:
        sys.exit(f"API hatasi: {e}")


def log_to_hafiza(package: dict, result: dict) -> None:
    """hafiza/icerik-arsivi/ altina log yaz."""
    ICERIK_ARSIV.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    slug = package["niche"]
    path = ICERIK_ARSIV / f"{today}-{slug}.md"

    lines = [
        f"# Icerik Paketi — {today}",
        f"",
        f"- **Niche:** {package['niche']}",
        f"- **Hook tipi:** {package['hook_type']}",
        f"- **Hook:** {package['hook_text'][:80]}...",
        f"- **Durum:** {result.get('ok', False)}",
        f"- **Paket ID:** {result.get('package', {}).get('id', 'N/A')}",
        f"",
        f"## Caption (varsayilan)",
        f"",
        package["caption_default"],
        f"",
    ]
    for key in ["caption_x", "caption_instagram", "caption_tiktok", "caption_pinterest", "caption_facebook"]:
        if package.get(key):
            lines.extend([f"## {key}", "", package[key], ""])

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Log yazildi: {path}")


def main():
    parser = argparse.ArgumentParser(description="Botfusions Icerik Uretim Motoru")
    parser.add_argument("--niche", required=True, choices=list(NICHES.keys()))
    parser.add_argument("--hook-type", required=True, choices=["number", "pain_point", "curiosity", "social_proof"])
    parser.add_argument("--topic", default="", help="Opsiyonel konu basligi")
    parser.add_argument("--dry-run", action="store_true", help="API'ye gondermeden goster")
    args = parser.parse_args()

    package = generate_content_package(args.niche, args.hook_type, args.topic)

    print("\n" + "=" * 55)
    print("  BOTFUSIONS — Icerik Uretim Motoru")
    print("=" * 55)
    print(f"  Niche      : {package['niche']}")
    print(f"  Hook tipi  : {package['hook_type']}")
    print(f"  Hook       : {package['hook_text'][:70]}...")
    print(f"  Platformlar: {len(package['platforms'])}")
    print(f"  Caption    : {package['caption_default'][:80]}...")
    print("=" * 55 + "\n")

    if args.dry_run:
        print("[DRY RUN] API'ye gonderilmedi.")
        print(json.dumps(package, ensure_ascii=False, indent=2))
        return

    result = save_to_pipeline(package)
    log_to_hafiza(package, result)
    print(f"Paket olusturuldu: ID={result.get('package', {}).get('id', 'N/A')}")


if __name__ == "__main__":
    main()
