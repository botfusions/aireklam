# PRD — Botfusions Ana Sayfa Revize
**Tarih:** 30 Nisan 2026 | **Versiyon:** 1.0 | **Hazırlayan:** Botfusions

---

## Özet
botfusions.com ana sayfası SEO audit bulgularına göre revize edilecek. Mevcut tasarım ve renk paleti korunacak, eksik bölümler eklenecek, varsayılan dil Türkçe olacak. Landing page (/geo-hizmet) değişmeyecek.

---

## Kapsam Dışı
- `/geo-hizmet` landing page → **dokunulmayacak**
- Backend / API değişikliği → yok
- Renk paleti → **aynı kalacak** (#A855F7, #7C3AED, #3B82F6, #F97316)

---

## Değişmeyecek Bölümler (Mevcut, İyi Durumda)
- Hero animasyonu ve CTA
- GEO monitoring dashboard (8/8 engines)
- Command Center for AI Visibility
- GEO Checker aracı (navbarda)
- FAQ accordion + FAQPage Schema
- Footer yapısı
- Tüm Schema markup'lar (Organization, HowTo, SoftwareApplication, FAQPage)

---

## 1. Dil Yapısı — TR Varsayılan, EN İkincil

**Mevcut:** Site tamamen İngilizce  
**Hedef:** Türkçe varsayılan, İngilizce ikincil dil

### Uygulama
```
/ (root)          → TR içerik (varsayılan)
/en               → EN içerik (mevcut içerik buraya taşınır)
```

- `<html lang="tr">` ana sayfada
- `<link rel="alternate" hreflang="en" href="/en">`
- `<link rel="alternate" hreflang="tr" href="/">`
- Nav'daki "EN" butonu → "TR / EN" toggle olacak
- Tüm meta tag, title, description → Türkçe versiyonu oluşturulacak

### Türkçe Title & Meta (Öncelik 1)
```html
<title>Botfusions | AI Ajan & GEO Hizmetleri — Türkiye'nin Öncü AI Ajansı</title>
<meta name="description" content="ChatGPT, Gemini ve Perplexity'de markanızı görünür kılıyoruz. 
AI ajan kurulumu, GEO optimizasyonu ve iş otomasyonu. Ücretsiz analiz için iletişime geçin.">
```

### Türkçe Hero Metni
```
Mevcut (EN): "AI Agents That Think, Decide, and Execute."
Yeni (TR):   "Düşünen, Karar Veren ve Harekete Geçen AI Ajanlar"
Alt metin:   "Araçlar sorunu çözmez. Özerk sistemler çözer."
```

---

## 2. Eklenecek Bölümler

### Bölüm A — Sonuçlar / Vaka Özeti
**Konum:** Hero'nun hemen altı (mevcut istatistik bandının yerine veya yanına)

```
[%527]          [8/8]           [30 Gün]         [100+]
Organik Artış   AI Motor        İlk Sonuç        Otomasyon
(Müşteri Vakası) Görünürlüğü    Garantisi        Projesi
```

- Rakamlar animasyonlu counter ile gelecek (mevcut style ile uyumlu)
- Altına küçük: "Gerçek müşteri sonuçları — vaka detayları için iletişime geçin"

### Bölüm B — Hizmetler Açıklama (3 Kart)
**Konum:** GEO dashboard bölümünden önce

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  GEO            │  │  AI Ajan        │  │  Otomasyon      │
│  Optimizasyon   │  │  Kurulumu       │  │  Sistemleri     │
│                 │  │                 │  │                 │
│ ChatGPT, Gemini │  │ 7/24 çalışan    │  │ İş süreçlerini  │
│ ve Perplexity   │  │ akıllı ajanlar  │  │ otomatize et    │
│ de görün        │  │ kur             │  │                 │
│                 │  │                 │  │                 │
│ [Daha Fazla]    │  │ [Daha Fazla]    │  │ [Daha Fazla]    │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

### Bölüm C — Güven Sinyalleri
**Konum:** FAQ bölümünden önce

- Müşteri logoları (varsa) veya sektör rozetleri
- "256-bit Güvenlik", "ISO Sertifikalı", "KVKK Uyumlu" ikonları görsel hale getirilecek
- Mevcut footer'da yazıyla var, görsel badge'e dönüştürülecek

### Bölüm D — Gizli EEAT Metnini Görünür Yap
Mevcut gizli metin About sayfasına veya footer üstüne **görünür** taşınacak:
```
Botfusions, yapay zeka destekli veri işleme ve otomasyon alanında 
sertifikalı mühendisler, kıdemli geliştiricilerden oluşan ekibiyle 
kurumsal çözümler sunar. GDPR ve KVKK uyumlu çalışır.
```

---

## 3. FAQ Türkçe Versiyonu

Mevcut 7 soru İngilizce. TR sayfası için Türkçe karşılıkları eklenecek:

| Mevcut (EN) | Eklenecek (TR) |
|---|---|
| What is the AI Visibility Score? | AI Görünürlük Skoru nedir? |
| AI models give different answers... | AI modelleri farklı cevap verirse? |
| What is '30M Synthetic Persona'? | 30 Milyon Sentetik Persona ne demek? |
| How long does it take? | Ne kadar sürede sonuç alırım? |
| How do you measure AI traffic? | AI motorlarından gelen trafiği nasıl ölçüyorsunuz? |
| Can't we manage manually? | Bunu kendi ajansımızla yapamaz mıyız? |
| Botfusions vs competitors? | Rakiplerinizden farkınız ne? |

---

## 4. Teknik Gereksinimler

| Konu | Gereksinim |
|------|-----------|
| Framework | Mevcut stack korunacak (Next.js/React varsayımı) |
| i18n | next-intl veya i18next ile TR/EN dil yönetimi |
| hreflang | TR ve EN için doğru hreflang tag'leri |
| Schema | Mevcut 4 schema korunacak, TR dili eklentisi yapılacak |
| Accordion | FAQ cevapları `<noscript>` fallback ile desteklenecek |
| Performance | LCP < 2.5s korunacak |

---

## 5. Sayfa Yapısı (Yeni Sıralama)

```
1. Navbar (TR/EN toggle)
2. Hero (Türkçe metin)
3. İstatistik Bandı → %527 + diğer rakamlar  ← YENİ
4. Hizmetler 3 Kart  ← YENİ
5. GEO Monitoring Dashboard (8/8 engines)
6. Command Center for AI Visibility
7. Our Proven Framework
8. Accelerate Sales Growth
9. Key Benefits
10. Güven Rozetleri  ← YENİ (görselleştirilmiş)
11. FAQ (TR versiyonu)  ← GÜNCELLENDİ
12. CTA Banner
13. Footer
```

---

## 6. Test Senaryoları

**T1:** TR kullanıcı → "/" açar → Türkçe içerik görür → "EN" tıklar → İngilizce geçer  
**T2:** Google Search Console → hreflang hatası yok → TR/EN sayfaları ayrı indexleniyor  
**T3:** Google Rich Results Test → FAQPage schema geçiyor  
**T4:** PageSpeed Insights → LCP < 2.5s, CLS < 0.1  
**T5:** ChatGPT'de "Botfusions nedir?" sorusu → FAQ cevabından alıntı geliyor (30 gün sonra)

---

## Tamamlanma Checklist

- [ ] TR title + meta description yayında
- [ ] `/en` route çalışıyor, hreflang doğru
- [ ] İstatistik bandı eklendi (%527 dahil)
- [ ] 3 hizmet kartı eklendi
- [ ] FAQ Türkçe versiyonu yayında
- [ ] Güven rozetleri görselleştirildi
- [ ] EEAT metni görünür hale getirildi
- [ ] Google Rich Results Test → FAQ geçiyor
- [ ] PageSpeed → LCP < 2.5s
- [ ] GSC'de TR/EN sayfaları ayrı indexlendi

**Süre:** 3-5 gün | **Zorluk:** Orta  
**İletişim:** info@botfusions.com | +90 850 302 74 60
