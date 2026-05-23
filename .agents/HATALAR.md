# Botfusions — Bilinen Hatalar & Çözüm Durumu

> Bu dosya tespit edilen hataları, kök nedenleri ve çözüm adımlarını takip eder.  
> Her yeni LLM oturumunda CLAUDE.md okuma protokolüne dahildir.

---

## HATA-001 — Google Ads Dönüşüm Takibi: 0 Dönüşüm

**Tarih:** 25 Nisan 2026  
**Durum:** ✅ Çözüldü — Mayıs 2026  
**Etki:** ₺634,89 / 7 gün harcandı, hiçbir form/telefon tıklaması ölçülemiyor

### Gerçek Kök Neden (25 Nisan'da Tespit Edildi)

**GTM'deki GA4 Yapılandırma etiketi yanlış Measurement ID'ye gönderiyordu:**
- Yanlış: `G-DFGR4GS0P7` (var olmayan/yanlış mülk)
- Doğru: `G-T1JJQT8QXT` (531252912 — botfusions mülkü)
- Bu nedenle 19 Nisan'dan bu yana hiçbir GA4 verisi toplanamamıştı

### Yapılan Düzeltmeler ✅

- **GTM Sürüm 3** yayınlandı — 25.04.2026 12:31
  - "GA4 - Yapılandırma" etiketi: G-DFGR4GS0P7 → **G-T1JJQT8QXT** olarak düzeltildi
  - Yayınlama notu: "GA4 Measurement ID Düzeltmesi"
- **Doğrulama:** GA4 gerçek zamanlı dashboard'da 2 aktif kullanıcı görüldü (düzeltme çalışıyor)
- **GA4 ↔ Google Ads bağlantısı:** Veri yöneticisi → 1 bağlandı, 19 Nis 2026'dan itibaren ✅

### Yeni UI Notu

Google Ads'deki eski GA4 import URL'leri artık çalışmıyor (`/aw/conversions/import/ga4` → 404).  
**Doğru yol:** GA4'te event'i "Temel etkinlik" (key event) olarak işaretle → Google Ads 24-48 saat içinde otomatik import eder.

### Kalan Adımlar (24 saat sonra)

**Adım 1 — GA4'te Temel Etkinlik işaretle:**
```
GA4 (cenk@botfusions.com) → Yönetici → Etkinlikler → Önemli etkinlikler
→ form_submitted → ⭐ Temel etkinlik yap
→ phone_click → ⭐ Temel etkinlik yap
```
*(Etkinlikler listede görünmüyorsa 24 saat daha bekle — GTM düzeltmesi henüz yeni)*

**Adım 2 — Google Ads otomatik import:**
```
Google Ads → Araçlar → Dönüşümler listesini kontrol et
→ form_submitted + phone_click → 24-48 saat içinde otomatik görünecek
```

**Adım 3 — Temizlik:**
- "GEO Hizmet - Form Gönderimi" ONCLICK aksiyonunu devre dışı bırak (çakışma önlemek için)

### Bağlam

- Smart Bidding için 30+ dönüşüm gerekiyor — bu çözülmeden Smart Bidding açılmasın
- GTM fix öncesinde toplanan 0 dönüşüm verisi geçersiz; 25 Nisan'dan itibaren sayım sıfırdan başlıyor

---

## HATA-002 — 14 Keyword Hiç Gösterim Almıyor

**Tarih:** 25 Nisan 2026  
**Durum:** ✅ Çözüldü — Mayıs 2026  
**Etki:** Keyword havuzunun %74'ü tamamen pasif

### Pasif Keywordler (son 7 gün, 0 gösterim)

- generative engine optimization (BROAD + EXACT)
- KOBİ dijital görünürlük (BROAD + PHRASE)
- marka AI görünürlüğü (BROAD)
- AI aramalarda görünme (BROAD)
- GEO danışmanlık (BROAD + PHRASE)
- AI görünürlük artırma (BROAD)
- ChatGPT'de görünürlük (BROAD)
- Perplexity görünürlük (BROAD)
- yapay zeka arama optimizasyonu (PHRASE + EXACT)

### Kök Neden

Türkiye'de bu terimler için yeterli arama hacmi yok. Özellikle:
- "generative engine optimization" — İngilizce teknik terim, TR'de çok düşük hacim
- "ChatGPT'de görünürlük", "Perplexity görünürlük" — henüz aranmıyor

### Çözüm

Keyword Planner ile hacim kontrolü yap → 0 hacimli keywordleri duraklat → bütçeyi çalışan keywordlere yönlendir.

---

## HATA-003 — Bütçe Konsantrasyonu (Kronik)

