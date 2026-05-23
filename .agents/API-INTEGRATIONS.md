# Botfusions AI Reklam Ajansi — API Entegrasyonlari

> Bu dosya, projenin kullandigi tum API'leri ve entegrasyonlari dokumente eder.
> Yeni bir LLM bu dosyayi okuyarak hangi API'lerin kurulu oldugunu ve nasil kullanildigini ogrenir.

---

## 1. Google Ads API (MCP)

**Durum:** Aktif
**Skill'ler:** `advertising/ads-google`, `marketing/paid-ads`, `advertising/ads-budget`
**Konfigurasyon:** `.mcp.json` (proje root)

### Kurulum
```bash
# 1. Google Ads MCP klasoru
cd 04-araclar/google_ads_mcp/

# 2. YAML konfigurasyon dosyasi
# google-ads.yaml icinde:
# - developer_token
# - client_id, client_secret
# - refresh_token
# - customer_id: 3646875139
```

### Mevcut Hesap
- **Customer ID:** 3646875139
- **Login Customer ID:** MCC ustu hesap (varsa)

### Kullanilan Araclar (MCP)
- `execute_gaql` — GAQL sorgusu calistirma
- `list_accessible_accounts` — Hesaplari listeleme
- `get_reporting_view_doc` — Raporlama gorunumu dokumani
- `get_reporting_fields_doc` — Alan dokumani

---

## 2. Gemini / Nano Banana Pro (Gorsel Uretimi)

**Durum:** Planlanmis
**Skill'ler:** `advertising/ads-generate`, `advertising/ads-photoshoot`
**Konfigurasyon:** Composio uzerinden erisim

### Gerekenler
- Gemini API anahtari veya Banana MCP konfigurasyonu
- Prompt → Gorsel → URL → Google Sheets pipeline

### Pipeline
```
Prompt → Gemini Nano Banana Pro → Gorsel URL → Google Sheets
```

---

## 3. Google Sheets API

**Durum:** Aktif
**Skill'ler:** Gorsel arsiv, kampanya takibi
**Sheet ID:** `1XrE0F5PWNXuvtvFv8OdK9-3zr-wUhNnkP4KuKviX3os`

### Kullanim
- Gorsel URL + kopya arsivi
- Kampanya performans verileri
- A/B test sonuclari

---

## 4. GA4 / Google Search Console + NocoDB Pipeline

**Durum:** Pipeline hazır, credentials bekleniyor
**Skill'ler:** `marketing/analytics-tracking`, `marketing/seo-audit`, `marketing/ai-seo`
**Modul Konumu:** `04-araclar/seo-machine-modules/modules/`
**Pipeline Konumu:** `05-gsc-nocodb/`

### Modüller
- `google_analytics.py` — GA4 veri çekme
- `google_search_console.py` — GSC veri çekme (mevcut)

### Agentic Pipeline (Yeni)
```
GSC API → gsc_nocodb_pipeline.py → NocoDB → Rapor
```

| Dosya | Açıklama |
|-------|----------|
| `05-gsc-nocodb/gsc_nocodb_pipeline.py` | Ana pipeline (GSC → NocoDB) |
| `05-gsc-nocodb/agent.py`               | Otonom ajan + anomali tespiti |
| `05-gsc-nocodb/nocodb_setup.py`        | İlk kurulum (tablo oluşturma) |
| `05-gsc-nocodb/.env.example`           | Ortam değişkenleri şablonu |

### NocoDB Tabloları
| Tablo | İçerik |
|-------|--------|
| `gsc_keywords`  | Keyword pozisyonları, quick win fırsatları |
| `gsc_pages`     | Düşük CTR sayfalar, iyileştirme fırsatları |
| `gsc_trends`    | Yükselen sorgular |
| `gsc_summary`   | Günlük özet, tüm metrikler |

### Kurulum
```bash
# 1. Bağımlılıkları yükle
pip install -r 05-gsc-nocodb/requirements.txt

# 2. .env oluştur
cp 05-gsc-nocodb/.env.example 05-gsc-nocodb/.env
# → GSC_CREDENTIALS_PATH ve NOCODB_API_TOKEN ekle

# 3. NocoDB base ve tabloları oluştur
python 05-gsc-nocodb/nocodb_setup.py --base "Botfusions SEO" --create

# 4. Pipeline çalıştır
python 05-gsc-nocodb/agent.py --client botfusions --days 30
```

