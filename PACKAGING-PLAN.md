# Paketleme Plani

Bu plan, `AI Reklam Ajansi` workspace'ini daha sonra tasinabilir, kurulabilir ve guvenli bir pakete donusturmek icin hazirlandi.

## Hedef

Mevcut klasor bir calisma alani. Paketleme hedefi ise bunu su yapiya indirmek:

- CMO dashboard'u calistiran lokal/API servis
- GSC, GA4, Google Ads, PageSpeed, OmniSocials ve Supabase entegrasyonlari
- GSC -> NocoDB raporlama pipeline'i
- Istege bagli Remotion video uretim modulu
- Secret icermeyen, kurulumu tekrar edilebilir, dokumante edilmis dagitim paketi

## Bolum 2 - Urun Mimarisi: Multi-Client Marketing OS

Bu sistem yalnizca Botfusions icin bir dashboard olarak dusunulmemeli. Nihai hedef, herhangi bir marka veya musteri icin kurulabilir bir pazarlama cozum sistemi olmali.

Konumlandirma:

```text
Marketing OS = SEO + GEO + Ads + Media + Analytics + Reporting
```

Bu yapida her musteri ayni motorlari kullanir, ancak kendi marka profili, web sitesi, hedef kitlesi, rakipleri, entegrasyonlari ve kanal hedefleriyle calisir.

### Ana Modul Haritasi

```text
Marketing OS
  Core
    - musteri profili
    - marka sesi
    - hedef kitle
    - urun/hizmet bilgisi
    - rakip listesi
    - kanal hedefleri

  SEO Engine
    - GSC veri cekme
    - teknik SEO kontrolu
    - keyword firsatlari
    - icerik plani
    - schema / internal link onerileri
    - SEO raporlama

  GEO Engine
    - AI gorunurluk analizi
    - LLM sorgu setleri
    - rakip cevap karsilastirmasi
    - entity ve kaynak guclendirme
    - GEO uyumlu sayfa/icerik onerileri

  Ads Engine
    - Google Ads audit
    - kampanya yapisi
    - negatif keyword onerileri
    - butce ve teklif analizi
    - reklam metni ve landing page uyumu

  Media Engine
    - reklam kopyalari
    - sosyal medya postlari
    - gorsel briefleri
    - video uretimi
    - yayinlama ve takvim

  Dashboard
    - SEO metrikleri
    - GEO skor/firsatlari
    - Google Ads metrikleri
    - GA4/donusum
    - medya uretim durumu
    - aksiyon listesi

  Connectors
    - Google Search Console
    - GA4
    - Google Ads
    - Supabase / NocoDB
    - OmniSocials
    - ileride Meta, LinkedIn, TikTok Ads
```

### GEO Modulunun Konumu

GEO sistemi ayri modul olarak kalmali, ancak SEO ile ortak veri kullanmali.

Ortak veriler:

- marka profili
- hedef kitle
- rakipler
- site sayfa envanteri
- keyword ve konu haritasi
- entity listesi
- schema ve kaynak bilgileri

Fark:

- SEO Engine klasik arama motoru performansina odaklanir.
- GEO Engine AI cevap motorlarinda gorunurluge odaklanir.

Bu nedenle ilk urun surumunde GEO ayri bir `geo` modulu olabilir. Daha sonra SEO dashboard'una "AI Visibility Layer" olarak baglanabilir.

### Musteri Config Modeli

Her musteri icin tek bir config dosyasi hedeflenmeli.

Onerilen format:

```json
{
  "client_id": "ornek-marka",
  "brand_name": "Ornek Marka",
  "website": "https://ornek.com",
  "industry": "SaaS",
  "market": "TR",
  "language": "tr",
  "modules": {
    "seo": true,
    "geo": false,
    "google_ads": true,
    "media": true,
    "social_publishing": false
  },
  "integrations": {
    "gsc_site_url": "https://ornek.com",
    "ga4_property_id": "",
    "google_ads_customer_id": "",
    "supabase_project": "",
    "nocodb_base": "Ornek Marka Marketing"
  }
}
```

Bu model sayesinde:

- Botfusions hardcoded degerleri sistemden ayrilir.
- Ayni kod tabani birden fazla musteri icin calisir.
- Modul bazli paketleme mumkun olur.
- Musteri bazli raporlama ve veri izolasyonu kolaylasir.

### Context Modeli

Mevcut `context/`, `.agents/` ve `hafiza/` yapilari urunlesirken ayrilmali.

Onerilen yeni yapi:

```text
clients/
  ornek-marka/
    client.json
    brand-profile.md
    audience.md
    competitors.md
    offers.md
    keywords.md
    content-map.md
    notes.md
```

Core motorlar bu dosyalari okuyarak calisir.

