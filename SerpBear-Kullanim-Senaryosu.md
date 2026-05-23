# SerpBear — Kurulum & Kullanım Senaryosu
**Botfusions AI Reklam Ajansı | Mayıs 2026**

---

## ✅ Sistem Durumu

| Kontrol | Sonuç |
|---------|-------|
| Sunucu erişimi | ✅ Aktif (HTTP 200) |
| Uygulama yükleniyor | ✅ SerpBear arayüzü açılıyor |
| API Key mevcut | ✅ Tanımlı |
| Scraping servisi | ⚠️ Henüz ayarlanmadı (ScrapingRobot gerekli) |

---

## 🔐 Erişim Bilgileri

| Alan | Değer |
|------|-------|
| URL | http://5.182.33.26:3080 |
| Kullanıcı | admin |
| API Key | c7d1e476a70f7a495cbc34748433c136 |

---

## 🚀 Adım Adım İlk Kurulum Senaryosu

### Adım 1 — Giriş Yap
1. Tarayıcıda `http://5.182.33.26:3080` aç
2. Kullanıcı: `admin` / Şifre: `S3rpB34r!2026.Strong`
3. Dashboard'a giriş yapıldığını doğrula

---

### Adım 2 — Scraping Servisi Ayarla (ÖNEMLİ)
SerpBear Google'dan rank verisi çekebilmek için bir scraping servisi gerektirir.

**Ücretsiz Seçenek: ScrapingRobot**
1. `https://scraping-robot.io` adresine git → ücretsiz hesap aç
2. API Key'ini kopyala (aylık **5.000 ücretsiz sorgu**)
3. SerpBear → **Settings** → **Scraping** sekmesine git
4. "ScrapingRobot" seç → API Key'i yapıştır → Kaydet

**Alternatif Seçenekler:**
- **Serper.dev** — Aylık 2.500 ücretsiz
- **DataForSEO** — Ücretli, çok güvenilir
- **Kendi proxy'in** — Manuel proxy listesi girilebilir

---

### Adım 3 — Domain Ekle
1. Dashboard'da **"Add Domain"** butonuna tıkla
2. Domain: `botfusions.com` gir
3. Ülke: **Turkey (TR)** seç
4. Dil: **Turkish** seç
5. **Kaydet**

**Müşteri Domainleri için:** Her müşteri için ayrı domain ekle.

---

### Adım 4 — Keyword Ekle
Domain eklendikten sonra:
1. `botfusions.com` domain kartına tıkla
2. **"Add Keyword"** butonuna bas
3. Takip edilecek keywordleri ekle:

```
Başlangıç keyword listesi (önerilen):
- botfusions
- ai reklam ajansı
- yapay zeka reklam
- geo hizmet
- ai seo
- chatbot ajansı türkiye
- otomatik sosyal medya yönetimi
```

4. Her keyword için **etiket (tag)** ekleyebilirsin (örn: `marka`, `geo`, `servis`)

---

### Adım 5 — İlk Taramayı Başlat
1. Keyword'leri ekledikten sonra **"Refresh"** butonuna tıkla
2. SerpBear Google'da her keyword'ü arar ve pozisyonu kaydeder
3. İlk veri ~2-5 dakika içinde gelir
4. Scraping servisi ayarlanmadıysa bu adım çalışmaz ⚠️

---

### Adım 6 — Otomatik Takip Ayarla
1. **Settings → Notification** bölümüne git
2. Email bildirimleri için SMTP ayarla (veya Slack webhook)
3. **Tarama sıklığı:** Günlük (önerilen) veya haftalık seç
4. SerpBear her gün belirlenen saatte otomatik tarama yapar

---

## 📊 API ile Kullanım (Otomasyon)

SerpBear'in REST API'si ile Claude veya N8N entegre edilebilir:

### Domain Listesi Al
```bash
GET http://5.182.33.26:3080/api/domains
Header: X-Api-Key: c7d1e476a70f7a495cbc34748433c136
```

### Keyword Listesi Al
```bash
GET http://5.182.33.26:3080/api/keywords?domainId=DOMAIN_ID
Header: X-Api-Key: c7d1e476a70f7a495cbc34748433c136
```

### Yeni Keyword Ekle
```bash
POST http://5.182.33.26:3080/api/keywords
Header: X-Api-Key: c7d1e476a70f7a495cbc34748433c136
Body: {
  "domainId": "DOMAIN_ID",
  "keywords": ["ai reklam ajansı", "geo hizmet"],
  "country": "TR",
  "device": "desktop",
  "tags": ["botfusions"]
}
```

### Manuel Tarama Başlat
```bash
POST http://5.182.33.26:3080/api/refresh
Header: X-Api-Key: c7d1e476a70f7a495cbc34748433c136
Body: { "domainId": "DOMAIN_ID" }
```

---

## 🤖 Claude ile Entegrasyon Senaryosu

Claude her sabah otomatik olarak şunu yapabilir:

```
1. SerpBear API → keyword pozisyonlarını çek
2. Önceki günle karşılaştır → düşen/çıkan keywordleri tespit et
3. Raporu oluştur → Gmail ile Cenk'e gönder
4. Büyük düşüşlerde alarm ver (örn: 5+ pozisyon kayıp)
```

Bu senaryo için **scheduled task** + **SerpBear API** + **Gmail MCP** kombinasyonu kullanılır.

---

## 🌐 Domain Atama (Coolify ile)

Eğer `serpbear.botfusions.com` gibi bir subdomain üzerinden erişmek istersen:

1. Coolify paneline git: `http://5.182.33.26:8000`
2. SerpBear servisi → **Domain** alanına `serpbear.botfusions.com` yaz
3. DNS'te A kaydı ekle: `serpbear` → `5.182.33.26`
4. SSL sertifikası otomatik alınır (Let's Encrypt)

---

## ⚡ Hızlı Başlangıç Özeti

```
✅ 1. http://5.182.33.26:3080 → Giriş yap
✅ 2. Settings → Scraping → ScrapingRobot API key ekle
✅ 3. Domain ekle: botfusions.com (TR / Türkçe)
✅ 4. Keyword'leri ekle (marka + servis + hedef kelimeler)
✅ 5. İlk taramayı başlat
✅ 6. Günlük otomatik tarama ayarla
🚀 7. Claude entegrasyonu → sabah raporu
```

---

*Botfusions AI Reklam Ajansı · botfusions.com · info@botfusions.com*
