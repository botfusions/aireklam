# CMO Dashboard — Tamamlama & Multi-Tenant Plan
**Tarih:** 14 Mayıs 2026  
**Öncelik:** Önce Botfusions tam çalışır → sonra multi-tenant

---

## AŞAMA 1 — Botfusions'ı Tam Tamamla

### 1A. Acil Düzeltmeler (Bugün)

| # | Görev | Dosya | Durum |
|---|-------|-------|-------|
| 1 | Supabase tabloları oluştur | `supabase-setup.sql` | ❌ Bekliyor |
| 2 | JS veri şekli düzelt (`json.data` → `json.posts/media`) | `cmo-dashboard.html` | ✅ Yapıldı |
| 3 | PageSpeed proxy Flask'a taşı | `gsc_api_server.py` | ❌ Bekliyor |

**Supabase setup — PowerShell'den:**
```powershell
# supabase-setup.sql dosyasını Supabase Studio'da çalıştır
# URL: https://supabase.turklawai.com
```

**PageSpeed proxy (gsc_api_server.py'ye eklenecek):**
```python
PSI_KEY = os.getenv("PAGESPEED_API_KEY", "")  # opsiyonel

@app.route("/api/pagespeed")
def pagespeed():
    url = request.args.get("url", "https://botfusions.com")
    strategy = request.args.get("strategy", "mobile")
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy={strategy}"
    if PSI_KEY:
        api_url += f"&key={PSI_KEY}"
    r = req_lib.get(api_url, timeout=30)
    return jsonify(r.json())
```

---

### 1B. Veri Bağlantıları (Bu Hafta)

#### Google Ads → Dashboard
- MCP üzerinden zaten çekiliyor
- Dashboard "Google Ads" sekmesi verilerini gösteriyor mu? Kontrol et
- Gerekirse `gsc_api_server.py`'ye `/api/google-ads/summary` endpoint ekle

#### GA4 Credentials
```bash
# 05-gsc-nocodb/.env dosyasına ekle:
GSC_CREDENTIALS_PATH=C:\...\gsc-service-account.json
NOCODB_BASE_URL=http://botfusions.com:8080
NOCODB_API_TOKEN=...
```

#### Dönüşüm Takibi (geo-hizmet formu)
- `analytics-tracking` skill ile GTM event kur
- Form submit → GA4 `lead_form_submit` eventi
- Google Ads conversion action bağla

---

### 1C. Dashboard Eksik Sekmeler Durumu

| Sekme | Veri Kaynağı | Durum |
|-------|-------------|-------|
| Sağlık | PageSpeed API | ❌ CORS sorunu |
| Bağlantılar | Manuel / MCP | ⚠️ Kısmi |
| Teknik | GSC + PageSpeed | ⚠️ Kısmi |
| AI/GEO | GSC sorguları | ⚠️ GSC bağlı ama eksik |
| Kontroller | Manuel checklist | ❓ Kontrol et |
| Google Ads | Google Ads MCP | ✅ MCP aktif |
| Sosyal Medya | OmniSocials proxy + Supabase | ✅ Düzeltildi |

---

## AŞAMA 2 — Multi-Tenant Altyapı

### Hedef
Aynı CMO Dashboard'u birden fazla müşteri için çalıştır. Her müşterinin kendi:
- Domain'i
- Google Ads hesabı
- OmniSocials workspace'i
- Supabase şeması / prefix'i
- GSC site_url'i

### 2A. Client Config Yapısı

`clients/` klasörü oluştur:
```
clients/
  botfusions.json
  musteri-a.json
  musteri-b.json
```

**Örnek `clients/botfusions.json`:**
```json
{
  "id": "botfusions",
  "name": "Botfusions",
  "domain": "https://botfusions.com",
  "google_ads_customer_id": "3646875139",
  "omni_workspace_id": "881407",
  "omni_accounts": {
    "instagram": "881407_instagram",
    "facebook": "881407_facebook",
    "youtube": "881407_youtube",
    "tiktok": "881407_tiktok",
    "pinterest": "881407_pinterest",
    "x": "881407_x"
  },
  "supabase_url": "https://supabase.turklawai.com",
  "supabase_schema": "botfusions",
  "gsc_site_url": "https://botfusions.com",
  "brand_color": "#A855F7"
}
```

### 2B. Flask Server Multi-Tenant

`gsc_api_server.py`'ye client seçimi ekle:
```python
# Tüm endpoint'lere ?client=botfusions parametresi
@app.route("/api/omni/posts")
def omni_posts():
    client_id = request.args.get("client", "botfusions")
    cfg = load_client_config(client_id)
    # cfg'den Supabase URL ve şeması al
    ...
```

### 2C. Dashboard UI — Client Switcher

`cmo-dashboard.html`'e client seçici ekle:
- Sol üstte dropdown: "Botfusions ▼"
- Değiştirince tüm veriler o client için yeniden çekilir
- LocalStorage'da son seçilen client saklanır
- Her client'ın brand rengi header'a yansır

### 2D. Supabase Multi-Tenant Stratejisi

**Seçenek A — Schema izolasyonu (önerilen):**
```sql
CREATE SCHEMA botfusions;
CREATE TABLE botfusions.social_posts (...);

CREATE SCHEMA musteri_a;
CREATE TABLE musteri_a.social_posts (...);
```

**Seçenek B — Row-level isolation:**
```sql
ALTER TABLE social_posts ADD COLUMN client_id TEXT;
-- RLS policy ile her client kendi datasını görür
```

---

## AŞAMA 3 — Otomasyon & Ajans Operasyonu

### Günlük Rapor Ajanı
- Her sabah 08:00 → Google Ads spend + anomali
- GSC pozisyon değişimleri
- OmniSocials post performansı
- Gmail'e özet gönder (cenk.tokgoz@gmail.com)

### İçerik Pipeline Otomasyonu
```
AI CMO önerir → Onay al → OmniSocials ile yayınla → Supabase'e kaydet
```

### Alarm Sistemi
- Google Ads bütçe %80 aşımı → anlık bildirim
- Keyword pozisyon 5+ düşüş → otomatik rapor
- Platform bağlantı kopması → alert

---

## Öncelik Sırası (Acilden Uzağa)

1. ✅ OmniSocials proxy düzeltmesi — **YAPILDI**
2. ✅ JS veri şekli uyuşmazlığı — **YAPILDI**  
3. ❌ Supabase tabloları kur (supabase-setup.sql)
4. ❌ PageSpeed proxy Flask'a taşı
5. ❌ GA4 credentials ekle
6. ❌ Dönüşüm takibi (geo-hizmet)
7. ❌ Multi-tenant client config sistemi
8. ❌ Client switcher UI
9. ❌ Günlük rapor ajanı
10. ❌ Alarm sistemi

---

*Botfusions AI Reklam Ajansı · Mayıs 2026*