Botfusions icin mevcut dosyalar daha sonra su sekle tasinabilir:

```text
clients/botfusions/
  client.json
  brand-profile.md
  audience.md
  competitors.md
  offers.md
  keywords.md
  content-map.md
```

### Modul Bazli Paketleme

Urun paketinde moduller opsiyonel olmali.

```text
core              zorunlu
seo               opsiyonel ama ana paket icin onerilir
geo               opsiyonel, sonra baglanabilir
google_ads        opsiyonel
media             opsiyonel
social_publish    opsiyonel
dashboard         zorunlu veya viewer modu
```

Bu sayede farkli musteri paketleri olusur:

- SEO paketi
- SEO + GEO paketi
- Google Ads denetim paketi
- Media production paketi
- Full CMO paketi

### Veri Izolasyonu

Her musteri icin veri su alanlarda ayrilmali:

- config
- auth/integration mapping
- dashboard verisi
- raporlar
- medya uretimleri
- GSC/GA4/Ads metrikleri
- NocoDB veya Supabase tablolarinda `client_id`

Tablo tasariminda her kayitta `client_id` bulunmali.

Ornek:

```text
gsc_keywords
  client_id
  date_fetched
  keyword
  clicks
  impressions
  position

ads_campaigns
  client_id
  date_fetched
  campaign_id
  campaign_name
  spend
  conversions
  cpa

media_assets
  client_id
  campaign
  asset_type
  file_url
  status
```

### Urunlestirme Yol Haritasi

#### 1. Botfusions Hardcode Temizligi

- `SITE_URL`, customer id, account id, API key ve marka metinleri config'e tasinir.
- Dashboard sabit metinleri client config'ten beslenir.
- Endpointler `client_id` parametresi kabul etmeye baslar.

#### 2. Client Registry

`clients/` altinda musteri configleri tutulur.

Ilk hedef:

```text
clients/botfusions/client.json
clients/demo/client.json
```

#### 3. Modul Runner

Tek komutla modul calistirma hedeflenir:

```powershell
python app.py run seo --client botfusions
python app.py run ads --client botfusions
python app.py run media --client botfusions
python app.py run geo --client botfusions
```

#### 4. Dashboard Multi-Client

Dashboard acilisinda musteri secimi gelir:

```text
Client: Botfusions
Modules: SEO, Ads, Media, GEO
```

Bu noktada dashboard tek musteri yerine cok musteri yonetebilir.

#### 5. GEO Baglantisi

GEO baslangicta ayri calisir:

```powershell
python app.py run geo --client botfusions
```

Daha sonra SEO raporuna su alanlarla baglanir:

- AI visibility score
- cited pages
- missing entities
- source authority gaps
- recommended content updates

### Ilk Minimum Urun Paketi

En mantikli ilk paket:

```text
Core + SEO + Google Ads + Dashboard
```

Neden:

- GSC ve Google Ads tarafinda mevcut kod daha hazir.
- Dashboard zaten var.
- Metrik ve raporlama degeri somut.
- Media ve GEO sonradan moduler olarak eklenebilir.

Ikinci paket:

```text
Core + SEO + Google Ads + Media
```

Ucuncu paket:

```text
Core + SEO + GEO + Dashboard
```

Full paket:

```text
Core + SEO + GEO + Ads + Media + Social Publishing + Dashboard
```

### Urun Adlandirma Taslagi

Gecici teknik adlar:

- `Marketing OS`
- `CMO Engine`
- `AI Marketing Control Center`
- `Search + Ads Intelligence System`
- `SEO/GEO Growth Engine`

Kod icinde marka bagimsiz ad kullanilmali. Botfusions yalnizca ilk client/proje olmali.

## Onerilen Paket Tipi

Ana onerim: Docker uyumlu servis paketi.

Neden:

- Flask API, dashboard ve Python bagimliliklari tek ortamda sabitlenir.
- VPS, local Windows ve ileride SaaS ortami icin ayni servis mantigi kullanilir.
- Secret'lar `.env` ile disaridan verilir.
- `node_modules`, `.venv`, video ciktilari gibi agir klasorler pakete girmez.

Alternatif olarak Windows-only local paket de tutulabilir:

- `setup.ps1`
- `start.ps1`
- `.env`
- Python virtualenv
- dashboard HTML

Ancak uzun vadede Docker daha temiz.

## Paketlenecek Cekirdek Dosyalar

### Dashboard/API

- `gsc_api_server.py`
- `cmo-dashboard.html`
- `05-dashboard/index.html` mevcutsa dashboard alternatifi olarak
- `start-cmo-dashboard.bat` sadece local Windows paketinde

### GSC/NocoDB Pipeline