**Tarih:** İlk tespit 15 Nisan 2026, 25 Nisan'da hâlâ devam ediyor  
**Durum:** ✅ Çözüldü — Mayıs 2026  

| Dönem | En pahalı keyword | Pay |
|-------|-------------------|-----|
| 1-14 Nisan | yapay zeka SEO (BROAD) | %59,7 |
| 19-25 Nisan | AI arama optimizasyonu (BROAD) | %57,8 |

BROAD eşleşme + Smart Bidding yok kombinasyonu bütçeyi tek keyword'e kilitleyor.  
**Çözüm:** HATA-001 çözüldükten sonra Smart Bidding aç (Target CPA).

---

## HATA-004 — PMAX Kampanyası Durmuş

**Tarih:** 25 Nisan 2026  
**Durum:** ✅ Kapatıldı — Kullanıcı tarafından kasıtlı durduruldu  
**Kampanya:** "Campaign #1" — PAUSED (bilerek)  
**Not:** Cenk tarafından manuel olarak durduruldu. Hata değil, takip edilmesine gerek yok.

---

---

## TAMAMLANAN ÇALIŞMALAR

### AŞAMA-2 — GSC Entegrasyonu & CMO Dashboard (✅ Tamamlandı — Mayıs 2026)

**Üretilen Dosyalar:**

- **`gsc_api_server.py`** — Flask REST API, 6 endpoint, mevcut refresh token ile doğrudan GSC'ye bağlanıyor
- **`start-cmo-dashboard.bat`** — Çift tıkla sunucuyu başlatır, tarayıcıda dashboard'u açar
- **`cmo-dashboard.html`** — Güncellenmiş dashboard:
  - GSC badge topbar'da
  - Sidebar'da canlı metrikler (ID'li elementler)
  - Teknik tab'da gerçek keyword tablosu + quick wins + top sayfalar

**Nasıl Test Edilir:**
```
start-cmo-dashboard.bat → çift tıkla
GSC bağlantısı yeşil = gerçek veri geliyor
GSC bağlantısı kırmızı = token yenile: python 05-gsc-nocodb/get_gsc_token.py
```

**Sıradaki Aşamalar:**
- Aşama 3 → Reddit/sosyal medya canlı mention monitoring
- Aşama 4 → Claude API ile gerçek AI CMO chat backend
- Aşama 5 → SaaS olarak paketleme (Next.js + Supabase, multi-tenant)

---

## HATA-005 — Google Ads MCP Bağlantı Sorunları (✅ Çözüldü — 10 Mayıs 2026)

**Tarih:** 10 Mayıs 2026
**Durum:** ✅ Çözüldü
**Etki:** MCP ile Google Ads'e bağlanılamıyor, rapor çekilemiyordu

### Tespit Edilen Sorunlar ve Çözümler

**Sorun 1: GOOGLE_ADS_CREDENTIALS yolu yanlıştı**
- `.mcp.json` dosyasında `C:\Users\user\google-ads.yaml` yazıyordu ama dosya yoktu
- **Çözüm:** `claude_desktop_config.json` içindeki `GOOGLE_ADS_CREDENTIALS` yolu düzeltildi:
  ```
  C:\Users\user\Downloads\Z.ai_claude code\AI  Reklam  Ajansı\04-araclar\google_ads_mcp\google-ads.yaml
  ```

**Sorun 2: Refresh token süresi dolmuştu**
- Eski token geçersizdi (USER_PERMISSION_DENIED hatası)
- **Çözüm:** `get-refresh-token.py` ile yeni token alındı (cenk@botfusions.com ile)
- Script yolu: `04-araclar/google_ads_mcp/get-refresh-token.py`

**Sorun 3: login_customer_id yanlış ayarlanmıştı**
- `google-ads.yaml` dosyasında `login_customer_id: 3646875139` yazıyordu
- Google API bu hesabı "client account" olarak görüp manager ID istiyordu
- 9965454498 (deaktif MCC) ve 5131327019 (ayrı hesap) denendi, hiçbiri çalışmadı
- **Çözüm:** `login_customer_id` tamamen kaldırıldı (yorum satırı yapıldı)
- Hesap `3646875139` artık login_customer_id olmadan direkt erişilebiliyor

### Doğru Yapılandırma (google-ads.yaml)

```yaml
developer_token: {{GOOGLE_ADS_DEVELOPER_TOKEN}}
client_id: {{GOOGLE_CLIENT_ID}}
client_secret: {{GOOGLE_CLIENT_SECRET}}
refresh_token: [geçerli token]
# login_customer_id:   ← KALDIRILDI, ayarlanmamalı
use_proto_plus: True
```

