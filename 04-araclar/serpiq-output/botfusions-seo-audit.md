# Botfusions.com — SerpIQ Tarzı SEO Audit
**Tarih:** 30 Nisan 2026  
**Analiz:** Codebase + Google Ads verisi + AI sentez  
**Model:** claude-sonnet-4-6  

---

## 🩺 Site Aşama Tanısı

**Aşama: `low_visibility → visibility_no_clicks`**

| Sinyal | Değer | Yorum |
|--------|-------|-------|
| Ücretli tıklama (10 gün) | 22 | Düşük hacim |
| Organik veri | GSC bağlı değil | Ölçülemiyor |
| Blog içerik | 0 | İçerik yok |
| Dönüşüm | 0 | Trafik kalitesi sorunu |
| Marka bilinirliği | Düşük | Yeni ajans |

Botfusions şu an **görünürlük kazanıyor ama dönüşüme çeviremiyor.** Temel sorun: trafik geldiğinde ne göreceğini bilmiyor.

---

## 1. 🔍 Ürün & Pazar Anlayışı

**Botfusions ne satıyor?**  
GEO (Generative Engine Optimization) — markaların ChatGPT, Claude, Gemini, Perplexity gibi AI araçlarının yanıtlarında görünmesini sağlama hizmeti.

**Kritik içgörü:** Hedef kitle **problem-aware ama solution-unaware.**  
"AI'da görünmüyorum" sorununu hissediyorlar ama "GEO" terimini bilmiyorlar. Bu eğitim içeriği gerektiriyor.

**Ana değer önerisi:** %527 organik trafik artışı (kanıtlanmış vaka)

---

## 2. 📊 Mevcut Görünürlük Analizi

### Google Ads'ten Gelen Sinyaller (Organik için proxy)

Son 10 günde arama terimleri şunları gösteriyor:

**✅ Yüksek intent — hedeflenmeli:**
| Terim | Gösterim | Yorum |
|-------|----------|-------|
| generative engine optimization | 12 | Bilinçli arıyor, EN NİTELİKLİ |
| geo hizmeti | 35 | Doğrudan ürün araması |
| agentic engine optimization | 1 | Yeni trend, erken fırsat |
| agentic engine optimization aeo | 1 | Uzun kuyruk fırsat |
| geo search optimization | 2 | Alakalı intent |
| answer engine optimization | 1 | AEO = GEO ile örtüşüyor |
| arama motoru optimizasyonu | 1 | Geleneksel → GEO köprüsü |

**❌ Yanlış intent — zaten temizlendi:**
chatbot, seo bot, ahrefs, amplitude vb. (30 Nisan fix ile kapatıldı)

---

## 3. 🎯 Keyword Boşluk Analizi

### Striking Distance (Hemen Kazanılabilir)

Bu terimler zaten gösterim alıyor ama içerik eksikliği yüzünden dönüşmüyor:

```
generative engine optimization → Blog yazısı YOK
agentic engine optimization    → Blog yazısı YOK  
answer engine optimization     → Blog yazısı YOK
geo nedir                      → Landing page içeriği ZEK
geo vs seo                     → Karşılaştırma içeriği YOK
```

### Eğitim Keyword Kümesi (Blog Serisi)

```
GEO nedir?                              → Pillar içerik
ChatGPT'de nasıl görünürüm?             → Uzun kuyruk
AI arama motorlarında üst sıra          → İnformasyonel
Perplexity SEO nasıl yapılır?           → Spesifik platform
Gemini'de marka görünürlüğü             → Spesifik platform
GEO vs SEO farkı nedir?                 → Karşılaştırma
yapay zeka arama optimizasyonu nedir?   → TR versiyonu
```

### Ürün Intent Kümesi (Landing Page)

```
AI arama optimizasyonu hizmeti
yapay zeka SEO ajansı
GEO danışmanlık
AI görünürlük artırma
ChatGPT optimizasyon hizmeti
```

