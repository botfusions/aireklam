---
name: video-marketing
description: Video pazarlama stratejisi. Platform bazli video plani, storyboard, icerik takvimi, performans olcum.
version: 1.0.0
author: Botfusions AI Reklam Ajansi
category: marketing
---

# Video Marketing Skill

## When to Activate

**Trigger words:** video pazarlama, video strateji, storyboard, YouTube, TikTok, Reels, LinkedIn video, video uretim, Remotion, Krea video

**Use when:**
- Planning video content for any platform
- Creating storyboards or video scripts
- Setting up a video production pipeline
- Measuring video campaign performance

---

## Pipeline Architecture

```
BRIEF → [1. PLATFORM STRATEJISI] → [2. ICERIK PLANI] → [3. STORYBOARD]
     → [4. PRODUKSIYON] → [5. DAGITIM] → [6. OLCUM & OPTIMIZASYON]
```

---

## Implementation

### Phase 1: Platform Strategy

| Platform | Format | Sure | Best For |
|----------|--------|------|----------|
| YouTube | 16:9 / Shorts | 30s-15dk | Uzun kuyruklu erisim |
| TikTok | 9:16 | 15-60s | Genc kitle, trend |
| Instagram Reels | 9:16 | 15-90s | Gorsel marka, urun |
| LinkedIn | 1:1 / 16:9 | 30s-5dk | B2B, dijital pazarlama |
| Facebook | 16:9 / 9:16 | 15-60s | Genis kitle, retargeting |

**Hedef kitle:** Demografik, izleme aliskanliklari, icerik tercihi, donusum davranisi.

### Phase 2: Content Plan

**Content pillar'lari:** Egitim (%30), Sosyal kanit (%25), Marka (%25), Urun (%20)

**Frekans:** YouTube 1-2/hafta, TikTok 3-5/hafta, Reels 3-4/hafta, LinkedIn 1-2/hafta

**Haftalik takvim:** Pzt → Egitim (YouTube), Car → Kisa icerik (Reels+TikTok), Cum → Case study

### Phase 3: Storyboard & Script

**Hook-Agitate-Solution-CTA formati:**
1. **Hook (0-3s):** Dikkat cekici acilis soru/iddia
2. **Agitate (3-10s):** Sorunu derinlestir
3. **Solution (10-25s):** Urun/hizmet cozumu
4. **CTA (25-30s):** Net aksiyon cagrisi

**Storyboard:** Sahne | Sure | Gorsel | Metin/SES | Aksiyon — seklinde tablo ile planla.

### Phase 4: Production Pipeline

- **Remotion** (`04-araclar/remotion-kaynak`): `python render.py --template <sablon> --data <icerik.json>`
- **Krea.ai:** Kling, Veo, Hailuo, Wan modeller — 9:16 / 16:9 / 1:1
- **Kie.ai:** Gorsel uretimi + YouTube thumbnail

**Uretim checklist:** Storyboard onay > Script yazildi > Gorsel hazir > Render > Thumbnail > Altyazi

### Phase 5: Distribution

- YouTube: baslik, aciklama, etiket, thumbnail, playlist
- TikTok: hashtag, ses, etkilesim CTA
- Reels: hashtag, konum, etiketleme
- LinkedIn: makale linki, hashtag, yorum CTA

### Phase 6: Performance Metrics

| Metrik | Hedef | Kritik Esik |
|--------|-------|-------------|
| Watch time | >50% | <30% = sorun |
| CTR (thumbnail) | >4% | <2% = degistir |
| View-to-action | >2% | <1% = optimize |
| Retention drop (ilk 3s) | <20% | >40% = hook zayif |
| Share rate | >1% | <0.3% = icerik degis |

---

## Error Handling

| Sorun | Cozum |
|-------|-------|
| Dusuk izlenme | A/B thumbnail/baslik testi yap |
| Yuksek drop-off | Ilk 3s hook'u yeniden yaz |
| Format uyumsuzlugu | Platform spec tablosu ile kontrol |
| Remotion render hatasi | JSON schema dogrula |
| Dusuk uretim hizi | Sablon kutuphanesi kur |

---

## Best Practices

**DO:** A/B thumbnail testi, ilk 3s maksimum dikkat, her platforma ozel format, 3 format kaydet (1:1, 16:9, 9:16), altyazi ekle.

**DON'T:** Ayni videoyu her yere yukleme, CTA'siz yayimlama, hook atlama, thumbnail'i son dakika yapma.

---

## Inputs / Outputs

**Inputs:** `product-marketing-context.md`, platform hedefleri/KPI, butce, hedef kitle verileri

**Outputs:** Video takvimi, storyboard dosyalari, video dosyalari (`03-videolar/`), performans raporu