- `05-gsc-nocodb/agent.py`
- `05-gsc-nocodb/gsc_nocodb_pipeline.py`
- `05-gsc-nocodb/nocodb_setup.py`
- `05-gsc-nocodb/get_gsc_token.py`
- `05-gsc-nocodb/requirements.txt`
- `05-gsc-nocodb/README.md`

### SEO/Analytics Modulleri

- `04-araclar/seo-machine-modules/modules/`
- `04-araclar/seo-machine-modules/requirements.txt`

### Google Ads

- `04-araclar/google_ads_mcp/`
- Google Ads yardimci scriptleri:
  - `04-araclar/add_negative_keywords.py`
  - `04-araclar/add_negative_keywords_mayo5.py`
  - `04-araclar/fix_negative_keywords_apr30.py`
  - `04-araclar/pause_rarely_served_keywords.py`

Bu scriptler dogrudan operasyonel degisiklik yaptigi icin pakette `tools/google-ads/` altina tasinmasi daha iyi olur.

### Veritabani Kurulumu

- `supabase-setup.sql`
- `supabase-geo-setup.sql`

### Opsiyonel Remotion Modulu

Paketin video uretim varyanti icin:

- `04-araclar/remotion-kaynak/package.json`
- `04-araclar/remotion-kaynak/package-lock.json`
- `04-araclar/remotion-kaynak/remotion.config.ts`
- `04-araclar/remotion-kaynak/tsconfig.json`
- `04-araclar/remotion-kaynak/postcss.config.mjs`
- `04-araclar/remotion-kaynak/src/`
- `04-araclar/remotion-kaynak/public/` icinden sadece gerekli sabit asset'ler

## Pakete Girmemesi Gerekenler

Kesinlikle disarida kalmali:

- `.env/`
- `*.env`
- `05-gsc-nocodb/ga4-service-account.json`
- `credentials.json`
- `google-ads.yaml`
- `node_modules/`
- `.venv/`
- `__pycache__/`
- `.obsidian/`
- `.claude/settings.local.json`
- `out/`
- `04-araclar/remotion-kaynak/out/`
- `04-araclar/remotion-kaynak/frames_output/`
- uretilmis `.mp4`
- buyuk ham medya dosyalari
- gecici zip dosyalari
- kisisel hafiza/log dosyalari, paket hedefi degilse:
  - `hafiza/`
  - `medya-gelistirme/hafiza/`
  - `degisiklik-gecmisi/`

Opsiyonel/karara bagli:

- `01-reklam-kopyalari/`
- `02-gorseller/`
- `03-videolar/`
- `Marketing V2/`
- `context/`
- `.agents/skills/`

Bunlar urun paketinden cok ajans operasyon verisi. SaaS/urun paketinde yer almalari gerekiyorsa `examples/`, `templates/` veya `knowledge-base/` olarak ayrilmali.

## Env Sozlesmesi

Paketlemeden once `.env.example` olusturulmali. Gercek degerler asla repoya girmemeli.

Onerilen degiskenler:

```env
# Server
CMO_SERVER_HOST=127.0.0.1
CMO_SERVER_PORT=8765
APP_ENV=local

# Dashboard
SITE_URL=https://botfusions.com
GSC_SITE_URL=https://botfusions.com

# Google OAuth / GSC
GSC_REFRESH_TOKEN=
GSC_CLIENT_ID=
GSC_CLIENT_SECRET=
GSC_CREDENTIALS_PATH=

# GA4
GA4_PROPERTY_ID=
GA4_REFRESH_TOKEN=
GA4_CLIENT_ID=
GA4_CLIENT_SECRET=

# Google Ads
GOOGLE_ADS_CUSTOMER_ID=
GOOGLE_ADS_YAML_PATH=

# OmniSocials
OMNISOCIALS_API_KEY=
OMNISOCIALS_BASE_URL=https://api.omnisocials.com/v1

# Supabase
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# NocoDB
NOCODB_BASE_URL=
NOCODB_API_TOKEN=

# Optional
PAGESPEED_API_KEY=
ADMIN_API_TOKEN=
```

## Kod Temizligi Gerekenler

Paketlemeden once yapilacak zorunlu duzeltmeler:

1. `gsc_api_server.py` icindeki hardcoded `OMNI_KEY` ve `SUPA_KEY` env'e tasinacak.
2. `google_search_console.py` icindeki OAuth client id/secret env'e tasinacak.
3. `CLAUDE.md` icindeki acik API key kaldirilacak veya maskelenecek.
4. Runtime'da `pip install` yapan bloklar kaldirilacak.
5. `start-cmo-dashboard.bat` icindeki global pip install yerine setup scripti kullanilacak.
6. Remotion `Root.tsx` / `root.tsx` casing hatasi duzeltilecek.
7. `package.json` ve README scriptleri esitlendirilecek.
8. Publish endpointlerine `ADMIN_API_TOKEN` tabanli basit koruma eklenecek.
9. GSC anomaly agent onceki donem verisini NocoDB'den okuyacak sekilde guncellenecek.

