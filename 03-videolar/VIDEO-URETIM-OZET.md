# Video Üretim Özeti — Nisan 2026

## Proje: ChatGPT / Claude / Gemini "Seni Görüyor mu?" Reklamı

---

## Üretilen Dosyalar

| Dosya | Format | Boyut | Açıklama |
|-------|--------|-------|----------|
| `geo-ai-reklam-9x16.html` | HTML | — | HyperFrames kompozisyonu (tarayıcıda izlenebilir, GSAP animasyonlu) |
| `geo-ai-reklam-sesli.mp4` | 1080×1920 | 3.4 MB | 9:16 Story — müzikli |
| `geo-ai-reklam-1x1-v2.mp4` | 1080×1080 | 2.2 MB | 1:1 Feed — natif render |
| `geo-ai-reklam-1x1-sesli.mp4` | 1080×1080 | 2.9 MB | 1:1 Feed — müzikli |

---

## Video İçeriği (6 Sahne · 30 Saniye)

| Zaman | Sahne | Mesaj |
|-------|-------|-------|
| 0–5s | Açılış | ChatGPT / Claude / Gemini orb'ları — "Yeni Arama Motoru" |
| 5–10s | İstatistik | %0→%62 counter animasyonu — "AI'a soruyor" |
| 10–14s | Soru | Brand pill'lar + glitch efekti — "Seni görüyor mu?" |
| 14–19s | Problem | Rakipler ✓ GÖRÜNÜR / Siz ✗ BULUNAMADI |
| 19–25s | Çözüm | Botfusions GEO Hizmeti — 3 checkmark |
| 25–30s | CTA | "Görünür Ol Şimdi" + botfusions.com/geo-hizmet |

---

## Teknik Detaylar

- **Render motoru:** Python PIL + ffmpeg (Chrome bağımsız)
- **Render scripti (9:16):** `render_video.py`
- **Render scripti (1:1):** `render_1x1.py`
- **Müzik:** Web Audio API (HTML) + numpy synthetic beat (MP4)
- **Beat:** 128 BPM — kick, hi-hat, Am-F-C-G bas + synth pad
- **Renk paleti:** Botfusions (#A855F7 purple, #22d3ee cyan, #F97316 orange)
- **Font:** DejaVu Sans Bold (Türkçe destekli)

---

## HyperFrames Entegrasyonu

Kurulu skill'ler → `.agents/skills/video/hyperframes/`

| Skill | Kullanım |
|-------|----------|
| `hyperframes` | HTML → Video kompozisyon motoru |
| `hyperframes-cli` | init, preview, render, tts |
| `website-to-hyperframes` | Siteyi videoya çevir |
| `gsap` | Animasyon kütüphanesi |

**Not:** HyperFrames CLI render için Chrome gerektirir. Sandbox'ta Chrome olmadığından Python PIL pipeline kullanıldı. Lokal makinede `npx hyperframes render` ile HTML'den de MP4 üretilebilir.

---

## Model Kullanımı

| Görev | Model |
|-------|-------|
| DESIGN.md, reklam kopyası, sahne kurgusu | Sonnet 4 |
| Render script yazma, ses üretme, format dönüşümü | **Haiku 4** |

---

## Sonraki Adımlar

- [ ] 16:9 (Facebook/YouTube) format da üret
- [ ] Türkçe ses seslendirme (TTS) ekle — `hyperframes tts`
- [ ] A/B test için farklı hook varyasyonları (Opus 4 ile)
- [ ] Google Ads'e yükle — kampanya hedefleme ayarla

---

*Botfusions AI Reklam Ajansı | Nisan 2026*
