"""
Strateji Olusturucu — Medya Gelistirme Pipeline Faz 3
=====================================================
Kullanim: python strateji_olustur.py [--hafta 2026-W21] [--niche geo]
hafiza/ verilerini okur, haftalik icerik plani + hook secimi uretir.
Flask API'ye (localhost:8765) paket olarak gonderir (opsiyonel).
"""
import argparse
import json
import random
import sys
from datetime import date, timedelta
from pathlib import Path

try:
    import requests as req_lib
except ImportError:
    sys.exit("requests gerekli: pip install requests")

ROOT = Path(__file__).resolve().parent.parent.parent
API = "http://localhost:8765"
HAZIFA_DIR = ROOT / "hafiza"


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

# ── Niche tanimlari (SISTEM-KONTEKST.md ile uyumlu) ─────────
NICHES = {
    "geo": {
        "name": "GEO / AI SEO",
        "landing": "botfusions.com/geo-hizmet",
        "proof": "%527 organik trafik artisi",
        "target": ["KOBI sahipleri", "dijital pazarlamacilar"],
        "platform_priority": ["instagram", "linkedin", "x", "tiktok"],
        "formats": ["carousel", "reel", "post"],
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
                "Bu ay kac soru isinizle ilgili ChatGPT'den gecti? Bilmiyorsunuz.",
                "SEO'nun yeri degisti: artik sayfalar degil, AI'lar siraliyor.",
                "Google trafiginiz dusuyor mu? Sorun sizde degil, arama degisti.",
            ],
            "social_proof": [
                "Musteri #1: '%527 organik trafik artisi, 90 gunde' — GEO calismasi sonucu",
                "Turkiye'nin ilk GEO ajanslarindan biri: Botfusions",
                "Dunya capinda GEO trendi: 2026'da aramalarin %40'i AI'dan gelecek",
            ],
        },
    },
    "agentic": {
        "name": "Agentic Sistemler",
        "proof": "7/24 calisan otonom AI agent",
        "target": ["sirketler", "girisimler"],
        "platform_priority": ["linkedin", "x"],
        "formats": ["post", "carousel"],
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
        },
    },
    "chatbot": {
        "name": "AI Chatbot & Asistanlar",
        "proof": "%80 musteri hizmetleri maliyet dususu",
        "target": ["e-ticaret", "hizmet sektoru"],
        "platform_priority": ["instagram", "facebook", "tiktok"],
        "formats": ["reel", "post", "story"],
        "hooks": {
            "number": [
                "Musteri hizmetleri maliyetini %80 dusurun — AI chatbot ile",
            ],
            "pain_point": [
                "Gece 3'te gelen musterinize kim cevap veriyor? Chatbot'unuz.",
            ],
            "curiosity": [
                "E-ticarette her 100 ziyaretci 70'i soru soruyor. Kaci cevap aliyor?",
            ],
            "social_proof": [
                "Aylik 500-2.000 USD retainer ile 7/24 musteri destegi",
            ],
        },
    },
}

# ── Haftalik gonderim plani (gunluk dagilim) ────────────────
WEEKLY_SCHEDULE = {
    "Pazartesi": {"geo": "number", "chatbot": "pain_point"},
    "Sali": {"agentic": "curiosity"},
    "Carsamba": {"geo": "social_proof"},
    "Persembe": {"chatbot": "number"},
    "Cuma": {"geo": "pain_point", "agentic": "social_proof"},
    "Cumartesi": {"geo": "curiosity"},
}


def read_hook_performance() -> dict:
    """hafiza/hook-kutuphanesi/ altindaki performans kayitlarini oku."""
    perf = {}
    hook_dir = HAZIFA_DIR / "hook-kutuphanesi"
    if not hook_dir.exists():
        return perf
    for f in hook_dir.glob("*.md"):
        lines = f.read_text(encoding="utf-8").splitlines()
        hooks = []
        for line in lines:
            if line.startswith("- hook:"):
                hook_text = line.split(":", 1)[1].strip()
                hooks.append(hook_text)
            elif line.startswith("  ortalama_engagement:") and hooks:
                val = line.split(":", 1)[1].strip()
                perf[hooks[-1]] = float(val.replace("%", "")) if val != "N/A" else 0
    return perf


def read_rakip_activity() -> list:
    """hafiza/rakip-arsivi/ altindaki son snapshot'lari oku."""
    rakip_dir = HAZIFA_DIR / "rakip-arsivi"
    if not rakip_dir.exists():
        return []
    snapshots = sorted(rakip_dir.glob("*-snapshot.md"), reverse=True)[:3]
    activity = []
    for snap in snapshots:
        content = snap.read_text(encoding="utf-8")
        lines = content.splitlines()
        for line in lines:
            if line.startswith("- ") and ("aktif" in line.lower() or "yeni" in line.lower()):
                activity.append(line[2:].strip())
    return activity


