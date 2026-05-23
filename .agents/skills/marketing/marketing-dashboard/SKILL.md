---
name: marketing-dashboard
description: "Gunluk/haftalik pazarlama performans dashboard'u. Spend, donusum, ROAS, CAC, kanal karsilastirmasi, anomali tespiti tek ekranda. Google Ads MCP + GA4 + Sheets entegrasyonu."
argument-hint: "daily | weekly | anomaly | setup | kpi"
version: 2.0.0
license: MIT
---

# Marketing Dashboard — CMO Performans Paneli

CMO'nun her sabah gordugu tek ekran: Harcama, donusum, ROAS, CAC, kanal karsilastirmasi, anomali uyarilari.

## When to Activate

TRIGGER when the user:
- "Dashboard kur", "rapor lazim", "gunluk rapor" dediginde
- "ROAS kac?", "CAC ne durumda?", "KPI takibi" istediginde
- "Kanal karsilastirma yap", "hangi kanal ne getirdi" sordugunda
- "Anomali tespiti", "harcama artis", "donusum dusus" dediginde
- Her pazartesi sabahi otomatik haftalik rapor icin
- Yeni bir kampanya baslatildiginda takip icin

## Pipeline Architecture

```
[Veri Kaynaklari]
  Google Ads (GAQL/MCP) ─┐
  Meta Ads (API/CSV) ─────┤
  GA4 (Data API) ─────────┼──→ Tarih Bazli Birlestir → KPI Hesapla
  GSC (Search API) ───────┤                              │
  Email (Export) ──────────┘                 ┌────────────┴────────────┐
                                             ▼                         ▼
                                      Sheets/Looker              Gmail/Slack Uyari
```

---

## Core KPI'lar

### Temel Metrikler

| KPI | Formul | Hedef | Kirmizi Esik |
|-----|--------|-------|-------------|
| **ROAS** | Gelir / Reklam Harcamasi | > 4x | < 2x |
| **CAC** | Toplam Harcama / Yeni Musteri | < LTV / 3 | > LTV / 2 |
| **CPA** | Harcama / Donusum | Platform bazli | Hedefin 2x |
| **CVR** | Donusum / Tiklama | > %3 | < %1 |
| **CTR** | Tiklama / Gosterim | > %2 | < %0.5 |
| **Spend Pace** | Harcama / Gecen Gun * Toplam Gun | Butce ±%10 | ±%20 |
| **MER** | Toplam Gelir / Toplam Pazarlama | > 3x | < 1.5x |

### Kanal Bazli Metrikler

| Kanal | Takip Edilen | Veri Kaynagi |
|-------|-------------|-------------|
| Google Ads | Spend, Tiklama, Donusum, ROAS, TO | Google Ads MCP (GAQL) |
| Meta Ads | Spend, Gosterim, Donusum, CPM | Meta API / CSV |
| GA4 | Oturum, Bounce, Donusum, Kanal | GA4 Data API |
| GSC | Gosterim, Tiklama, Pozisyon, CTR | GSC API |
| Email | Acilma, Tiklama, Donusum | ESP Export |

---

## Google Ads MCP Entegrasyonu

### Gunluk Veri Cekme (GAQL)

```sql
-- Son 7 gun kampanya performansi
SELECT
  campaign.name,
  campaign.status,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros / 1000000 AS cost_try,
  metrics.conversions,
  metrics.conversion_value,
  metrics.ctr,
  metrics.average_cpc
FROM campaign
WHERE segments.date DURING LAST_7_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

### Anomali Sorgulama

```sql
-- Bugun vs 7 gun ortalamasi karsilastirma
SELECT
  campaign.name,
  metrics.cost_micros / 1000000 AS today_cost,
  metrics.conversions AS today_conversions
