---
name: wavespeed
description: "WaveSpeedAI — Botfusions secilmis modeller. GPT Image 2, Nano Banana 2, Seedream 4.5, Kling 3.0, Seedance 2.0. Gorsel, video, muzik uretimi."
argument-hint: "image | video | edit | music | bg-remove | upscale <prompt>"
version: 1.2.0
license: MIT
---

# WaveSpeedAI — Botfusions Secilmis Modeller

## When to Activate

TRIGGER when the user:
- Gorsel uretmek istediginde ("gorsel uret", "resim olustur")
- Video uretmek istediginde ("video uret", "reklam videosu")
- Gorsel duzenlemek istediginde ("gorsel duzenle", "edit image")
- Muzik/ses uretmek istediginde ("muzik olustur", "jingle")
- Arka plan kaldirmak istediginde ("bg kaldir")
- "wavespeed" veya "wave" dediginde

## API Bilgileri

**Base URL:** `https://api.wavespeed.ai/api/v3/`
**Auth:** `Authorization: Bearer $WAVESPEED_API_KEY`
**Env:** `WAVESPEED_API_KEY`

```
1. POST /api/v3/{model_id} → taskId al
2. GET /api/v3/predictions/{taskId} → poll et
3. Sonuc URL'sini al
```

---

## GORSEL MODELLERI (3)

| # | Model | Model ID | Aciklama |
|---|-------|----------|----------|
| 1 | **GPT Image 2** | `openai/gpt-image-2-text-to-image` | OpenAI "thinking" model — tutarli, metin-hassas, production-ready |
| 2 | **Nano Banana 2** | `google/nano-banana-2-text-to-image` | Hizli, yuksek kalite, guclu tutarlilik, gercekci |
| 3 | **Seedream 4.5** | `bytedance/seedream-v4.5` | Cok yonlu, mukemmel prompt takibi |

**Ne zaman hangi:**
- Final / kaliteli is → **GPT Image 2** (yuksek kalite, dusunur)
- Hizli / batch / deneme → **Nano Banana 2** (hizli, tutarli)
- Yaratıcı / prompt hassas → **Seedream 4.5** (en iyi prompt takibi)

### Maliyet Kontrol Ayarlari (ONEMLI)

GPT Image 2 ve Nano Banana 2 icin **mutlaka** su ayarlar kullanilmalidir:

| Parametre | Deger | Neden |
|-----------|-------|-------|
| **Resolution** | `1K` | Yuksek cozunurluk maliyeti 3-5x artirir |
| **Quality** | `low` | Standart/High kalite fiyatı cok yukseltir |
| **Aspect Ratio** | `auto` | Model karar versin, ekstra maliyet yok |
| **Format** | `png` | Web icin ideal, ekstra maliyet yok |

**API kullanimi:**
```json
{
  "model": "openai/gpt-image-2-text-to-image",
  "prompt": "...",
  "resolution": "1K",
  "quality": "low",
  "aspect_ratio": "auto",
  "format": "png"
}
```

> **UYARI:** Resolution 2K/4K veya Quality medium/high kullanmak maliyeti **dramatik** artirir.
> Varsayilan ayarlari asla degistirme — ozel durumlar icin kullanici onayi al.

---

### Gorsel Duzenleme (Edit)

| Model | Model ID | Ne yapar |
|-------|----------|----------|
| **Qwen Image Edit** | `qwen-image-edit` | Gorsel duzenleme — referans gorsel + prompt |
| **FLUX 2 Klein Edit** | `wavespeed-ai/flux-2-klein-9b-edit` | Gorsel duzenleme |
| **WAN 2.6 Image Edit** | `alibaba/wan-2.6-image-edit` | Gorsel duzenleme |

---

## VIDEO MODELLERI (3)