### Müşteri Profili Ekleme
`05-gsc-nocodb/gsc_nocodb_pipeline.py` → `CLIENT_PROFILES` dict'ine ekle:
```python
"yeni-musteri": {
    "client_id": "yeni-musteri",
    "site_url": "https://yeni-musteri.com",
    "nocodb_base": "Yeni Müşteri SEO",
},
```

### Env Değişkenleri
```bash
GSC_CREDENTIALS_PATH=/path/to/gsc-service-account.json
NOCODB_BASE_URL=http://botfusions.com:8080
NOCODB_API_TOKEN=your_nocodb_token_here
```

---

## 5. WordPress API

**Durum:** Modul mevcut
**Skill'ler:** `.claude/commands/publish-draft.md`
**Modul Konumu:** `04-araclar/seo-machine-modules/modules/wordpress_publisher.py`

### Kullanim
- Blog yazisi yayinlama
- Landing page yayinlama
- SEO metadata otomatik doldurma

---

## 6. Composio (Otomasyon)

**Durum:** Referans olarak mevcut
**Skill'ler:** Gorsel pipeline

### Kullanim
- `GEMINI_GENERATE_IMAGE` → Gorsel uretme
- `GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND` → Sheets'e kayit

---

## 7. Web Search (Dahili)

**Durum:** Aktif (Claude Code Web Search tool)
**Skill'ler:** Tum arastirma skill'leri

### Kullanim
- Keyword arastirmasi
- Rakip analizi
- Trend tespiti
- SERP analizi

---

## 9. OmniSocials API (Sosyal Medya Dağıtım)

**Durum:** Aktif — API Key mevcut
**Skill'ler:** `advertising/social-publisher`
**Dokümantasyon:** https://docs.omnisocials.com

### API Key
```
OMNISOCIALS_API_KEY={{secrets.env dosyasindan okunur}}
```

### Desteklenen Platformlar (11 Kanal)
| Kanal ID | Platform | Feed | Story | Reel |
|----------|----------|------|-------|------|
| `facebook` | Facebook | ✅ | ✅ | ✅ |
| `instagram` | Instagram | ✅ | ✅ | ✅ |
| `threads` | Threads | ✅ | - | - |
| `linkedin` | LinkedIn Profil | ✅ | - | - |
| `linkedin_page` | LinkedIn Şirket | ✅ | - | - |
| `youtube` | YouTube | - | - | ✅ |
| `tiktok` | TikTok | ✅ | - | ✅ |
| `pinterest` | Pinterest | ✅ | - | - |
| `x` | X (Twitter) | ✅ | - | - |
| `bluesky` | Bluesky | ✅ | - | - |
| `mastodon` | Mastodon | ✅ | - | - |

### Bağlı Hesap ID'leri — Botfusions Workspace (881407)

| Platform | Account ID | Kullanıcı | İçerik Türleri |
|----------|-----------|-----------|----------------|
| Instagram | `881407_instagram` | @botfusions | post, story, reel |
| Facebook | `881407_facebook` | Ömer Tokgöz | post, story, reel |
| YouTube | `881407_youtube` | @botfusionss | reel |
| TikTok | `881407_tiktok` | @botfusions | post, reel |
| Pinterest | `881407_pinterest` | cenk0342 | post |
| X (Twitter) | `881407_x` | @botfusionss | post (X Premium) |

**Pinterest Board ID'leri:**
- `AI-Botfusions-GEO` → `1091067515915706441`
- `Profil` → `1091067515915706431`

### Temel Endpoint'ler
```bash
# Hesapları listele (bağlı kanallar)
GET https://api.omnisocials.com/v1/accounts

# Gönderi oluştur (taslak)
POST https://api.omnisocials.com/v1/posts/create

# Oluştur + hemen yayınla
POST https://api.omnisocials.com/v1/posts/create-and-publish

# Medya yükle
POST https://api.omnisocials.com/v1/media/upload

# Taslağı yayınla
POST https://api.omnisocials.com/v1/posts/:id/publish
```

### Temel Kullanım (Cross-posting)
```json
{
  "content": {
    "default": "Genel metin tüm platformlar için",
    "x": "Kısa versiyon (280 karakter limit) 🚀",
    "linkedin": "LinkedIn için uzun, profesyonel versiyon...",
    "linkedin_page": "[Botfusions Resmi] Şirket sayfası versiyonu..."
  },
  "accounts": [
    "facebook-account-id",
    "instagram-account-id",
    "linkedin-account-id",
    "x-account-id"
  ],
  "media_urls": {
    "default": ["https://cdn.../gorsel-16x9.jpg"],
    "instagram": ["https://cdn.../gorsel-1x1.jpg"]
  },
  "scheduled_at": "2026-05-15T10:00:00Z"
}
```

