# Google Ads Günlük Raporlama Agent'ı
**Botfusions | Customer ID: 3646875139**
**Skill Referansı:** `.agents/skills/paid-ads/SKILL.md` + `.agents/skills/analytics-tracking/SKILL.md`

---

## Nasıl Kullanılır

Bu agent'ı tetiklemek için Claude'a şunu söyle:
> "Google Ads raporunu çek, analiz et ve özetini ver"
> "Son 7 günün performansını göster"
> "Anomali var mı kontrol et"

---

## Agent Görevi Tanımı

```
Sen Botfusions'ın Google Ads performans analistissin.
Önce `.agents/product-marketing-context.md` dosyasını oku.
Ardından `.agents/skills/paid-ads/SKILL.md` ve `.agents/skills/analytics-tracking/SKILL.md` skill'lerini uygula.
```

---

## Rapor Şablonu (paid-ads skill'inden uyarlanmış)

### Günlük Özet Format

```
📊 BOTFUSIONS GOOGLE ADS GÜNLÜK RAPOR
Tarih: [TARİH]
Dönem: Son 7 gün / Bugün
─────────────────────────────────────

💰 HARCAMA
  Bugün:        X TRY
  7 günlük:     X TRY
  Aylık bütçe:  X TRY (kullanım: %X)

📈 PERFORMANS
  Gösterim:     X
  Tıklama:      X
  TO (CTR):     %X
  Ort. TBM:     X ₺
  Dönüşüm:      X ⚠️ (hedef: >0)
  CPA:          X ₺ (hedef: <150 ₺)

🔑 ANAHTAR KELİMELER (Top 5)
  1. [kelime] — X tıklama, X ₺ TBM, X dönüşüm
  2. ...

🚨 ANOMALİLER
  [ ] Harcama >%30 artış (son güne göre)
  [ ] TO %50 düşüş
  [ ] Dönüşüm 0 (>50 tıklama sonrası)
  [ ] Bütçe tükenmiş

💡 ÖNERİLER (paid-ads skill analizi)
  1. ...
  2. ...

📋 AKSIYON GEREKTİREN
  □ [Aksiyon] → [Sorumlu] → [Tarih]
```

---

## Anomali Kuralları (analytics-tracking skill'inden)

| Durum | Eşik | Aksiyon |
|-------|------|---------|
| Harcama artışı | >%30 günlük | Kampanya duraklatma uyarısı |
| Dönüşüm sıfır | >50 tıklama | Landing page + takip kodu kontrol |
| TO düşüşü | <%2 | Reklam metni yenile (ad-creative skill) |
| Tek kelime bütçe hakimiyeti | >%80 | Negative keyword + yeni grup öner |
| Kalite puanı düşük | <5 | ai-seo skill ile landing optimizasyonu |

---

## Mevcut Kampanya Sorunları (Mart 2026 Verisinden)

Mart 2026 raporuna göre acil öncelikler:

### 1. Dönüşüm Takibi Kurulumu (analytics-tracking skill)
```
Hedef URL: botfusions.com/geo-hizmet
İzlenecek olaylar:
  - form_submit (ücretsiz analiz formu)
  - phone_click (+90 850 302 74 60)
  - whatsapp_click
  - scroll_75 (sayfanın %75'i görüldü)

GTM kurulumu için analytics-tracking skill'ini çalıştır.
```

### 2. Keyword Stratejisi Revizyonu (paid-ads skill)
```
Sorun: "yapay zeka SEO" → 108 tıklama, 0 dönüşüm
Neden: Arama niyeti uyuşmuyor (araç arıyor, danışman değil)

Önerilen yeni gruplar:
GRUP A — Yüksek niyet
  + "AI danışmanlık hizmetleri"
  + "yapay zeka pazarlama ajansı"
  + "dijital görünürlük danışmanı"
  - Negatif: "nasıl yapılır", "ücretsiz", "nedir"

GRUP B — GEO farkındalık (eğitim içerikli)
  + "ChatGPT'de marka görünürlüğü"
  + "AI aramalarda nasıl çıkarım"
  + "yapay zeka SEO nedir"
  → Bu grup landing'i eğitim sayfasına yönlendir

GRUP C — Rakip kaçırma
  + "SEO ajansı alternatifi"
  + "yapay zeka SEO ajansı"
  → Botfusions GEO farkını vurgulayan mesaj
```

### 3. Landing Page Mesaj Uyarlaması (copywriting skill)
```
"yapay zeka SEO" arayan kişiye özel:
  H1: "Yapay Zeka SEO'dan Fazlası: ChatGPT'de Görün"
  Alt başlık: SEO bitti demiyoruz — ama artık yetmez.
  CTA: "GEO Nedir? Ücretsiz Rehber Al"
```

---

## Otomatik Rapor Pipeline (Composio ile)

```
Her sabah 09:00 (Türkiye saati):
  1. Google Ads MCP → son 24 saat veri
  2. Anomali kontrol (yukarıdaki kurallar)
  3. GEMINI_GENERATE_TEXT → rapor özeti yaz
  4. GMAIL → cenk@botfusions.com'a gönder
  5. GOOGLESHEETS → rapor satırı ekle
     Sheet: 12mEFOJTUOMA5W5Eh2kKWkYcvJeA5KB5hcXYLaWW1_bg
```

**Kurulum için:** Google Ads MCP bağlantısı gerekli.
`04-araclar/add-google-ads-mcp.ps1` dosyasını çalıştır → Claude Desktop yeniden başlat.

---

## Haftalık Strateji Toplantısı Şablonu

Her Pazartesi Claude'a sor:
> "Geçen haftanın Google Ads raporunu çek, paid-ads skill ile analiz et, bu haftaki aksiyonları listele ve Google Sheets'e kaydet"

---

*Botfusions AI Reklam Ajansı | paid-ads + analytics-tracking skill entegrasyonu*