## Onerilen Hedef Klasor Yapisi

```text
botfusions-cmo/
  app/
    server.py
    dashboard/
      index.html
    modules/
      seo/
      gsc/
      ga4/
      google_ads/
      omnisocials/
      supabase/
  pipelines/
    gsc_nocodb/
      agent.py
      pipeline.py
      setup.py
  tools/
    google-ads/
    remotion/
  sql/
    supabase-setup.sql
    supabase-geo-setup.sql
  config/
    clients.example.json
  docs/
    README.md
    SETUP.md
    DEPLOYMENT.md
  .env.example
  requirements.txt
  Dockerfile
  docker-compose.yml
  setup.ps1
  start.ps1
```

## Docker Taslagi

Ilk Docker paketi iki servisle baslayabilir:

```yaml
services:
  cmo-api:
    build: .
    env_file: .env
    ports:
      - "127.0.0.1:8765:8765"
    command: python app/server.py

  gsc-agent:
    build: .
    env_file: .env
    profiles: ["jobs"]
    command: python pipelines/gsc_nocodb/agent.py --client botfusions --days 30
```

Remotion dahil edilecekse ayri bir Node image daha mantikli:

```yaml
  remotion:
    build:
      context: tools/remotion
    profiles: ["video"]
    volumes:
      - ./media:/app/media
      - ./renders:/app/out
```

## Local Windows Paket Akisi

Docker kullanilmadan local paket istenirse:

1. `setup.ps1`
   - Python venv olusturur.
   - `requirements.txt` kurar.
   - `.env` yoksa `.env.example` kopyalama talimati verir.

2. `start.ps1`
   - venv'i aktif eder.
   - `python app/server.py` baslatir.
   - dashboard URL'sini yazar.

3. Opsiyonel `render-video.ps1`
   - Remotion klasorunde `npm install` kontrolu yapar.
   - secilen composition'i render eder.

## Paketleme Kontrol Listesi

### Guvenlik

- [ ] Tum secret'lar rotate edildi.
- [ ] Kodda hardcoded token kalmadi.
- [ ] Dokumanlarda acik key kalmadi.
- [ ] `.env.example` var.
- [ ] `.env`, service account JSON ve yaml credential dosyalari git disinda.
- [ ] Publish endpointlerinde admin token kontrolu var.

### Build

- [ ] `python -m py_compile` ana Python dosyalarinda geciyor.
- [ ] `pip install -r requirements.txt` temiz ortamda geciyor.
- [ ] `npx tsc --noEmit` Remotion icin geciyor.
- [ ] `npm run build:geo` veya secilen render scripti geciyor.
- [ ] README'deki tum komutlar gercek scriptlerle uyumlu.

### Paket Icerigi

- [ ] `node_modules` yok.
- [ ] `.venv` yok.
- [ ] `out`, `frames_output`, mp4 render ciktilari yok.
- [ ] buyuk ham medya dosyalari yok veya `media-sample/` olarak sinirli.
- [ ] submodule ihtiyaclari dokumante edildi.

### Operasyon

- [ ] `SETUP.md` var.
- [ ] `DEPLOYMENT.md` var.
- [ ] `TROUBLESHOOTING.md` var.
- [ ] NocoDB/Supabase kurulum adimlari net.
- [ ] Google Ads/GSC/GA4 auth akisi net.

## Asamali Yol Haritasi

### Asama 1 - Guvenli Temizlik

- Hardcoded key'leri kaldir.
- `.env.example` ekle.
- `.gitignore` guclendir.
- Remotion casing hatasini duzelt.

### Asama 2 - Calistirilabilir Paket

- Kok `requirements.txt` olustur.
- `setup.ps1` ve `start.ps1` ekle.
- `gsc_api_server.py` dosyasini `app/server.py` yapisina tasimaya basla.
- Dashboard dosyasini `app/dashboard/index.html` altina al.

### Asama 3 - Docker

- `Dockerfile` ekle.
- `docker-compose.yml` ekle.
- Lokal dashboard ve API'yi container ile calistir.
- Volume/env mantigini test et.

### Asama 4 - Urunlestirme

- Multi-client config dosyasi ekle.
- Auth/token mekanizmasini netlestir.
- GSC agent'i scheduled job yap.
- Raporlari `reports/` veya harici storage'a yaz.

## Paketleme Sonrasi Minimum Komutlar

Beklenen final deneyim:

```powershell
copy .env.example .env
notepad .env
.\setup.ps1
.\start.ps1
```

Docker varyanti:

```powershell
copy .env.example .env
docker compose up --build cmo-api
```

Dashboard:

```text
http://localhost:8765
```
