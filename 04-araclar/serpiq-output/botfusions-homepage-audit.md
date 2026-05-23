# botfusions.com — Ana Sayfa SEO Audit
**Tarih:** 30 Nisan 2026  
**Kaynak:** Canlı sayfa taraması + codebase analizi  
**Model:** claude-sonnet-4-6  

---

## 🩺 Site Aşama Tanısı

**Aşama: `low_visibility` — Görünürlük yok, içerik temeli eksik**

| Sinyal | Değer | Yorum |
|--------|-------|-------|
| Google Ads (ana sayfa) | Yok | Organik trafiğe bağımlı |
| Organik GSC verisi | Bağlı değil | Ölçülemiyor |
| Blog içerik | Var ama muhtemelen ince | Teyit gerekiyor |
| İçerik dili | İngilizce | Türk hedef kitle için sorunlu |
| Yapısal veri (Schema) | ✅ Güçlü | Organization + FAQPage + HowTo + SoftwareApplication |

---

## 1. 🔍 Sayfa Analizi — Güçlü & Zayıf Yönler

### Görsel Olarak Güçlü
- Tasarım profesyonel, Botfusions marka kimliğiyle uyumlu (mor/koyu tema)
- GEO Checker aracı navbarda → lead magnet olarak çalışabilir
- "8/8 AI Engines" monitörü — rakiplerinden farklılaşıyor
- Dashboard/simulation görselleri güven veriyor
- "100+ Automations, 99.9% Uptime, 256-bit Security, ISO Certified" sosyal kanıt var

### SEO Açısından Kritik Sorunlar

**1. Başlık yanlış hedeflenmiş 🔴**
```
Mevcut: "AI Agents That Think, Decide, and Execute. | Botfusions"
Sorun:  Kimse "AI agents that think" aramıyor
Hedef:  "GEO Hizmetleri | AI Görünürlük Optimizasyonu | Botfusions"
```

**2. Dil karmaşası 🔴**
- Ana sayfa: **İngilizce**
- `/geo-hizmet` landing page: **Türkçe**
- Google Ads: **Türkçe** keywordler hedefliyor ama **İngilizce** ana sayfaya yönlendirebilir
- Türk KOBİ hedef kitlesine İngilizce ana sayfa yabancı hissettiriyor

**3. Hero mesajı convert etmiyor 🟡**
```
"Tools don't solve problems. Autonomous systems do."
```
Zekice ama Türkiye pazarında bu soyutlama anlaşılmıyor.
Türk KOBİ sahibi şunu anlamak istiyor: "Bu benim için ne yapıyor?"

**4. Gizli metin bloğu ⚠️**
Sayfa kaynak kodunda şifre gibi bir metin var:
> "Botfusions — Formerly known as XTRACT — Premium AI-driven data extraction..."

Bu muhtemelen AI motorları için kasıtlı eklendi (GEO amacıyla). Organization Schema'da da bu bilgiler mevcut. Ancak Google bunu **gizli içerik** olarak işaretleyebilir — görünür ve doğal bir About bölümüne taşınması daha güvenli.

---

## 2. 📊 Keyword Boşluk Analizi

### Ana Sayfanın Hedeflemesi Gereken Terimler (Türkçe)

| Keyword | Niyet | Zorluk | Öncelik |
|---------|-------|--------|---------|
| yapay zeka otomasyon ajansı | Satın alma | Orta | 🔴 Yüksek |
| AI ajan hizmeti | Bilgi + satın alma | Düşük | 🔴 Yüksek |
| agentic AI çözümleri | Bilgi | Çok düşük | 🟡 Orta |
| yapay zeka danışmanlık | Satın alma | Orta | 🔴 Yüksek |
| AI görünürlük optimizasyonu | Bilgi + satın alma | Çok düşük | 🔴 Yüksek |
| GEO ajansı | Satın alma | Çok düşük | 🟡 Orta |

### Şu An Gelen Ama Kaçırılan Arama Niyetleri

```
"AI ajan ne işe yarar?"         → Sayfa cevap vermiyor, eğitim içeriği yok
"yapay zeka ile iş otomasyonu"  → İçerik yok
"GEO nedir Türkiye"             → Blog yazısı yok
"botfusions"                    → Marka aramaları — iyimser senaryo
```

---

## 3. 🌐 GEO (AI Motor) Görünürlük Analizi

**Sayfa GEO için kısmen hazır, ama eksikler var:**

### ✅ İyi — Beklenenden Çok Daha Sağlam
- Wiki sayfası var (navbarda) — AI motorları wiki'den alıntı yapar
- GEO Checker aracı kendi başına otorite sinyali
- **FAQPage Schema mevcut** — 7 sorulu accordion, schema ile desteklenmiş ✅
- **Organization Schema** — adres, telefon, logo, sektör bilgisi tam ✅
- **HowTo Schema** — süreç adımları için ✅
- **SoftwareApplication Schema** — GEO Checker aracı için ✅
- "8/8 engines" monitörü sektörel uzmanlık gösteriyor
- Footer'da "vs Competitors" sayfaları (Brand24, Mention, Scrunch AI, Brandwatch) — karşılaştırma trafiği için akıllı