def read_trends() -> list:
    """hafiza/trend-log/ altindaki son trend ozetlerini oku."""
    trend_dir = HAZIFA_DIR / "trend-log"
    if not trend_dir.exists():
        return []
    trends = sorted(trend_dir.glob("*.md"), reverse=True)[:2]
    items = []
    for t in trends:
        content = t.read_text(encoding="utf-8")
        for line in content.splitlines():
            if line.startswith("- ") and len(line) > 10:
                items.append(line[2:].strip())
    return items[:10]


def select_best_hook(niche: str, hook_type: str, performance: dict) -> str:
    """Performans verisine gore en iyi hook'u sec, yoksa rastgele."""
    hooks = NICHES[niche]["hooks"].get(hook_type, [])
    if not hooks:
        return ""

    scored = []
    for h in hooks:
        score = performance.get(h, 0)
        scored.append((h, score))
    scored.sort(key=lambda x: x[1], reverse=True)

    if scored[0][1] > 0:
        return scored[0][0]
    return random.choice(hooks)


def generate_weekly_plan(week_label: str, niche_filter: str = "") -> dict:
    """Haftalik icerik plani olustur."""
    performance = read_hook_performance()
    rakip = read_rakip_activity()
    trends = read_trends()

    plan = {
        "week": week_label,
        "generated_at": date.today().isoformat(),
        "days": [],
        "strategy_notes": [],
        "rakip_notlari": rakip[:5],
        "trend_notlari": trends[:5],
    }

    for gun, niche_hook_map in WEEKLY_SCHEDULE.items():
        for niche, hook_type in niche_hook_map.items():
            if niche_filter and niche != niche_filter:
                continue
            niche_data = NICHES[niche]
            hook_text = select_best_hook(niche, hook_type, performance)
            if not hook_text:
                continue
            platforms = niche_data["platform_priority"][:2]
            fmt = random.choice(niche_data["formats"])
            plan["days"].append({
                "gun": gun,
                "niche": niche,
                "hook_type": hook_type,
                "hook_text": hook_text,
                "platformlar": platforms,
                "format": fmt,
                "kanit": niche_data["proof"],
            })

    if rakip:
        plan["strategy_notes"].append(
            f"Rakip aktivitesi tespit edildi: {len(rakip)} hareket. "
            "Fark vurgula: Botfusions somut veri ile konusuyor."
        )
    if not performance:
        plan["strategy_notes"].append(
            "Hook performans verisi yok — varsayilan hook'lar kullanildi. "
            "Veri toplandikca strateji otomatik iyilesir."
        )

    return plan


def write_plan_files(plan: dict) -> tuple:
    """haftalik-plan.md ve hook-secimi.md dosyalarini yaz."""
    output_dir = Path(__file__).resolve().parent
    week = plan["week"]

    # ── haftalik-plan.md ──
    plan_lines = [
        f"# Haftalik Icerik Plani — {week}",
        "",
        f"Olusturulma: {plan['generated_at']}",
        "",
    ]

    if plan["strategy_notes"]:
        plan_lines.append("## Strateji Notlari")
        for note in plan["strategy_notes"]:
            plan_lines.append(f"- {note}")
        plan_lines.append("")

    if plan["rakip_notlari"]:
        plan_lines.append("## Rakip Aktivitesi")
        for r in plan["rakip_notlari"]:
            plan_lines.append(f"- {r}")
        plan_lines.append("")

    if plan["trend_notlari"]:
        plan_lines.append("## Trend Sinyalleri")
        for t in plan["trend_notlari"]:
            plan_lines.append(f"- {t}")
        plan_lines.append("")

    plan_lines.append("## Gunluk Plan")
    plan_lines.append("")
    plan_lines.append("| Gun | Niche | Hook Tipi | Hook | Platformlar | Format |")
    plan_lines.append("|-----|-------|-----------|------|-------------|--------|")
    for day in plan["days"]:
        hook_preview = day["hook_text"][:50] + "..." if len(day["hook_text"]) > 50 else day["hook_text"]
        plan_lines.append(
            f"| {day['gun']} | {day['niche']} | {day['hook_type']} | "
            f"{hook_preview} | {', '.join(day['platformlar'])} | {day['format']} |"
        )

    plan_lines.append("")
    plan_lines.append("---")
    plan_lines.append(f"*Otomatik uretim: strateji_olustur.py — {plan['generated_at']}*")

    plan_path = output_dir / "haftalik-plan.md"
    plan_path.write_text("\n".join(plan_lines), encoding="utf-8")

    # ── hook-secimi.md ──
    hook_lines = [
        f"# Hook Secimi — {week}",
        "",
        f"Olusturulma: {plan['generated_at']}",
        "",
        "## Secilen Hook'lar",
        "",
    ]
    for day in plan["days"]:
        hook_lines.append(f"### {day['gun']} — {day['niche']} ({day['hook_type']})")
        hook_lines.append(f"**Hook:** {day['hook_text']}")
        hook_lines.append(f"**Kanit:** {day['kanit']}")
        hook_lines.append(f"**Platformlar:** {', '.join(day['platformlar'])}")
        hook_lines.append(f"**Format:** {day['format']}")
        hook_lines.append("")

    hook_path = output_dir / "hook-secimi.md"
    hook_path.write_text("\n".join(hook_lines), encoding="utf-8")

    return plan_path, hook_path


