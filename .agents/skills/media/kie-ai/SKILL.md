---
name: kie-ai
description: "Kie.ai — Birlesik AI API gateway. Nano Banana Pro, Kling 3.0, Sora 2 Pro, Veo 3.1, GPT Image tek API anahtari ile. En uygun fiyatli erisim."
argument-hint: "image | video | upload | status <prompt>"
version: 1.0.0
license: MIT
---

# Kie.ai — Birlesik AI API Gateway

Birden fazla AI modeline tek API anahtari ile erisim. Replicate ve Fal.ai'ye ucuz alternatif.

## When to Activate

TRIGGER when the user:
- API uzerinden gorsel/video uretmek istediginde
- Maliyet optimize etmek istediginde ("en ucuz", "maliyet dusur")
- Kie pipeline kullanmak istediginde
- "kie" veya "kie.ai" dediginde
- Batch gorsel uretiminde maliyet kontrolu gerektiginde

## Mevcut Modeller

### Gorsel Modelleri

| Model | Saglayici | Maliyet | En Iyi |
|-------|-----------|---------|--------|
| **Nano Banana** | Google AI Studio | ~$0.04 | Hizli, dengeli |
| **Nano Banana** | Kie AI | $0.09 | API uzerinden |
| **Nano Banana Pro** | Google AI Studio | ~$0.13 | Yuksek kalite |
| **Nano Banana Pro** | Kie AI | $0.09 | En uygun fiyat |
| **GPT Image 1.5** | WaveSpeed | ~$0.07 | Hizli ve ucuz |
| **Flux.1 Kontext** | BFL | - | Tutarli sahne |
| **4o Image API** | OpenAI | - | Yuksek sadakat |

### Video Modelleri

| Model | Saglayici | Maliyet | En Iyi |
|-------|-----------|---------|--------|
| **Kling 3.0** | Kie AI | ~$0.30 | Image-to-video, 3-15s |
| **Sora 2 Pro** | Kie AI | ~$0.30 | 10-15s video |
| **Veo 3.1** | Google AI Studio | ~$0.50 | Sinematik + ses |
| **Runway Aleph** | Runway | - | Coklu duzenleme |

### Muzik

| Model | Ozellik |
|-------|---------|
| **Suno** | V3.5, V4, V4.5 — Gercekci vokal, 8 dk'ya kadar |

## API Kullanimi

**Endpoints:**
- Gorev olustur: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Durum sorgula: `GET https://api.kie.ai/api/v1/jobs/recordInfo?taskId=TASK_ID`
- Dosya yukle: `POST https://kieai.redpandaai.co/api/file-stream-upload`

**Auth:** `Authorization: Bearer KIE_API_KEY`
**Ortam Degiskeni:** `KIE_API_KEY`

### Async Is Akisi
```
1. createTask → taskId al
2. recordInfo'yu poll et (waiting → success/fail)
3. Sonuc URL'sini al
```

### Ornek: Gorsel Uretim
```bash
curl -X POST https://api.kie.ai/api/v1/jobs/createTask \
  -H "Authorization: Bearer $KIE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nano-banana-pro",
    "prompt": "Professional product photography...",
    "aspect_ratio": "1:1"
  }'
```

### Ornek: Video Uretim
```bash
curl -X POST https://api.kie.ai/api/v1/jobs/createTask \
  -H "Authorization: Bearer $KIE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "kling-3.0",
    "image_url": "https://...",
    "prompt": "Slow zoom in, cinematic lighting",
    "duration": 5
  }'
```

## Proje Entegrasyonu

### Mevcut Pipeline
```
creative-engine-template/
├── tools/
│   ├── providers/kie.py      ← Kie AI saglayici
│   ├── kie_upload.py          ← Dosya yukleme
│   └── config.py              ← Maliyet matrisi
├── references/docs/
│   └── kie-ai-api.md          ← Tam API referans
```

### Maliyet Karsilastirma

| Islem | Google AI Studio | Kie AI | Tasarruf |
|-------|-----------------|--------|----------|
| Nano Banana Pro | $0.13 | $0.09 | %31 |
| Kling 3.0 Video | - | $0.30 | - |
| Sora 2 Pro Video | - | $0.30 | - |

## Reklam Ajansi Kullanimi

### Urun Fotografi → Video
```
1. Nano Banana Pro ile urun sahnesi uret ($0.09)
2. Kling 3.0 ile videoye animasyonla ($0.30)
3. Toplam: ~$0.39/reklam
```

### Toplu Uretim
```
1. 50 urun gorseli (Nano Banana Pro): $4.50
2. En iyi 10'u videoye cevir (Kling 3.0): $3.00
3. Toplam: $7.50 — 50 gorsel + 10 video
```

## Error Handling

- Gorev basarisiz → 3 kez tekrar dene, farkli model oner
- API timeout → 60s bekle, tekrar sorgula
- Dosya yukleme hatasi → dosya boyutunu kontrol et (max 10MB)
- Kredi yetersiz → kullanicibilgi ver

## Best Practices

### DO
- Toplu uretimde Kie API kullan (ucuz)
- Nano Banana Pro icin Kie'yi sec ($0.09 vs $0.13)
- Video uretimi icin once gorsel olustur, sonra animasyonla
- creative-engine-template pipeline'ini kullan

### DON'T
- Tek gorsel icin Kie kullanma (Google AI Studio daha ucuz olabilir)
- Maliyet matrisini kontrol etmeden batch baslama
- Video uretiminde uzun prompt kullanma (5-15s sinirla)