### Workflow Entegrasyonu
```
content-repurposer skill → Platform bazlı metinler
        ↓
canvas-design / HyperFrames → Görseller (URL olarak)
        ↓
OmniSocials API → Tek çağrıyla tüm platformlara yayın
        ↓
Google Sheets → Post URL'leri + durum kaydı
```

### Önemli Notlar
- Hesap bağlantıları (OAuth) sadece dashboard üzerinden: `app.omnisocials.com → Settings → Channels`
- Rate limit: 100 istek/dakika
- Karakter limitleri: X=280, LinkedIn=3000, Instagram=2200
- `partially_posted` durumu: bazı platformlar başarısız olsa diğerleri etkilenmez

---

## 10. Supabase (Medya & Post Veritabanı)

**Durum:** Aktif — VPS1 (turklawai.com)
**Kullanım:** Medya kütüphanesi, yayınlanan postlar, analytics arşivi

### Bağlantı Bilgileri
```
SUPABASE_URL={{secrets.env dosyasindan okunur}}
SUPABASE_ANON_KEY={{secrets.env dosyasindan okunur}}
SUPABASE_SERVICE_KEY={{secrets.env dosyasindan okunur}}
```

### Tablolar (kurulum: `supabase-setup.sql` çalıştır)
| Tablo | İçerik |
|-------|--------|
| `media_library` | Üretilen tüm görsel/video — URL, tip, boyut |
| `social_posts` | Yayınlanan postlar — platform, durum, OmniSocials ID |

### Storage Bucket
- `media-library` — public bucket, tüm görseller/videolar burada

### API Endpoint'leri
```
REST: https://supabase.turklawai.com/rest/v1/
Storage: https://supabase.turklawai.com/storage/v1/
Auth: Authorization: Bearer <ANON_KEY veya SERVICE_KEY>
```

---

## API Kurulum Oncelikleri

| Oncelik | API | Durum | Etki |
|---------|-----|-------|------|
| 1 | Google Ads MCP | Aktif | Reklam denetimi ve optimizasyon |
| 2 | OmniSocials | Aktif ✅ | Sosyal medya dağıtımı (11 kanal) |
| 3 | GA4 + GSC | API Key gerekli | Performans takibi |
| 4 | Gemini/Banana | Planlanmis | Gorsel uretimi |
| 5 | WordPress | Modul hazir | Icerik yayinlama |
| 6 | Google Sheets | Aktif | Veri arsivi |

---

## 8. Skill Kaynak Deposu

**Tek kaynak:** `coreyhaines31/marketingskills`
**URL:** https://github.com/coreyhaines31/marketingskills
**Durum:** Aktif — yeni skill güncellemeleri buradan takip edilir

### Kural
Yeni skill eklenecekse veya mevcut skill güncellenecekse **sadece bu repo** referans alınır.
`whyashthakker/agent-skills-marketing` ve `kostja94/marketing-skills` repoları KULLANILMAZ.

### Güncelleme Süreci
1. `coreyhaines31/marketingskills` reposunda yeni release/commit var mı kontrol et
2. Local `.agents/skills/marketing/` klasörü ile karşılaştır
3. Eksik skill'leri aynı SKILL.md formatında oluştur
4. `MANIFEST.md` sürümünü artır ve yeni skill'leri tabloya ekle

### Mevcut Versiyon
- **Local:** v2.1.0 (75 skill) — Mayıs 2026
- **Upstream:** coreyhaines31/marketingskills — v1.10.0

---

## Yeni Ortama Tasima Kontrol Listesi

Yeni bir makineye tasidiginda:

- [ ] `.mcp.json` dosyasini kopyala
- [ ] Google Ads `google-ads.yaml` dosyasini kopyala (API anahtarlari icerir)
- [ ] `.env` dosyasini olustur (GA4, GSC anahtarlari)
- [ ] Node.js kur (Remotion icin)
- [ ] Python 3.11+ kur (moduller icin)
- [ ] `pip install -r 04-araclar/seo-machine-modules/requirements.txt`