| # | Model | Model ID | Aciklama |
|---|-------|----------|----------|
| 1 | **Kling 3.0** | `kwaivgi/kling-v3.0-pro-text-to-video` | Son Kling modeli — ustun kalite ve kontrol |
| 2 | **Kling 2.6** | `kwaivgi/kling-v2.6-pro-text-to-video` | Gercekci video, hassas hareket kontrolu |
| 3 | **Seedance 2.0** | `bytedance/seedance-2.0-text-to-video` | Sinematik + ses uretimi, rejissor kontrolu |

### Gorselden Video (I2V)

| Model | Model ID |
|-------|----------|
| **Kling 3.0 I2V** | `kwaivgi/kling-v3.0-pro-image-to-video` |
| **Seedance 2.0 I2V** | `bytedance/seedance-2.0-image-to-video` |

**Ne zaman hangi:**
- En kaliteli video → **Kling 3.0**
- Gercekci hareket → **Kling 2.6**
- Sinematik + ses → **Seedance 2.0** (ses dahil)

---

## MUZIK VE SES (2)

| # | Model | Model ID | Aciklama |
|---|-------|----------|----------|
| 1 | **Ace Step 1.5** | `wavespeed-ai/ace-step-1.5` | Hizli muzik uretimi |
| 2 | **ElevenLabs V3** | `elevenlabs/eleven-v3` | Seslendirme, TTS |

---

## ARAÇLAR (3)

| # | Ne Icin | Model ID |
|---|---------|----------|
| 1 | **BG kaldir** | `wavespeed-ai/image-background-remover` |
| 2 | **Upscale** | `clarity-ai/crystal-upscaler` |
| 3 | **Reklam videosu** | `wavespeed-ai/ai-video-ads` |

---

## Hizli Referans (Kopyala-Yapistir)

```
GORSEL (KALİTELİ):  openai/gpt-image-2-text-to-image
GORSEL (HIZLI):     google/nano-banana-2-text-to-image
GORSEL (YARATICI):  bytedance/seedream-v4.5
GORSEL EDIT:        qwen-image-edit
VIDEO (EN IYI):     kwaivgi/kling-v3.0-pro-text-to-video
VIDEO (GERCEKCI):   kwaivgi/kling-v2.6-pro-text-to-video
VIDEO (SINEMATIK):  bytedance/seedance-2.0-text-to-video
VIDEO I2V:          bytedance/seedance-2.0-image-to-video
MUZIK:              wavespeed-ai/ace-step-1.5
SES:                elevenlabs/eleven-v3
BG KALDIR:          wavespeed-ai/image-background-remover
UPSCALE:            clarity-ai/crystal-upscaler
```

---

## Reklam Ajansi Senaryolari

### GEO Instagram Post
```
1. Nano Banana 2 → 4 taslak uret (hizli)
2. GPT Image 2 → en iyiyi finalize et
```

### Urun Fotografi → Reel
```
1. BG kaldir → temiz urun
2. Seedance 2.0 I2V → 5s animasyonla (ses dahil)
```

### LinkedIn Carousel (metinli)
```
1. Seedream 4.5 → prompt hassas, baslikli gorseller
```

### Reklam Videosu
```
1. Kling 3.0 → en kaliteli video
2. Ace Step 1.5 → arka plan muzigi
3. ffmpeg ile birlestir
```

### Gorsel Duzenleme
```
1. Mevcut gorseli yukle + prompt ver
2. Qwen Image Edit → duzenle (renk, metin, stil degistir)
```

---

## Hesap Seviyeleri

| Seviye | Gorsel/dk | Video/dk | Aktivasyon |
|--------|-----------|----------|------------|
| Bronze | 2 | 2 | Varsayilan ($1 deneme) |
| Silver | 500 | 500 | $100 |
| Gold | 3.000 | 3.000 | $1.000 |

## Flask API Endpoint'leri

| Endpoint | Fonksiyon |
|----------|-----------|
| `POST /api/wavespeed/generate` | Uret (model + prompt) |
| `GET /api/wavespeed/status/<id>` | Gorev durumu |
| `GET /api/wavespeed/models` | Bu model listesi |

## Error Handling

- 401 → API key yok/yanlis
- 429 → Limit asildi, hesap yukselt
- Task failed → Baska model dene
