---
name: attribution-modeling
description: Pazarlama atif modelleme. Son tiklama, ilk tiklama, coklu dokunma, veri odakli atif ile hangi kanalin ne getirdigini olcme.
version: 1.0.0
author: Botfusions AI Reklam Ajansi
category: marketing
---

# Attribution Modeling Skill

## When to Activate

**Trigger words:** atif modelleme, attribution, son tiklama, ilk tiklama, multi-touch, coklu dokunma, kanal ROI, donusum yolu, butce dagitimi, data-driven attribution

**Use when:**
- Measuring which marketing channel drives conversions
- Deciding budget allocation across channels
- Analyzing customer conversion paths
- Comparing attribution models

---

## Pipeline Architecture

```
VERI TOPLAMA → [1. DATA COLLECTION] → [2. MODEL SELECTION] → [3. PATH ANALYSIS]
            → [4. CHANNEL VALUATION] → [5. BUDGET OPTIMIZATION]
```

---

## Implementation

### Phase 1: Data Collection

**Veri kaynaklari:**

| Kaynak | Veri Tipi | Arac |
|--------|-----------|------|
| GA4 | Web event, conversion | Google Analytics |
| Google Ads | Tiklama, harcama, donusum | Google Ads MCP |
| Meta Ads | Impression, click, action | Meta API |
| CRM | Firsat, kazanim, kayip | HubSpot/Salesforce |
| Email | Open, click, donusum | Mail platform API |

**UTM standardi:** `utm_source` (kanal), `utm_medium` (tip), `utm_campaign` (adi), `utm_content` (varyasyon), `utm_term` (keyword)

**Event tracking:** Page view, form submit, CTA click, video events, purchase, offline conversion import

### Phase 2: Model Selection

| Model | Mantik | Best For |
|-------|--------|----------|
| **Last-click** | Son dokunma %100 | Direkt Response, SEM |
| **First-click** | Ilk dokunma %100 | Brand awareness |
| **Linear** | Esit dagitim | Genel bakis |
| **Time-decay** | Son dokunma agirlikli | Uzun satis donguleri |
| **Position-based** | Ilk+son %40, orta %20 | B2B, funnel analizi |
| **Data-driven** | Algoritma tabanli | Buyuk hesaplar (>5000 donusum/ay) |

**Secim kararcisi:** <500 donusum → Position-based / 500-5000 → Time-decay vs Position-based / >5000 → Data-driven

### Phase 3: Path Analysis

```
Ornek yol: Organic → Retargeting → Email → Branded Search → CONVERT
Last-click:    15%       10%        15%         60%
Data-driven:   30%       15%        20%         35%
```

**Metrikler:** Path length (B2B: 5-12, B2C: 2-4), Time to convert (gun), Assisted conversions, Top 10 paths

**Drop-off:** Impressions → Clicks (-40%) → Landing (-30%) → Form Start (-50%) → Complete (-20%) → Sale

### Phase 4: Channel Valuation

| Kanal | Harcama | Donusum | CPA | ROAS | Atif Degeri |
|-------|---------|---------|-----|------|-------------|
| Google Search | TBD | TBD | TBD | TBD | TBD |
| Meta Ads | TBD | TBD | TBD | TBD | TBD |
| LinkedIn | TBD | TBD | TBD | TBD | TBD |
| Email | TBD | TBD | TBD | TBD | TBD |
| Organic | TBD | TBD | TBD | TBD | TBD |

**ROI:** ROAS = Donusum Degeri / Harcama | CAC = Harcama / Yeni Musteri | LTV/CAC hedef: >3x

**Assist orani yuksek kanal → ust funnel degeri var. Sadece last-click bakilirsa butce yanlis kesilir.**

### Phase 5: Budget Optimization

**Prensipler:** Mevcut dagitimi analize et → Marginal ROI hesapla → Dusuk ROI azalt / Yuksek ROI arttir → Kanali tamamen kapatma → Tek seferde max %20 degisiklik

**Dongu:** Hafta 1-2 veri toplama → Hafta 3 atif modeli → Hafta 4 butce ayari → Hafta 5-6 olcum → Tekrarla

**Tavan/kurallar:** Tek kanal max %60, test kanallari min %10, brand search min %15

---

## Error Handling

| Sorun | Cozum |
|-------|-------|
| Eksik conversion verisi | `analytics-tracking` skill ile kur |
| Cross-device farki | User-ID / logged-in tracking ekle |
| Offline donusum eksik | CRM entegrasyonu + offline import |
| Model celiskisi | Unified reporting dashboard kur |
| Dusuk veri hacmi | Position-based model ile basla |

---

## Best Practices

**DO:** En az 2 modeli karsilastir, UTM'yi standart kullan, assisted conversion raporla, %20 kuraliyla kademeli degistir, aylik rapor olustur.

**DON'T:** Sadece last-click ile butce dagit, farkli platform metriklerini direkt karsilastirma, dusuk veriyle data-driven secme, butceyi dramatik degistir, kanali tamamen silme.

---

## Inputs / Outputs

**Inputs:** `product-marketing-context.md`, GA4/Google Ads erisimi, mevcut butce dagitimi, donusum verileri (min 30 gun)

**Outputs:** Atif modeli karsilastirma raporu, channel valuation matrisi, butce yeniden dagitim onerisi, path analysis, aylik rapor sablonu
