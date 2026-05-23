---
name: krea-ai
description: "Krea.ai — 64+ AI modeli tek platformda. Gorsel, video, upscale, LoRA egitim, 3D. Reklam ajansi icin tam yaratici suite."
argument-hint: "image | video | enhance | train | batch | pipeline <prompt>"
version: 1.0.0
license: MIT
---

# Krea.ai — AI Yaratıcı Suite

64+ AI modeli tek abonelikte: Flux, Imagen, GPT Image, Ideogram, Seedream, Nano Banana Pro, Veo, Kling, Sora ve daha fazlasi.

## When to Activate

TRIGGER when the user:
- Gorsel olusturmak istediginde ("gorsel uret", "resim olustur", "image generate")
- Video olusturmak istediginde ("video uret", "reklam videosu")
- Gorsel kalite artirmak istediginde ("kalite yukselt", "upscale", "enhance")
- Marka stili egitmek istediginde ("LoRA egit", "marka stili olustur")
- Urun fotografi istediginde ("urun foto", "product shot")
- Toplu gorsel uretimi istediginde ("50 varyasyon", "batch gorsel")

## Platform Ozellikleri

### Gorsel Modelleri (20+)

| Model | CU | Sure | En Iyi |
|-------|-----|------|--------|
| **z-image** | 3 | 5s | En hizli taslak |
| **Flux** | 5 | 5s | Genel kullanim, LoRA destekli |
| **Imagen 4 Fast** | 16 | 17s | Hizli Google modeli |
| **Ideogram 3** | 54 | 18s | Metin/typografi iceren gorseller |
| **Seedream 4** | 24 | 20s | Fotorealistik |
| **Nano Banana Pro** | 119 | 30s | Ustun fotorealizm |
| **GPT Image** | 184 | 60s | En yuksek kalite, karmasik kompozisyon |

### Video Modelleri (7)

| Model | CU | En Iyi |
|-------|-----|--------|
| **Hailuo 2.3** | low | Hizli, yumusak hareket |
| **Kling 2.5** | med | Gercekci fizik (varsayilan) |
| **Veo 3** | 608+ | Sinematik + ses uretimi |
| **Veo 3.1** | varies | En kaliteli video |
| **Wan 2.5** | 569 | Stil kontrolu |

### Enhance/Upscale (3)

| Model | Max Cozunurluk | En Iyi |
|-------|---------------|--------|
| **Topaz** | 22K | Sadik buyutme |
| **Topaz Generative** | 16K | Yaratici detay ekleme |
| **Topaz Bloom** | 10K | Maksimum yaratici detay |

## Reklam Ajansi Pipeline

### Taslak → Final Akisi
```
1. Flux ile 4-8 taslak uret (5 CU/adet, 5s)
2. En iyi 2-3 taslagi sec
3. Nano Banana Pro ile finalize et (119 CU, 30s)
4. Topaz ile 4K upscale (51 CU)
5. Google Sheets'e kaydet
```

### Urun Fotografi Pipeline
```
1. Urun goruntusu al
2. GPT Image ile 10 yasam tarzi sahnesi olustur
3. En iyi 4'ü Kling/Veo ile videoye animasyonla
4. Topaz ile 4K'e cikar
```

### Video Reklam Pipeline
```
1. 6 sahne storyborad olustur (Nano Banana Pro)
2. Her sahneyi Veo 3 ile 5s animasyonla (+ ses)
3. ffmpeg ile birlestir (30s reklam)
4. Topaz ile upscale
```

## API Kullanimi

**Endpoint:** `https://api.krea.ai`
**Auth:** `Authorization: Bearer KREA_API_TOKEN`
**Ortam Degiskeni:** `KREA_API_TOKEN`

### Gorsel Uretim
```bash
# Taslak
uv run krea-ai generate --model flux --prompt "..." --aspect-ratio 1:1

# Final
uv run krea-ai generate --model nano-banana-pro --prompt "..." --aspect-ratio 16:9

# Batch
uv run krea-ai generate --model flux --prompt "..." --batch-size 4
```

### LoRA Egitim
```bash
# Marka stili egit
uv run krea-ai train --images ./brand-assets/ --type style --trigger-word "botfusions"

# LoRA ile uret
uv run krea-ai generate --model flux --style-id STYLE_ID --style-strength 1.0 --prompt "..."
```

## Fiyatlandirma

| Plan | Aylik CU | Fiyat | Onemli |
|------|---------|-------|--------|
| Free | 100/gun | $0 | Sinirli model |
| Basic | 5,000 | ucretli | Ticari lisans, 4K upscale |
| Pro | 20,000 | ucretli | Tum video modelleri, 8K |
| Max | 60,000 | ucretli | Sinirsiz LoRA, 22K |

## Reklam Format Destegi

| Platform | Format | En Iyi Model |
|----------|--------|-------------|
| Instagram Feed | 1:1 (1080x1080) | Flux / Nano Banana Pro |
| Instagram Story | 9:16 (1080x1920) | Nano Banana Pro |
| Facebook | 16:9 (1200x628) | GPT Image |
| TikTok | 9:16 (1080x1920) | Nano Banana Pro |
| YouTube | 16:9 (1920x1080) | GPT Image |
| Display | 300x250, 728x90 | Ideogram 3 (metinli) |

## Error Handling

- API rate limit → 30s bekle, tekrar dene
- Model yok → alternatif model oner (Flux → Seedream → Nano Banana Pro)
- LoRA egitim basarisiz → gorsel sayisini azalt, tekrar dene
- CU yetersiz → kullanicidan plan yukseltme iste

## Best Practices

### DO
- Taslak icin Flux, final icin Nano Banana Pro / GPT Image kullan
- Reklam metni iceren gorseller icin Ideogram 3 sec
- Marka tutarliligi icin LoRA egit
- Video icin once gorsel storyborad olustur
- Batch uretimde seed kullan (tekrar edilebilirlik)

### DON'T
- Taslak icin GPT Image kullanma (pahali)
- LoRA olmadan marka gorseli uretme
- Video uretirken reference image kullanmamak
- Topaz Bloom'u urun fotograflarinda kullanma (az detay ekler)