---

## 4. 🤖 AI Motorlarında Görünürlük (GEO Öz-Analiz)

Botfusions'ın kendi hizmetini satması için önce **kendisi AI motorlarında görünmeli.**

**Şu an eksik olan:**
- Wikipedia / Vikipedi kaydı yok
- LinkedIn şirket sayfası aktif değil
- Blog/içerik yok → AI motorları alıntı yapacak kaynak bulamıyor
- Basın / PR zero → "Botfusions" sorgusu AI'da çıkmıyor olabilir
- Structured data (Schema.org Organization) eksik mi?

**Acil yapılması gereken:**
Kendi landing page'inizi AI motorlarının anlayacağı formata optimize edin — bu hem organik hem de GEO için temel.

---

## 5. 📋 İçerik Öncelik Matrisi

| Öncelik | İçerik | Tip | Hedef Keyword | Etki |
|---------|--------|-----|---------------|------|
| 🔴 1 | GEO Nedir? Kapsamlı Rehber | Blog | "GEO nedir", "generative engine optimization" | Yüksek |
| 🔴 2 | GEO vs SEO: Temel Farklar | Blog | "geo vs seo", "yapay zeka SEO" | Yüksek |
| 🟡 3 | ChatGPT'de Nasıl Görünürsünüz? | Blog | "chatgpt'de görünmek", "ai arama" | Orta |
| 🟡 4 | Botfusions Vaka Çalışması | Blog | marka + sektör keyword | Orta |
| 🟢 5 | Agentic Engine Optimization | Blog | "agentic engine optimization" | Uzun vade |
| 🟢 6 | Answer Engine Optimization | Blog | "AEO nedir" | Uzun vade |

---

## 6. ⚡ Quick Wins (Bu Hafta Yapılabilecekler)

### 1. Landing Page Schema Ekle
```json
{
  "@type": "ProfessionalService",
  "name": "Botfusions GEO Hizmeti",
  "description": "Generative Engine Optimization...",
  "areaServed": "TR"
}
```

### 2. "GEO Nedir?" Blog Yazısı
- Hedef: 1.500+ kelime
- Target keyword: "generative engine optimization TR"
- Internal link: /geo-hizmet landing page'e
- CTA: Ücretsiz GEO analizi formu

### 3. FAQ Bölümü Landing Page'e Ekle
AI motorları FAQ'lardan doğrudan alıntı yapıyor. Eklenecek sorular:
- "GEO hizmeti ne kadar sürer?"
- "ChatGPT'de görünmek için ne yapmalıyım?"
- "GEO ile SEO arasındaki fark nedir?"
- "Botfusions hangi AI motorlarına optimize ediyor?"

### 4. Google My Business
Yerel aramalar için zorunlu. "GEO ajansı İstanbul" gibi aramalarda önemli.

---

## 7. 📈 Beklenen Etki (90 Gün)

| Metrik | Şu An | 30 Gün | 90 Gün |
|--------|-------|--------|--------|
| Organik keyword | ~0 | 5-10 | 20-40 |
| Blog trafik | 0 | 50-100/ay | 300-500/ay |
| AI atıfı (ChatGPT vb.) | 0 | İlk görünüm | Düzenli |
| Form doldurma | 0 | 1-3 | 5-10/ay |

---

## 8. 🔄 Öğrenilen Sinyaller → Sonraki Döngü

**Kazanan açı:** "Türkiye'nin ilk GEO ajansı" + "%527 vaka" ikili en güçlü mesaj  
**Proof gap:** Vaka çalışması sayısı artırılmalı  
**Visual win:** GEO vs SEO karşılaştırma görseli yüksek engagement alır  
**Snippet fırsatı:** "GEO nedir?" sorusu için featured snippet alınabilir

---

**Rapor:** Botfusions AI Reklam Ajansı — SerpIQ Pipeline  
**İletişim:** info@botfusions.com | +90 850 302 74 60