def send_packages_to_api(plan: dict) -> list:
    """Plandaki her gun icin content_package olustur ve Flask API'ye gonder."""
    results = []
    for day in plan["days"]:
        niche_data = NICHES[day["niche"]]
        default_caption = (
            f"{niche_data['proof']}\n\n"
            f"Daha fazla bilgi: {niche_data.get('landing', 'botfusions.com')}\n"
            f"Iletisim: info@botfusions.com | +90 850 302 74 60\n\n"
            f"#Botfusions #AI #{day['niche'].upper()}"
        )
        package = {
            "niche": day["niche"],
            "hook_type": day["hook_type"],
            "hook_text": day["hook_text"],
            "caption_default": default_caption,
            "platforms": [
                f"881407_{p}" for p in day["platformlar"]
            ],
            "post_type": day["format"],
            "strategy_reason": f"Haftalik plan: {plan['week']} — {day['gun']} {day['niche']}",
            "campaign": day["niche"],
        }
        try:
            r = req_lib.post(
                f"{API}/api/pipeline/packages",
                json=package,
                headers={"Content-Type": "application/json", "X-CMO-Key": CMO_KEY},
                timeout=10,
            )
            r.raise_for_status()
            results.append({"gun": day["gun"], "niche": day["niche"], "ok": True})
        except Exception as e:
            results.append({"gun": day["gun"], "niche": day["niche"], "ok": False, "error": str(e)})
    return results


def main():
    parser = argparse.ArgumentParser(description="Botfusions Strateji Olusturucu")
    parser.add_argument("--hafta", default="", help="Hafta etiketi (orn: 2026-W21)")
    parser.add_argument("--niche", default="", choices=["", "geo", "agentic", "chatbot"],
                        help="Tek niche icin plan olustur")
    parser.add_argument("--send", action="store_true", help="Plani Flask API'ye gonder")
    parser.add_argument("--dry-run", action="store_true", help="Dosya yazmadan goster")
    args = parser.parse_args()

    week_label = args.hafta or f"{date.today().isocalendar()[0]}-W{date.today().isocalendar()[1]:02d}"

    plan = generate_weekly_plan(week_label, args.niche)

    print("\n" + "=" * 55)
    print("  BOTFUSIONS — Strateji Olusturucu")
    print("=" * 55)
    print(f"  Hafta      : {plan['week']}")
    print(f"  Gunluk plan: {len(plan['days'])} icerik")
    print(f"  Rakip data : {len(plan['rakip_notlari'])} not")
    print(f"  Trend data : {len(plan['trend_notlari'])} sinyal")
    print("=" * 55)

    for day in plan["days"]:
        hook_preview = day["hook_text"][:60]
        print(f"  {day['gun']:10s} | {day['niche']:8s} | {day['hook_type']:14s} | {hook_preview}...")

    print()

    if plan["strategy_notes"]:
        print("  Strateji Notlari:")
        for note in plan["strategy_notes"]:
            print(f"    - {note}")
        print()

    if args.dry_run:
        print("[DRY RUN] Dosya yazilmadi.")
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return

    plan_path, hook_path = write_plan_files(plan)
    print(f"  Plan yazildi : {plan_path}")
    print(f"  Hook yazildi : {hook_path}")

    if args.send:
        print("\n  Paketler API'ye gonderiliyor...")
        results = send_packages_to_api(plan)
        ok_count = sum(1 for r in results if r["ok"])
        print(f"  Sonuc: {ok_count}/{len(results)} basarili")
        for r in results:
            status = "OK" if r["ok"] else f"HATA: {r.get('error', '')}"
            print(f"    {r['gun']:10s} | {r['niche']:8s} | {status}")
    else:
        print("  [NOT] --send ile paketleri API'ye gonderebilirsiniz.")

    print()


if __name__ == "__main__":
    main()
