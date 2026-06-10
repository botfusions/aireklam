# -*- coding: utf-8 -*-
"""2026-W24 paketlerini onaylanan metinlerle guncelle + content_approved yap.

Kullanici onayi: 10 Haziran 2026 — "x haric hepsinde yayinla"
Platformlar: X haric — post/carousel: IG+FB+TikTok+Pinterest, reel: IG+FB+TikTok+YouTube
"""
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent.parent
API = "http://localhost:8765"


def _read_secret(name):
    # Flask ile ayni oncelik sirasi: once 05-gsc-nocodb/.env, sonra secrets.env
    for env_file in [ROOT / "05-gsc-nocodb" / ".env", ROOT / "secrets.env"]:
        if not env_file.exists():
            continue
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith(f"{name}="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


SUPA_URL = _read_secret("SUPABASE_URL")
SUPA_KEY = _read_secret("SUPABASE_ANON_KEY")
CMO_KEY = _read_secret("CMO_API_KEY")

POST_PLATFORMS = ["881407_instagram", "881407_facebook", "881407_tiktok", "881407_pinterest"]
REEL_PLATFORMS = ["881407_instagram", "881407_facebook", "881407_tiktok", "881407_youtube"]

CAPTIONS = {
    1: """Turkiye'de GEO bilen ajans sayisi: 5'ten az. Biz biriyiz.

ChatGPT, Gemini ve Perplexity artik musterilerinizin yeni arama motoru. Bu araclarda gorunmek icin klasik SEO yetmiyor; iceriginizin yapay zeka tarafindan anlasilir ve alintilanabilir olmasi gerekiyor.

Ilk musterimizde sonuc: 90 gunde %527 organik trafik artisi.

Tanisma Paketi $500 - botfusions.com/geo-hizmet
#GEO #AISEO #Botfusions""",
    2: """Gece 3'te gelen musterinize kim cevap veriyor? Chatbot'unuz.

Siteye gelen ziyaretcilerin cogu mesai disinda soru soruyor. Cevap alamayan musteri rakibe gidiyor. AI chatbot 7/24 cevapliyor, randevu aliyor, satisa yonlendiriyor.

Musteri hizmetleri maliyetinde %80'e varan dusus.

Detay: botfusions.com | info@botfusions.com
#AIChatbot #MusteriDeneyimi #Botfusions""",
    3: """Claude SDK ile kendi AI agent'inizi kurmak ne kadar surer? Yanit: 2 hafta.

Tekrar eden operasyon isleri - raporlama, veri girisi, musteri takibi - artik otonom ajanlarla yuruyor. Kurulumu yapiyoruz, ekibiniz sadece onayliyor.

7/24 calisan, yorulmayan dijital calisan.

Kesif gorusmesi: info@botfusions.com
#AgenticAI #Otomasyon #ClaudeSDK""",
    4: """Dunya capinda GEO trendi: 2026'da aramalarin %40'i AI'dan gelecek.

Google'da 1. sayfada olmak artik yetmiyor. Musteriniz soruyu ChatGPT'ye soruyor ve orada yalnizca AI'in tanidigi markalar oneriliyor.

Markanizin AI gorunurlugunu ucretsiz tariyoruz: botfusions.com/geo-hizmet
#GEO #YapayZeka #DijitalPazarlama""",
    5: """Musteri hizmetleri maliyetini %80 dusurun.

E-ticarette her 100 ziyaretcinin 70'i soru soruyor. Kaci cevap aliyor? AI chatbot tum sorulara aninda yanit veriyor, sepet terkini azaltiyor.

Aylik 500$'dan baslayan kurulum + yonetim.

botfusions.com | +90 850 302 74 60
#ETicaret #AIChatbot #Botfusions""",
    6: """Musteriniz ChatGPT'ye soruyor. Rakibiniz cikiyor. Siz cikmiyorsunuz.

Her gun binlerce "en iyi X firmasi hangisi?" sorusu AI'lara soruluyor. Cevapta olmayan marka, o musteriyi hic gormuyor bile.

90 gunde kanitlanmis sonuc: %527 organik trafik artisi.

Ucretsiz AI gorunurluk analizi: botfusions.com/geo-hizmet
#GEO #ChatGPT #AIVisibility""",
    7: """Turkiye'de gercekten teslim eden az sayida agentic sistem kurucusundan biriyiz.

Claude SDK + MCP ile kurdugumuz otonom is akislari: rapor uretimi, sosyal medya pipeline'i, veri toplama, musteri takibi. Kendi ajansimizi bu sistemlerle yonetiyoruz - sattigimiz seyi her gun kullaniyoruz.

Kurulum 5K-50K USD | Kesif: info@botfusions.com
#AgenticAI #MCP #Otomasyon""",
    8: """Google trafiginiz dusuyor mu? Sorun sizde degil, arama degisti.

Kullanicilar cevabi artik arama sonuclarinda degil, dogrudan AI sohbetinde aliyor. Tiklama azaliyor cunku soru size hic ulasmiyor.

Cozum: iceriginizi AI'larin kaynak gosterdigi formata tasimak. Buna GEO diyoruz.

botfusions.com/geo-hizmet
#GEO #SEO #AISearch""",
}

# post_type'a gore platform secimi (reel: 2,5,6,8 | carousel/post: 1,3,4,7)
REELS = {2, 5, 6, 8}


def main():
    if not (SUPA_URL and SUPA_KEY and CMO_KEY):
        sys.exit("secrets.env eksik: SUPABASE_URL / SUPABASE_ANON_KEY / CMO_API_KEY")

    headers = {
        "Authorization": f"Bearer {SUPA_KEY}",
        "apikey": SUPA_KEY,
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    }

    for pkg_id, caption in CAPTIONS.items():
        platforms = REEL_PLATFORMS if pkg_id in REELS else POST_PLATFORMS
        patch = {"caption_default": caption, "platforms": platforms}
        r = requests.patch(
            f"{SUPA_URL}/rest/v1/content_packages?id=eq.{pkg_id}",
            headers=headers, json=patch, timeout=15,
        )
        r.raise_for_status()
        print(f"  #{pkg_id} guncellendi ({'reel' if pkg_id in REELS else 'post'}, {len(platforms)} kanal)")

        a = requests.post(
            f"{API}/api/pipeline/packages/{pkg_id}/approve",
            json={"approved_by": "cenk"},
            headers={"Content-Type": "application/json", "X-CMO-Key": CMO_KEY},
            timeout=15,
        )
        a.raise_for_status()
        print(f"  #{pkg_id} -> content_approved")

    print("\nTamamlandi: 8/8 paket guncellendi ve onaylandi.")


if __name__ == "__main__":
    main()