### ⚠️ Hâlâ Eksik
| Eksik | Etki |
|-------|------|
| Vaka çalışması yok | "%527 artış" sayfada görünmüyor, sadece söylenti |
| Backlink / PR eksik | AI motorları authority sinyali olarak kullanıyor |
| Blog içerik ince | Citation kaynağı yetersiz |
| Accordion cevapları DOM'da gizli | Googlebot JS çalıştıramazsa göremez — schema telafi ediyor ama risk var |

---

## 4. 📋 Sayfa İçeriği Boşlukları

### Mevcut Bölümler
- Hero: AI Agents + CTA
- GEO monitoring dashboard (8/8 engines)
- Command Center for AI Visibility
- Our Proven Enterprise-Grade Framework  
- Accelerate Sales Growth (leads, content, social post)
- The Key Benefits of AI for Your Business Growth

### Eksik Bölümler (Rakiplerinde Var)

**1. Vaka Çalışması / Sonuçlar Bölümü**
```
"%527 organik trafik artışı" → Sayfada görünmüyor, eklenirse güçlü sosyal kanıt
Müşteri logoları → Yok
Before/After metrikleri → Yok
```

**2. Hizmet Açıklama Bölümü**
"AI Agents" ne demek? Türk KOBİ sahibi bilmiyor.  
3 hizmet kutusu + "nasıl çalışır" akışı eklenebilir.

**3. ✅ FAQ Bölümü — MEVCUT** *(Önceki raporda hatalı "yok" denilmişti)*  
7 sorulu accordion + FAQPage Schema ile tam kurulmuş:
- What exactly is the AI Visibility Score?
- What is '30 Million Synthetic Persona' technology?
- How long does it take to see results?
- How do you measure traffic from AI models?
- Botfusions vs competitors farkı nedir?

**4. Güven Sinyalleri**
- Müşteri yorumları / testimonial → Yok
- Medyada yer aldık logoları → Yok
- Sertifikalar → Footer'da "Data Privacy Assured & Enterprise-Grade Security" var ama görsele dönüştürülmemiş

---

## 5. ⚡ Quick Wins (Bu Hafta)

### 1. Title Tag Güncelle
```html
<!-- Mevcut -->
<title>AI Agents That Think, Decide, and Execute. | Botfusions</title>

<!-- Önerilen -->
<title>Botfusions | AI Ajan & GEO Hizmetleri — Türkiye'nin Öncü AI Ajansı</title>
```

### 2. Meta Description Ekle / Güncelle
```html
<meta name="description" content="ChatGPT, Gemini ve Perplexity'de 
markanızı görünür kılıyoruz. AI ajan kurulumu, GEO optimizasyonu ve 
otomasyon hizmetleri. Ücretsiz analiz için hemen iletişime geçin.">
```

### 3. ✅ FAQPage Schema — ZATEN MEVCUT
Accordion'daki cevaplar FAQPage Schema ile desteklenmiş. Yapılacak tek şey:
accordion cevaplarının Googlebot JS çalıştıramazsa da okunabilmesi için
`<noscript>` fallback veya statik HTML alternatifi eklemek.

### 4. Gizli Metin Bloğunu Görünür Yap
Şu an görünmez durumdaki EEAT metni bir "About" bölümüne taşı. Google bunu penalty olarak değerlendirebilir.

### 5. Türkçe Dil Seçeneği
Nav'daki EN düğmesi var ama TR sayfası çalışıyor mu? Test et.

---

## 6. 📈 Beklenen Etki (90 Gün)

| Metrik | Şu An | 30 Gün | 90 Gün |
|--------|-------|--------|--------|
| Marka araması CTR | Düşük | +%30 (title fix) | +%50 |
| FAQ snippet | 0 | 1-2 | 5+ |
| AI motor atıfı | Düşük | Artış | Düzenli |
| Organik oturum | Ölçüsüz | GSC bağlandıktan sonra | Taban oluşur |

---

## 7. 🔄 geo-hizmet vs Ana Sayfa Karşılaştırması

| | botfusions.com | botfusions.com/geo-hizmet |
|--|----------------|--------------------------|
| Dil | İngilizce | Türkçe |
| Hedef | Global/Enterprise | Türk KOBİ |
| Ads | Yok | Aktif kampanya |
| Dönüşüm | Book a call | Form doldurma |
| İçerik | Geniş hizmet yelpazesi | Tek ürün odaklı |
| SEO olgunluğu | Daha gelişmiş | Daha ham |

**Öneri:** Ana sayfaya Türkçe trafik yönlendirmeden önce ya TR versiyonu çıkar ya da `/geo-hizmet`'i ana Ads hedefi olarak tut.

---

**Rapor:** Botfusions AI Reklam Ajansı — SerpIQ Pipeline  
**Sonraki adım:** GSC bağla → gerçek organik veriyle karşılaştır  
**İletişim:** info@botfusions.com | +90 850 302 74 60
