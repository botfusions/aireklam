# Medya Geliştirme — Sistem Kontekst Dosyası

> **Claude için talimat:** Bu dosyayı önce oku. Kullanıcıya sormadan önce buradaki bilgileri kontrol et.  
> Eksik bilgi varsa sor — ama bu dosyada yazılı olan şeyleri tekrar sorma.

---

## Botfusions Kimdir?

**Türkiye'nin öncü AI pazarlama ajansı.** GEO, agentic sistemler ve AI chatbot kurulumu yapıyor.  
Site: `botfusions.com` · Mail: `info@botfusions.com` · Tel: `+90 850 302 74 60`

**Marka sesi:** Uzman + Dürüst + İddalı + Eğitici. Jargon yok, abartı yok. Somut veri, net adım.  
**Ana kanıt:** "%527 organik trafik artışı" — gerçek müşteri vakası.

---

## Hizmet Nişleri (İçerik Üretilecek 3 Alan)

### 1. GEO / AI SEO
ChatGPT, Claude, Gemini, Perplexity'de görünürlük optimizasyonu.  
Landing: `botfusions.com/geo-hizmet`  
Hedef: KOBİ'ler, yerel işletmeler, dijital ajanslar  
Hook açısı: "Rakibin AI'da çıkıyor, sen çıkmıyorsun"  
Rekabet: Türkiye'de GEO bilen ajans sayısı çok az → erken hareket avantajı  
**Fiyat: Tanışma Paketi $500** (GeoNexa global rakip Basic paketi $1.499 — avantajlı giriş)  
Kopyalar: `../01-reklam-kopyalari/geo-reklam-kopyalari.md`  
Görseller: `../02-gorseller/geo-gorseller/`

### 2. Agentic Sistemler
Otonom AI agent kurulumu — Claude SDK, MCP, workflow otomasyonu.  
Hedef: Şirketler, girişimler, operasyonunu otomatize etmek isteyen ekipler  
Fiyat aralığı: Kurulum 5K–50K USD · Aylık 2K–10K USD retainer (S-Tier iş modeli)  
Hook açısı: "7/24 çalışan, hiç yorulmayan dijital çalışan"  
Rekabet: Türkiye'de gerçekten teslim edebilen çok az oyuncu var

### 3. AI Chatbot & Asistanlar
Web satış & müşteri destek botları, sesli AI ajanlar.  
Hedef: E-ticaret, hizmet sektörü, müşteri hizmetleri yoğun işletmeler  
Fiyat aralığı: Aylık 500–2.000 USD retainer (A-Tier iş modeli)  
Hook açısı: "Müşteri hizmetleri maliyetini %80 düşür"  
Rekabet: Ürün satan çok var, gerçek kurulum yapan az

---

## Hedef Kitle

| Segment | Kanal | Mesaj Tonu |
|---------|-------|-----------|
| KOBİ sahipleri | Instagram, Facebook | Basit, somut fayda, rakam |
| Dijital pazarlamacılar | LinkedIn, X | Teknik, data odaklı |
| Girişimciler / startup | TikTok, X | Hızlı, pratik, trend |
| Kurumsal karar vericiler | LinkedIn | Güven, vaka çalışması, ROI |

---

## Rakip Haritası (Özet)

| Rakip Tipi | Tehdit | Botfusions Farkı |
|------------|--------|-----------------|
| Geleneksel SEO ajansları | Düşük | GEO bilmiyorlar |
| Jasper / Copy.ai gibi araçlar | Orta | Araç değil hizmet satıyoruz |
| Freelancer danışmanlar | Düşük | Ölçeklenemezler |

→ Tam rakip analizi: `../context/competitor-analysis.md`

---

## Sosyal Medya Hesapları

| Platform | Account ID | Format |
|----------|-----------|--------|
| Instagram | `881407_instagram` | Post / Story / Reel |
| Facebook | `881407_facebook` | Post / Story / Reel |
| YouTube | `881407_youtube` | Yalnızca Reel |
| TikTok | `881407_tiktok` | Post / Reel |
| Pinterest | `881407_pinterest` | Post |
| X | `881407_x` | Post (25K karakter limit) |

**API Key:** `secrets.env` → `OMNISOCIALS_API_KEY`

---

## Botfusions Marka Renkleri

