# -*- coding: utf-8 -*-
"""2026-W24 statik kart uretimi — HTML sablon + Playwright screenshot.

Kullanim: python kart-sablon.py
4 kart uretir: chatbot x2, agentic x2 (1080x1080 PNG).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

TEMPLATE = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: 1080px; height: 1080px;
    background: linear-gradient(145deg, #0f0a1e 0%, #1a1033 55%, #2d1457 100%);
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #fff; overflow: hidden; position: relative;
  }}
  .glow {{
    position: absolute; width: 700px; height: 700px; border-radius: 50%;
    background: radial-gradient(circle, {accent}33 0%, transparent 65%);
    top: -200px; right: -200px;
  }}
  .container {{
    position: relative; z-index: 2; height: 100%;
    display: flex; flex-direction: column; justify-content: space-between;
    padding: 90px 80px;
  }}
  .badge {{
    display: inline-block; align-self: flex-start;
    background: {accent}22; border: 2px solid {accent};
    color: {accent}; font-size: 26px; font-weight: 700;
    padding: 12px 28px; border-radius: 999px; letter-spacing: 2px;
  }}
  .hook {{
    font-size: {hook_size}px; font-weight: 800; line-height: 1.22;
    margin: 40px 0 0 0;
  }}
  .hook .vurgu {{ color: {accent}; }}
  .alt {{
    font-size: 34px; line-height: 1.5; color: #c9c2dd; margin-top: 36px;
  }}
  .footer {{
    display: flex; justify-content: space-between; align-items: flex-end;
    border-top: 2px solid #ffffff22; padding-top: 36px;
  }}
  .brand {{ font-size: 38px; font-weight: 800; }}
  .brand span {{ color: #A855F7; }}
  .cta {{
    background: #F97316; color: #fff; font-size: 28px; font-weight: 700;
    padding: 18px 36px; border-radius: 14px;
  }}
</style>
</head>
<body>
  <div class="glow"></div>
  <div class="container">
    <div>
      <div class="badge">{badge}</div>
      <div class="hook">{hook}</div>
      <div class="alt">{alt}</div>
    </div>
    <div class="footer">
      <div class="brand">bot<span>fusions</span></div>
      <div class="cta">{cta}</div>
    </div>
  </div>
</body>
</html>"""

CARDS = [
    {
        "out": "chatbot-gece3-1x1.png",
        "badge": "AI CHATBOT",
        "accent": "#3B82F6",
        "hook_size": 64,
        "hook": 'Gece 3\'te gelen müşterinize<br>kim cevap veriyor?<br><span class="vurgu">Chatbot\'unuz.</span>',
        "alt": "7/24 cevap · randevu · satışa yönlendirme.<br>Müşteri hizmetleri maliyetinde %80'e varan düşüş.",
        "cta": "botfusions.com",
    },
    {
        "out": "chatbot-maliyet80-1x1.png",
        "badge": "AI CHATBOT",
        "accent": "#3B82F6",
        "hook_size": 64,
        "hook": 'Müşteri hizmetleri maliyetini<br><span class="vurgu">%80 düşürün.</span>',
        "alt": "E-ticarette her 100 ziyaretçinin 70'i soru soruyor.<br>Kaçı cevap alıyor? AI chatbot anında yanıtlıyor.",
        "cta": "botfusions.com",
    },
    {
        "out": "agentic-2hafta-1x1.png",
        "badge": "AGENTIC SİSTEMLER",
        "accent": "#A855F7",
        "hook_size": 60,
        "hook": 'Kendi AI agent\'ınızı kurmak<br>ne kadar sürer?<br><span class="vurgu">Yanıt: 2 hafta.</span>',
        "alt": "Raporlama, veri girişi, müşteri takibi — otonom ajanlarla.<br>7/24 çalışan, yorulmayan dijital çalışan.",
        "cta": "info@botfusions.com",
    },
    {
        "out": "geo-5ten-az-1x1.png",
        "badge": "GEO / AI SEO",
        "accent": "#FDE047",
        "hook_size": 62,
        "hook": 'Türkiye\'de GEO bilen<br>ajans sayısı: <span class="vurgu">5\'ten az.</span><br>Biz biriyiz.',
        "alt": "ChatGPT, Gemini ve Perplexity yeni arama motoru.<br>İlk müşterimizde 90 günde %527 organik trafik artışı.",
        "cta": "botfusions.com/geo-hizmet",
    },
    {
        "out": "geo-trend40-1x1.png",
        "badge": "GEO / AI SEO",
        "accent": "#FDE047",
        "hook_size": 60,
        "hook": '2026\'da aramaların<br><span class="vurgu">%40\'ı AI\'dan</span> gelecek.',
        "alt": "Google'da 1. sayfa artık yetmiyor. ChatGPT yalnızca<br>tanıdığı markaları öneriyor. Ücretsiz AI görünürlük taraması.",
        "cta": "botfusions.com/geo-hizmet",
    },
    {
        "out": "geo-trafik-dusuyor-1x1.png",
        "badge": "GEO / AI SEO",
        "accent": "#FDE047",
        "hook_size": 60,
        "hook": 'Google trafiğiniz düşüyor mu?<br>Sorun sizde değil,<br><span class="vurgu">arama değişti.</span>',
        "alt": "Cevaplar artık AI sohbetinde veriliyor. Çözüm: içeriğinizi<br>AI'ların kaynak gösterdiği formata taşımak. Buna GEO diyoruz.",
        "cta": "botfusions.com/geo-hizmet",
    },
    {
        "out": "agentic-teslim-1x1.png",
        "badge": "AGENTIC SİSTEMLER",
        "accent": "#A855F7",
        "hook_size": 58,
        "hook": 'Türkiye\'de <span class="vurgu">gerçekten teslim eden</span><br>az sayıda agentic sistem<br>kurucusundan biriyiz.',
        "alt": "Claude SDK + MCP ile otonom iş akışları.<br>Sattığımız şeyi her gün kendimiz kullanıyoruz.",
        "cta": "info@botfusions.com",
    },
]


def main():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("playwright gerekli: pip install playwright && playwright install chromium")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1080})
        for card in CARDS:
            html_path = HERE / card["out"].replace(".png", ".html")
            html_path.write_text(TEMPLATE.format(**{k: v for k, v in card.items() if k != "out"}), encoding="utf-8")
            page.goto(html_path.as_uri())
            page.wait_for_timeout(400)
            out_path = HERE / card["out"]
            page.screenshot(path=str(out_path))
            print(f"  OK: {out_path.name}")
        browser.close()
    print("\n4 kart uretildi.")


if __name__ == "__main__":
    main()