### Hesap Yapısı

| Hesap ID | Ad | Erişim |
|----------|-----|--------|
| 3646875139 | Botfusions (kampanyalar) | ✅ Direkt erişim, login_customer_id gereksiz |
| 5131327019 | botfusions (MCC, boş) | ✅ Erişilebilir ama kampanya yok |
| 9965454498 | Bilinmiyor | ❌ Deaktif |

### Token Yenileme

Token süresi dolduğunda:
```powershell
cd "C:\Users\user\Downloads\Z.ai_claude code\AI  Reklam  Ajansı\04-araclar\google_ads_mcp"
C:\Users\user\.local\bin\uv.exe run python get-refresh-token.py
# → cenk@botfusions.com ile giriş yap
# → Yeni token'ı google-ads.yaml dosyasındaki refresh_token alanına yapıştır
# → Cowork'u yeniden başlat
```

### Rapor Scripti

`04-araclar/google_ads_mcp/rapor10gun.py` → Son 10 günlük kampanya + keyword + günlük trend raporu
```powershell
C:\Users\user\.local\bin\uv.exe run python rapor10gun.py
```

---

## TAMAMLANAN ÇALIŞMALAR (12 Mayıs 2026)

### LinkedIn Reklam Videosu — 45s MP4 Üretimi

**Tarih:** 12 Mayıs 2026
**Durum:** ✅ Tamamlandı

**Üretilen Dosya:**
- `04-araclar/remotion-kaynak/out/linkedin-ad-45s.mp4` (5.8 MB, 1920x1080, 45s)

**Kullanılan Kaynaklar:**
- Resim 1 (baslangic.png): GEO v2 gorseli (1603x1211)
- Resim 2 (bit.png): The Visibility Report 12052026 (1664x1211)
- Muzik: mixkit-deep-urban-623.mp3 (8.8 MB)

**Render Scripti:**
- `04-araclar/remotion-kaynak/linkedin-ad-render.py`
- FFmpeg pipe modu + Pillow (1350 frame, 3.1 dk render suresi)
- Remotion npm SSL hatasi nedeniyle Python alternatifi kullanildi

**Video Yapisi:**

| Zaman | Sahne | Icerik |
|-------|-------|--------|
| 0-2s | Intro fade | Siyah -> Resim 1 |
| 2-9s | Hook | "Yapay Zeka Caginda" + "Gorunmezlik Duvarini Asmak" |
| 9-15s | Atif Ekonomisi | "%25 trafik kaybi" |
| 15-18s | Gecis | Resim 1 -> Resim 2 crossfade |
| 18-24s | Davranissal Zeka | "50.000+ kullanici yolculugu" |
| 24-30s | Makine Anlasilabilirligi | "7 Farkli Modelde Canli Izleme" |
| 30-36s | Varlik Otoritesi | "Entity Authority" |
| 36-45s | CTA | "botfusions.com/geo-hizmet" + buton |

**Renk Paleti (resimlerle uyumlu):**
- Accent: #6366f1 (violet/indigo — Visibility Report'tan alindi)
- Overlay: Koyu gradyan (metin okunabilirligi icin)
- Animasyonlar: Ken Burns zoom, slide-in, fade, bounce CTA

**Bilinen Sinirlamalar:**
- Remotion (React) render calismadi — npm SSL hatasi (UNABLE_TO_VERIFY_LEAF_SIGNATURE)
- Python + Pillow alternatifi kullanildi, kalite ayni seviyede
- Windows cp1254 encoding → "→" karakteri yerine "-" kullanildi

---

### Proje Temizlik (12 Mayıs 2026)

**Durum:** ✅ Tamamlandı

**Sonuclar:**
- Disk: 4.4 GB -> 1.3 GB
- Git tracked: 1348 -> 503 dosya
- Silinen: canva-mcp-server, seomachine, google-cli, claude-ads, creative-engine + 7 olu kok dosya + 903 frame PNG
- Commit: `9a27fa9`

### SERPiq Entegrasyonu (12 Mayıs 2026)

**Durum:** ✅ Kuruldu, OAuth bekliyor

- Repo: https://github.com/manojahi/serpiq
- Konum: `04-araclar/serpiq/`
- Config: `~/.serpiq/config.json` (provider: anthropic, model: claude-sonnet-4-5)
- ai-seo skill v2.1.0'a SERPiq bolumu eklendi
- **Bekleyen:** `npx serpiq auth` ile GSC OAuth yapilmali

---

*Son güncelleme: 12 Mayıs 2026 | Botfusions AI Reklam Ajansı*