| Renk | Hex | Kullanım |
|------|-----|----------|
| Primary Purple | `#A855F7` | Ana marka rengi |
| Dark Purple | `#7C3AED` | İkincil / aksan |
| Blue | `#3B82F6` | Bilgi / vurgu |
| Orange | `#F97316` | CTA / öne çıkarma |
| Yellow | `#FDE047` | Rozet / highlight |

---

## İçerik Üretim Kuralları

1. Önce yaz → kullanıcı onaylar → sonra görsel üret
2. Görsel onay olmadan yayın yapılmaz
3. Türkçe yazan skill: `turkce-insani-yazar` — AI tonu giderilmiş
4. Platform adaptasyonu zorunlu — her kanal kendi limiti ve formatında

### Hook Formülleri (Kanıtlanmış)
- **Rakam hook:** "%527 organik trafik artışı — 90 günde"
- **Acı nokta:** "Müşteri ChatGPT'ye soruyor. Rakibin çıkıyor. Sen çıkmıyorsun."
- **Merak:** "ChatGPT'de kaç soru senin işletmenden geçti bu ay?"
- **Sosyal kanıt:** "Türkiye'de GEO'yu uygulayan ajanslardan biriyiz"

---

## Dual-Brain Hafıza Mimarisi

Her ajan çalışması sonucu **iki beyne** kaydedilir:

| Beyin | Konum | Ne zaman |
|-------|-------|----------|
| **Beyin 1** — Obsidian Wiki | `hafiza/` (vault kökü) | Her çalışmada → log + ilgili klasör |
| **Beyin 2** — Claude Memory | `spaces/.../memory/` | Kritik öğrenme, karar, hata düzeltmesi |

Detaylar: `hafiza/DUAL-BRAIN.md`

> ⚠️ `medya-gelistirme/hafiza/` artık kullanılmıyor — tüm kayıtlar ana `hafiza/` wikisine.

---

## Bu Sistemin Modülleri

| Klasör | İş |
|--------|----|
| `01-veri-toplama/` | Günlük rakip analiz, trend scrape, Google Ads verisi |
| `02-strateji/` | Hook seçimi, CTA, kanal/format kararı |
| `03-icerik-motoru/` | Script, carousel, 6 kanal adaptasyon |
| `04-gorsel-uretim/` | PNG statik, MP4 video, platform boyutları |
| `05-yayin/` | OmniSocials scheduling + onay kapısı |
| `06-analytics-loop/` | Performans raporu + içerik motoruna feedback |
| `hafiza/` | Hook kütüphanesi, rakip arşivi, performans tarihi |

→ Her modülün detayı ilgili klasördeki `GOREV.md` dosyasında.

---

## Bağlantılı Kaynaklar (Ana Klasörde)

| Dosya | İçerik |
|-------|--------|
| `../context/brand-voice.md` | Marka sesi ve mesaj çatısı |
| `../context/competitor-analysis.md` | Tam rakip analizi |
| `../context/features.md` | Hizmet detayları ve USP |
| `../context/target-keywords.md` | SEO anahtar kelimeler |
| `../context/style-guide.md` | Yazı stili kuralları |
| `../01-reklam-kopyalari/geo-reklam-kopyalari.md` | GEO kampanya kopyaları |
| `../AI-Is-Modelleri-Tier-Listesi.md` | S/A/B/F tier iş modeli analizi |
| `../CLAUDE.md` | Sistem durumu, araçlar, skill haritası |

---

## Aktif Kampanya Durumu

| Kampanya | Durum | Sorun |
|----------|-------|-------|
| GEO Hizmet (Google Ads) | Aktif | Bütçenin %99.4'ü tek keyword'de |
| Sosyal Medya | Hazır değil | İçerik sistemi kurulacak |
| Analytics/Dönüşüm | Eksik | Form submit takibi yok |

## ⚠️ Kritik Site Durumu

| Sorun | Detay | Öncelik |
|-------|-------|---------|
| **GEO ajans listelerinde yok** | TR'deki "en iyi GEO ajansı" listelerinde Botfusions geçmiyor | 🔴 Yüksek |
| **botfusion.com (s'siz) satılık** | $9.999'a başka biri alabilir, marka karmaşası riski | 🟡 Orta |

> Google index sorunu önceden çözüldü. Tekrar işaretleme.

---

*Botfusions AI Reklam Ajansı · Mayıs 2026 · botfusions.com*
