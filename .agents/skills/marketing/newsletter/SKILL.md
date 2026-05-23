---
name: newsletter
description: E-posta bulletin ve newsletter yonetimi. Icerik plani, tasarim, gonderim takvimi, acilma/oran optimizasyonu.
version: 1.0.0
author: Botfusions AI Reklam Ajansi
category: marketing
---

# Newsletter & Email Bulletin Skill

## When to Activate

**Trigger words:** newsletter, e-bulletin, email pazarlama, acilma orani, click rate, segmentasyon, subject line, email kampanya, bulletin, abone yonetimi

**Use when:**
- Planning newsletter content and schedule
- Optimizing open rates and click rates
- Segmenting subscriber lists
- Designing email templates

---

## Pipeline Architecture

```
HEDEF KITLE → [1. CONTENT CURATION] → [2. SUBJECT LINE] → [3. DESIGN & TEMPLATE]
           → [4. SEGMENT] → [5. SEND] → [6. ANALYZE] → [7. OPTIMIZE]
```

---

## Implementation

### Phase 1: Content Curation

| Tip | Oran | Aciklama |
|-----|------|----------|
| Egitim | 40% | Sektorel bilgi, ipuclari, rehberler |
| Urun/hizmet | 25% | Yeni ozellik, guncelleme, kampanya |
| Sosyal kanit | 15% | Case study, musteri yorumu |
| Topluluk | 10% | Etkinlik, haber, sektor guncel |
| Satis CTA | 10% | Direkt urun onerisi, demo talebi |

**Secim kriterleri:** Acik deger sunuyor mu? Marka uyumlu mu? Aksiyon cagiriyor mu? Oncekinden farkli mi?

### Phase 2: Subject Line Optimization

**Formul:** `[Kisisellestirme] + [Merak/Tarik] + [Deger Vaadi]`

**A/B Test eksenleri:** Kisisellestirmeli vs degil, kisa (<30 karakter) vs uzun, emoji vs emojisiz, urgency vs curiosity

| Metrik | Iyi | Ortalama | Kotu |
|--------|-----|----------|------|
| Open Rate | >25% | 15-25% | <15% |
| Click Rate | >4% | 2-4% | <2% |
| Unsubscribe | <0.3% | 0.3-0.5% | >0.5% |

### Phase 3: Design & Template

**Tasarim ilkeleri:** Mobil-first (%60+ mobil), tek kolon (600px max), gorsel/metin 40/60, CTA butonu min 44x44px

**Sablon yapisi:** Logo/Header → Hero Gorsel → Icerik Blogu (baslik + ozet + CTA) → Sosyal Kanit → Ana CTA → Footer/Unsub

**Dark mode:** Logo beyaz cerceveli veya SVG, butonlara inverted color yedegi, yuksek kontrast metin

### Phase 4: Segmentation

| Kriter | Ornek |
|--------|-------|
| Demografik | Sektor, sirket buyuklugu, unvan |
| Davranis | Son acma, son tiklama, satin alma |
| Engagement | Aktif, pasif, yeni, risk altinda |
| Pipeline stage | Awareness, consideration, decision |

**Kisisellestime:** {{isim}}, {{sirket}}, {{son_icerik}}, {{sehir}}

### Phase 5: Send & Schedule

**En iyi saatler:** Sali 10-11, Persembe 14-15, Carsamba 09-10 (B2B)

**Delivery checklist:** Spam test (>8 skor), mobil test, link kontrol, personalization dogrulama, unsubscribe link, ALT metinler

### Phase 6: Analyze & Optimize

**Analiz dongusu:** Gonder → 24s bekle → ilk metrikler → 48s final metrikler → segment karsilastir → hipotez olustur

**Optimizasyon:** Open dusuk → subject line + saat / Click dusuk → CTA konumu + deger / Unsubscribe yuksek → frekans + segment / Bounce yuksek → list temizligi

---

## Error Handling

| Sorun | Cozum |
|-------|-------|
| Spam klasoru | DNS kayitlari (SPF/DKIM) kontrol et |
| Yuksek bounce | List temizligi yap, gecersiz adresleri sil |
| Dusuk open rate | A/B test ile subject line optimize |
| Mobil bozukluk | Responsive sablon test zorunlu |
| Unsubscribe patlamasi | Frekansi azalt, segment ayarla |

---

## Best Practices

**DO:** Her gonderimde A/B subject line testi, aylik liste temizligi, welcome series ile yeni abone bagla, preheader text optimize et, CTA'yı en ustte gorunur yap.

**DON'T:** Haftada 2'den fazla gonderim, sadece gorsel email (spam riski), satin alma listesi kullanma, unsubscribe gizleme, her mailde ayni sablon.

---

## Inputs / Outputs

**Inputs:** `product-marketing-context.md`, abone listesi/segment verileri, gonderim platformu, onceki performans verileri

**Outputs:** Newsletter takvimi, A/B test sonuclari, HTML sablonlar, segment performans raporu, optimizasyon onerileri