FROM campaign
WHERE segments.date = TODAY
```

---

## Dashboard Template (Google Sheets)

### Sayfa Yapisi

**Satir 1:** Baslik + Tarih araligi secici
**Satir 2:** KPI Kartlari (Spend | Revenue | ROAS | CAC | CVR | Leads)
**Satir 3:** Kanal Karsilastirma Tablosu
**Satir 4:** Trend Grafigi (7/30 gun)
**Satir 5:** Anomali Uyarilari (kirmizi/sari/yesil)
**Satir 6:** En Iyi / En Kotu Performing Kampanya
**Satir 7:** Aksiyon Maddeleri

### KPI Kart Formati

```
┌─────────────────────────┐
│  ROAS        ↑ %12      │
│  4.2x                   │
│  Hedef: >4x   ● YESIL   │
│  Gecen Hafta: 3.8x      │
└─────────────────────────┘
```

---

## Anomali Tespiti

| Anomali Tipi | Esik | Aksiyon |
|-------------|------|---------|
| `spend_increase` | 7 gun ort. ustunde %30+ | Butce kontrol et, negatif kelime ekle |
| `conversion_drop` | 7 gun ort. altinda %40+ | Landing page kontrol, takip dogrula |
| `cpc_spike` | 7 gun ort. ustunde %50+ | Rakip aktivitesi kontrol, bid ayarla |
| `roas_below` | < 2.0 esigi | Kampanyayi durdur, analyze et |
| `ctr_decline` | 7 gun ort. altinda %30+ | Kreatif yenile, headline test et |
| `impression_drop` | 7 gun ort. altinda %50+ | Hesap durumu kontrol, budget check |

### Anomali Uyari Format

```
⚠️ ANOMALI TESPITI
Tarih: 2026-04-11
Kampanya: GEO_Hizmet_Search
Metrik: Harcama
Deger: 245 TRY (7 gun ort: 150 TRY)
Degisim: +%63
Oneri: Butce %99 tek kelimede, yeni kelime grubu ekle
```

---

## Haftalik Rapor Yapisi

### 1. Ozet KPI'lar

| Metrik | Bu Hafta | Gecen Hafta | Degisim | Hedef | Durum |
|--------|----------|-------------|---------|-------|-------|
| Harcama | | | | | |
| Donusum | | | | | |
| ROAS | | | | | |
| CPA | | | | | |
| CTR | | | | | |
| CVR | | | | | |

### 2. Kanal Performansi

| Kanal | Harcama | Donusum | ROAS | CPA | Not |
|-------|---------|---------|------|-----|-----|
| Google Ads | | | | | |
| Meta Ads | | | | | |
| Toplam | | | | | |

### 3. En Iyi / En Kotu

| En Iyi 3 Kampanya | Neden |
|--------------------|-------|
| | |

| En Kotu 3 Kampanya | Sorun | Aksiyon |
|--------------------|-------|---------|
| | | |

### 4. Aksiyon Maddeleri

- [ ] ...
- [ ] ...

---

## Looker Studio Entegrasyonu

1. Google Sheets'i veri kaynagi olarak bagla (otomatik guncel)
2. GA4 dogrudan bagla (gercek zamanli)
3. Google Ads dogrudan bagla
4. Tarih bazli blend yap
5. Widget'lar: Scorecard, Time Series, Pie Chart, Tablo (kosullu format), Bar Chart

---

## Botfusions Mevcut Dashboard Durumu

| Veri Kaynagi | Durum | Aksiyon Gerekli |
|-------------|-------|----------------|
| Google Ads | Aktif (MCP) | GAQL sorgularini otomatiklestir |
| GA4 | Kurulmadi | Analytics-tracking skill ile kur |
| GSC | Kurulmadi | API erisimi al |
| Meta Ads | Kurulmadi | Henuz aktif degil |
| Sheets | Aktif | Dashboard template olustur |

### Oncelikli Dashboard
1. Google Ads + Sheets → Gunluk dashboard
2. GA4 eklenince → Performans dashboard
3. Meta Ads baslayinca → Coklu kanal dashboard

---

## Error Handling

| Hata | Cozum |
|------|-------|
| API limit / auth hatasi | Backoff ile tekrar dene, Slack ile uyari |
| Tarih uyumsuzlugu | UTC+3 (Turkiye) standardina zorla |
| Donusum eksik | `analytics-tracking` skill ile dogrula |
| Eski veri | Veri kaynagini yenile |
| Anomali false positive | Mevsimsellik baseline ekle |

## Best Practices

### DO
- Is sorusuyla basla, veriyle degil ("Hangi kanal en cok donusum getirdi?")
- Pazartesi-Pazar haftasi kullan (Turkiye)
- Kosullu format ekle (yesil=kirmizi=sari=uyari)
- Veri toplamayi otomatiklestir
- Onceki donem karsilastirmasi ekle

### DON'T
- Vitayn metrikleri takip etme ("gosterim" tek basina anlamsiz)
| Cok karmasik dashboard yapma (max 7 widget)
| Farkli atif modellerini karistirma
| Veri kalitesini atlayip gorsellestirmeye atlama

## Related Skills
- **analytics-tracking** — Dashboard icin veri toplama
- **paid-ads** — Kampanya optimizasyonu
- **ab-test-setup** — Dashboard'da test takibi
- **attribution-modeling** — Coklu dokunma atif
