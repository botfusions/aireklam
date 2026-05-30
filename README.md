# Botfusions AI Reklam Ajansi

AI destekli tam servis reklam ajansi sistemi. 68 skill, 5 kategori, CMO fonksiyonlarinin tamami.

## Mimari

```
URL / Brifing
     |
[1. MARKA ANALIZI]        ai-seo, paid-ads
[2. STRATEJI]              content-strategy, copywriting
[3. REKLAM KOPYA]          ad-creative, social-content
[4. GORSEL & VIDEO]        krea-ai, kie-ai, pixa, hyperframes
[5. DAGITIM & TAKIP]       Google Ads MCP, analytics-tracking
[6. RAPORLAMA]             marketing-dashboard, ab-test-setup
```

## Skill Envanteri (76 Skill, v2.1)

| Kategori | Sayi | Konum |
|----------|------|-------|
| Marketing | 47 | `.agents/skills/marketing/` |
| Advertising | 21 | `.agents/skills/advertising/` |
| Media Production | 4 | `.agents/skills/media/` |
| SEO | 1 | `.agents/skills/seo/` |
| Video | 1 | `.agents/skills/video/` |

### Marketing (47)
ab-test-setup, ad-creative, ai-seo, analytics-tracking, attribution-modeling, churn-prevention, cold-email, competitor-alternatives, competitor-audit, content-strategy, context-analyzer, copy-editing, copywriting, customer-journey, customer-research, email-sequence, form-cro, free-tool-strategy, image, influencer-marketing, launch-strategy, lead-magnets, marketing-automation, marketing-dashboard, marketing-ideas, marketing-psychology, newsletter, onboarding-cro, page-cro, paid-ads, paywall-upgrade-cro, popup-cro, pr-communications, pricing-strategy, product-marketing-context, programmatic-seo, referral-program, revops, sales-enablement, schema-markup, seo-audit, signup-flow-cro, site-architecture, social-content, social-listening, video, video-marketing

### Advertising (21)
ads, ads-amazon, ads-apple, ads-attribution, ads-audit, ads-budget, ads-competitor, ads-create, ads-creative, ads-dna, ads-generate, ads-google, ads-landing, ads-linkedin, ads-meta, ads-microsoft, ads-photoshoot, ads-plan, ads-server-side-tracking, ads-tiktok, ads-youtube

### Media Production (4)
krea-ai (64+ model, LoRA, 22K upscale), kie-ai (ucuz API gateway), pixa (MCP-native), wavespeed (15 model, maliyet optimizasyonu)

### SEO (1)
seo-expert (icerik pipeline + vaka analizi)

### Video (1)
hyperframes (HTML-tabanli video uretim, GSAP animasyon, 60+ hazir blok)

## Klasor Yapisi

```
AI Reklam Ajansi/
├── CLAUDE.md                          <- Master orchestrator
├── cmo-dashboard.html                 <- CMO Dashboard UI
├── gsc_api_server.py                  <- Flask API (GSC + OmniSocials proxy)
├── .env.template                      <- Secret referans sablonu
├── secrets.env                        <- Canli API keyler (GITIGNORED)
├── supabase-setup.sql                 <- Supabase tablo kurulumu
├── supabase-geo-setup.sql             <- GEO tablolari
├── start-cmo-dashboard.bat            <- Dashboard baslatici
├── yayinla.ps1                        <- OmniSocials yayin scripti
├── .agents/
│   ├── product-marketing-context.md   <- Marka bilgisi (Botfusions)
│   ├── MANIFEST.md                    <- Skill envanteri (68+ skill)
│   ├── API-INTEGRATIONS.md            <- API kurulum rehberi
│   ├── HATALAR.md                     <- Bilinen hatalar ve cozumler
│   ├── OKARA-GAP-ANALIZ.md            <- Okara gap analizi
│   ├── OMNISOCIALS.md                 <- OmniSocials entegrasyonu
│   └── skills/
│       ├── marketing/ (45+ skill)
│       ├── advertising/ (25+ skill)
│       ├── media/ (4 skill)
│       ├── seo/ (1 skill)
│       └── video/ (1 skill)
├── hafiza/                            <- Obsidian wiki (Dual-Brain)
│   ├── entities/                      <- Botfusions, GeoNexa, Lighthouse...
│   ├── concepts/                      <- GEO, AEO, MCP, RAG, n8n
│   ├── decisions/                     <- Fiyat, strateji karar kayitlari
│   ├── rakip-arsivi/                  <- Rakip snapshot'lari
│   └── trend-log/                     <- Haftalik trend ozetleri
├── medya-gelistirme/                  <- 6 modul icerik pipeline
│   ├── SISTEM-KONTEKST.md             <- Pipeline kontekst dosyasi
│   ├── supabase-pipeline-setup.sql    <- content_packages tablosu
│   ├── 01-veri-toplama/               <- Rakip analiz, trend scrape
│   ├── 02-strateji/                   <- Hook secimi, CTA, kanal karari
│   ├── 03-icerik-motoru/              <- Script, carousel, 6 kanal adaptasyon
│   ├── 04-gorsel-uretim/              <- PNG statik, platform boyutlari
│   ├── 05-yayin/                      <- OmniSocials scheduling + onay kapisi
│   └── 06-analytics-loop/            <- Performans raporu + feedback
├── context/                           <- Botfusions pazarlama verileri
│   ├── brand-voice.md
│   ├── features.md
│   ├── target-keywords.md
│   ├── competitor-analysis.md
│   ├── seo-guidelines.md
│   └── NotebookLLM/
├── 01-reklam-kopyalari/
│   ├── geo-reklam-kopyalari.md
│   └── competitor-karsilastirmalar/
├── 02-gorseller/
│   ├── botfusions-logo-*.png          <- 3 logo (icon, monogram, wordmark)
│   ├── geo-gorseller/                 <- 2 format (1:1, 9:16)
│   └── maskotlar/                     <- 6 maskot (C1-C6)
├── 04-araclar/
│   ├── google_ads_mcp/                <- Google Ads MCP server
│   ├── seo-machine-modules/           <- Python SEO modulleri
│   ├── hyperframes/                   <- HeyGen HyperFrames (aktif video)
│   ├── _arsiv-remotion-kaynak/        <- [ARSIV] Eski Remotion
│   └── serpiq/                        <- SERPiq SEO audit araci
├── 05-dashboard/
│   └── index.html                     <- Dark mode CMO dashboard
├── 05-gsc-nocodb/                     <- GSC pipeline
└── Marketing V2/                      <- SEO raporlari
```

## Yeni LLM Baslangic Protokolu

Herhangi bir LLM bu 4 dosyayi okuyarak baslayabilir:
1. `CLAUDE.md` -> Is akislari ve skill eslestirme
2. `.agents/product-marketing-context.md` -> Marka bilgisi, hedef kitle, ton
3. `.agents/MANIFEST.md` -> Skill envanteri ve kullanim kilavuzu
4. `.agents/API-INTEGRATIONS.md` -> API kurulum ve entegrasyon rehberi

## API Entegrasyonlari

| API | Durum | Detay |
|-----|-------|-------|
| Google Ads MCP | Aktif | Customer 3646875139, GAQL sorgulari, dashboard dinamik |
| OmniSocials API | Aktif | 6 kanal (IG, FB, YT, TikTok, Pinterest, X) |
| Flask Proxy (8765) | Aktif | GSC + Ads + GA4 + PageSpeed + Pipeline proxy |
| GSC (Search Console) | Bagli | OAuth refresh token ile |
| GA4 | Bagli | Property 531252912, OAuth refresh token |
| PageSpeed API | Aktif | Flask proxy `/api/pagespeed` |
| Supabase | Aktif | social_posts, media_library, geo_scans + content_packages |
| Google Sheets | Aktif | Gorsel pipeline |
| WaveSpeed AI | Planli | 15 secilmis model, maliyet kontrol |
| Krea.ai | Planli | Gorsel uretim |
| Kie.ai | Planli | Gorsel uretim |
| Pixa.com | MCP bagli | Gorsel uretim |

**Guvenlik:** Tum API key'ler `secrets.env` dosyasinda (gitignored). Kodda sifir hardcoded secret.

## Aktif Kampanya: GEO Hizmet

- **Landing:** botfusions.com/geo-hizmet
- **Google Ads:** Customer 3646875139 (Skor: 30/100, optimizasyon bekliyor)
- **Gorseller:** 2 format (1:1 kare, 9:16 dikey) + 6 maskot + 3 logo
- **Video:** GEO 20s reklam (HyperFrames, 1080x1920, MP4)
- **Sosyal Medya:** 6 platform aktif (OmniSocials API)
- **Pipeline:** `medya-gelistirme/` 6 modul hazir (Supabase SQL + Flask endpoint'leri)
- **Bekleyen:** Donusum takibi (GTM), medya pipeline Faz 1 implementasyonu
- **GitHub:** https://github.com/botfusions/aireklam

## Onemli Baglantilar

- [Google Sheet (URL Takip)](https://docs.google.com/spreadsheets/d/1XrE0F5PWNXuvtvFv8OdK9-3zr-wUhNnkP4KuKviX3os/edit)
- [Dashboard (Local)](http://localhost:8080/index.html)
- [CMO Dashboard](http://localhost:8765) — `python gsc_api_server.py` ile baslat
- Supabase: `https://supabase.turklawai.com`

---

## Oturum Hafizasi (Session Log)

> Her oturumda yapilan isler buraya eklenir. Yeni LLM baslarken bu bolumu okur.

---

### 14 Mayis 2026 — Oturum 2

**1. CMO Dashboard Tamir Plani (6 Gorev)**
- Gorev 1: Supabase tablolari — `supabase-setup.sql` + `supabase-geo-setup.sql` hazir
- Gorev 2: PageSpeed proxy — `/api/pagespeed` endpoint eklendi, CORS cozuldu
- Gorev 3: GEO MCP yolu — graceful fallback eklendi, server crash onlenuyor
- Gorev 4: Google Ads entegrasyonu — dashboard tamamen dinamik:
  - `/api/google-ads/summary` — kampanya, keyword, gunluk trend (GAQL)
  - `/api/google-ads/health` — baglanti kontrolu
  - KPI kartlari, kampanya tablosu, keyword tablosu, SVG sparkline
- Gorev 5: GA4 baglantisi — OAuth refresh token ile kuruldu:
  - `/api/ga4/summary` — trafik, kaynaklar, donusum
  - `/api/ga4/page` — sayfa trendi
  - `/api/ga4/health` — baglanti kontrolu
  - Property: 531252912 (cenk@botfusions.com OAuth)
- Gorev 6: Donusum takibi — GA4 endpoint'leri hazir, GTM manual kurulum bekliyor

**2. GA4 OAuth Flow**
- `get-ga4-token.py` — bir kerelik OAuth refresh token olusturucu
- Service account denenmedi (GA4 UI gserviceaccount.com kabul etmiyor)
- OAuth refresh token ile cozuldu

**3. SSL Certificate Fix**
- Python 3.13 (Microsoft Store) SSL hatasi -> certifi env vars ile cozuldu
- gRPC SSL handshake failure -> GA4 client gRPC'den REST API'ye yazildi

**4. Okara Gap Analizi + Multi-Tenant SaaS Plani**
- `.agents/OKARA-GAP-ANALIZ.md` — Okara.ai karsilastirma analizi
- Multi-tenant SaaS plani (5 asama): Supabase Auth → Veri Izolasyonu → Admin Panel → Musteri Self-Service → Deployment
- Fiyatlandirma: Starter ₺2.999 / Pro ₺6.999 / Enterprise ₺14.999+

**5. Yeni Skill'ler**
- `.agents/skills/marketing/` altinda 8 yeni skill (ASO, co-marketing, community, competitor-profiling, directory, linkedin-organic, youtube-organic)
- `.agents/skills/advertising/social-publisher/` — OmniSocials yayin skill'i

---

### 14 Mayis 2026 — Oturum 1

**1. CMO Dashboard Altyapisi**
- `cmo-dashboard.html` — tam CMO dashboard (Google Ads, sosyal medya, GSC, teknik SEO)
- `gsc_api_server.py` — Flask API sunucusu (port 8765)
  - GSC proxy endpoint'leri
  - OmniSocials CORS proxy (tarayici direkt API'ye erisemiyor)
  - Supabase baglantisi (social_posts, media_library tablolari)
- `supabase-setup.sql` + `supabase-geo-setup.sql` — Supabase tablo kurulumu
- **Cozulen sorunlar:**
  - OmniSocials CORS hatasi -> Flask proxy ile cozuldu
  - OmniSocials GET /posts 403 -> API publish-only, Supabase'e yonlendirildi
  - JS veri sekli uyumsuzlugu -> `json.data` -> `json.posts` duzeltildi

**2. OmniSocials Yayin Scripti**
- `yayinla.ps1` — video yukle + Instagram/Facebook/YouTube/TikTok reel + X post
- `HATA-LOG-2026-05-14.md` — dashboard hata ve cozum kayitlari

---

### 12 Mayis 2026

**1. Proje Temizlik**
- Disk: 4.4 GB -> 1.3 GB
- Git tracked: 1348 -> 503 dosya
- Silinen: canva-mcp-server, seomachine, google-cli, claude-ads, creative-engine + 7 olu kok dosya + 903 frame PNG
- Commit: `9a27fa9`

**2. SERPiq Entegrasyonu**
- Repo: https://github.com/manojahi/serpiq -> `04-araclar/serpiq/`
- Config: `~/.serpiq/config.json` (provider: anthropic, model: claude-sonnet-4-5)
- ai-seo skill v2.1.0'a SERPiq bolumu eklendi
- Bekleyen: `npx serpiq auth` ile GSC OAuth

**3. LinkedIn Reklam Videosu (45s)**
- `04-araclar/remotion-kaynak/out/linkedin-ad-45s.mp4` (5.8 MB, 1920x1080)
- Pillow + FFmpeg ile render (Remotion npm SSL hatasi nedeniyle Python alternatifi)
- Renk paleti: #6366f1 violet (resimlerle uyumlu), Ken Burns zoom, slide-in animasyonlar
- Sahne yapisi: Hook (0-9s) -> Atif Ekonomisi (9-15s) -> Gecis (15-18s) -> Davranissal Zeka (18-24s) -> Makine Anlasilabilirligi (24-30s) -> Varlik Otoritesi (30-36s) -> CTA (36-45s)

**4. Klasor Duzenleme**
- `botfusions-brand-identity-poster.png` -> `02-gorseller/`
- 3 karsilastirma HTML -> `01-reklam-kopyalari/competitor-karsilastirmalar/`
- `_COP_KLASORU_SILME_ONCESI_KONTROL/` silindi

---

### 25 Nisan 2026

**1. Marketing Skills Guncellendi — claude-ads v1.4.0 -> v1.5.1**
- Kaynak: `https://github.com/AgriciDaniel/claude-ads` (6 commit gerideydi)
- Guncellenen konum: `.agents/skills/advertising/` (21 skill, tumu v1.5.1)
- Yeni gelenler: `ads-math` (PPC hesap makinesi), `ads-test` (A/B test tasarimi)

**2. Landing Page Audit — botfusions.com/geo-hizmeti**
- Genel skor: **58/100 — C sinifi**
- Rapor: `Marketing V2/GEO-Landing-Audit.md`
- Kritik: `<title>` tag eslesmiyor, testimonials zayif, fiyat ucurumu yuksek

---

*Son Guncelleme: 23 Mayis 2026 (Oturum 7) | Botfusions AI Reklam Ajansi*

---

### 23 Mayis 2026 — Oturum 7

**1. Guvenlik Denetimi ve Duzeltmeler**
- **Hardcoded secret temizligi:** 15+ dosyadan canli API anahtarlari kaldirildi
  - `gsc_api_server.py` — OMNI_KEY, SUPA_KEY → `os.getenv()` + `secrets.env`
  - `05-gsc-nocodb/get_gsc_token.py` — Google OAuth CLIENT_ID/SECRET → `os.getenv()`
  - `get-ga4-token.py` — ayni duzeltme
  - `04-araclar/seo-machine-modules/modules/google_search_console.py` — ayni duzeltme
  - 3 PowerShell scripti (`yayinla.ps1`, `geo-yayinla.ps1`, `yayinla-geo-post.ps1`) — API key → `$env:`
  - 8 dokuman dosyasindaki API key'ler `{{PLACEHOLDER}}` ile maskelendi
- **CORS:** `*` wildcard → sabit localhost origin listesi
- **Auth:** POST endpoint'lere `X-CMO-Key` middleware eklendi
- **SSRF:** `/api/geo/scan` endpoint'ine URL validation (scheme + private IP block + hostname blocklist)
- **Secrets yonetimi:** `secrets.env` (gitignored) + `.env.template` (referans sablonu)

**2. GitHub Push (Push Protection)**
- Repo: https://github.com/botfusions/aireklam
- Commit gecmisi temizlendi (orphan commit) — sifir hardcoded secret
- `.gitignore` guncellendi: tum gorseller haric tutuldu, maskotlar/logo/GEO icin istisna
- Toplam 3 commit: ana proje + hafiza/pipeline/skill'ler + maskotlar/logo

**3. Tam Proje Yuklemesi**
- `hafiza/` — Obsidian wiki (5 entity, 5 kavram, 3 karar, rakip arsivi)
- `medya-gelistirme/` — 6 modul pipeline + Supabase SQL setup
- Yeni skill'ler: ads-amazon, ads-attribution, ads-server-side-tracking, image, video, wavespeed
- Maskotlar: 6 adet (C1-C6), 3 logo, 2 GEO infografik

---

### 22 Mayis 2026 — Oturum 6

**1. GEO 20s Reklam Videosu — Tam Yayin (6 Platform)**
- Remotion ile 5 sahne reklam videosu olusturuldu (1080x1920, 20s, 9:16)
- Kullanici geri bildirimi uygulandi: arka plan isik patlamalari kaldirildi, maskot kucultuldu, yazilar buyutuldu
- Muzik: `mixkit-tech-house-vibes-130.mp3` (kullanici sagladi)
- OmniSocials ile 6 platforma yayinlandi:
  - Instagram ✅ | Facebook ✅ | TikTok ✅ | X ✅ | YouTube Reel ✅ | Pinterest ✅
- **Pinterest cozumu:** Board secimi icin top-level `"pinterest": {"board_id": "..."}` anahtari gerekiyor

**2. OmniSocials API Formatlari Guncellendi**
- `social-publisher/SKILL.md` guncellendi:
  - YouTube: `"type": "reel"` top-level anahtar (post_type degil)
  - Pinterest: `"pinterest": {"board_id": "...", "title": "...", "link": "..."}` top-level
  - Windows: `--ssl-no-revoke` curl flag zorunlu
  - Auth: `Authorization: Bearer <key>` header formati dogrulandi

**3. HyperFrames Kurulumu (Remotion Yerine)**
- HeyGen HyperFrames v0.6.36 kuruldu (`04-araclar/hyperframes/`)
- **Neden:** HTML-tabanli, build adimi yok, GSAP animasyon, 60+ hazir blok, 6-core paralel render
- **Remotion arsivlendi:** `remotion-kaynak/` → `_arsiv-remotion-kaynak/`
- GEO 20s reklami HyperFrames HTML'e cevrildi (`index.html`, 342 satir, 5 sahne, GSAP timeline)
- Render: `output/geo-reklam-20s.mp4` (2.0 MB, 1080x1920, 20s, H.264)
- **Ornek:** 3 saat (Remotion) → 30 dakika (HyperFrames) ayni video icin

**4. HyperFrames vs Remotion Karsilastirmasi**

| Ozellik | Remotion | HyperFrames |
|---------|----------|-------------|
| Format | React TSX | HTML + CSS |
| Build | Webpack gerekli | Yok |
| Animasyon | useCurrentFrame + interpolate | GSAP timeline |
| Zamanlama | Sequence from={frame} | data-start="4" data-duration="4" |
| Render | npx remotion render | npx hyperframes render (6 worker) |
| Lint | Yok | hyperframes lint |
| Hazir bilesen | 0 | 60+ blok (TikTok, harita, grafik) |

---

### 20 Mayis 2026 — Oturum 5

**1. Google Ads MCP Server — SSL + REST Cozumu**
- **Sorun:** grpcio 1.80.0 BoringSSL Windows'ta SSL sertifika dogrulayamiyor (`CERTIFICATE_VERIFY_FAILED`)
- **Cozum:** MCP server `api.py`'ye REST API fallback eklendi
  - gRPC basarisiz olursa otomatik httpx ile Google Ads REST API'ye gecer
  - `_rest_search_stream()` — GAQL sorgularini REST uzerinden calistirir
  - `_get_rest_token()` — OAuth refresh token ile access token alir
  - `server.py` — credential check try-except icine alindi
- **Config:** `claude_desktop_config.json` — `uv.exe` yerine global Python ile calistiriliyor (uv'nin .venv'inde SSL tamamen bozuk: `OPENSSL_Applink` hatasi)
- **google-ads.yaml:** `login_customer_id: 3646875139` + `transport: rest` eklendi (YAML'daki transport su an kullanilmiyor ama gelecekte desteklenebilir)
- **Dosyalar:** `04-araclar/google_ads_mcp/ads_mcp/tools/api.py`, `ads_mcp/server.py`

**2. Google Ads Canli Audit (REST API ile)**
- Botfusions (3646875139) gercek verilerle 80-check audit yapildi
- **Skor: 30/100 — F (Kritik)**
- Harcama: $2,540.87 (son 30 gun) | Donusum: 0 | Israf: $2,071 (%81.5)
- CTR: %0.03 | CPC: $47.94
- 2 kampanya (ikisi PAUSED): Website traffic-Search-1 (Search), Campaign #1 (PMax)
- 1 ad group: "Reklam grubu 1"
- 2 conversion action: AD_CALL + WEBPAGE (form) — ama 0 donusum
- Top israf: "seo bot" $285, "geo hizmeti" $272, "scalepost" $269, "chatbot" $199
- **Demo scriptleri:** `Claude ADS/live_audit_score.py`, `demo_audit_score.py`, `demo_meta_audit.py`

**3. Rakip Analizi Guncellendi**
- Semust.com eklendi (ORTA threat, SEO arac platformu, 4000+ marka)
- Toplam 16 rakip, 6 kategori
- Lighthouse Group: ORTA -> YUKSEK, ROIPUBLIC: ORTA -> ORTA-YUKSEK
- Dosya: `hafiza/rakip-arsivi/rakip-listesi.md`

**4. Claude Ads Skill Yerel Kurulum**
- 3 yeni skill eklendi: `ads-amazon`, `ads-attribution`, `ads-server-side-tracking`
- 6 Python script kopyalandi: `ads/scripts/`
- Toplam: 25 skill + 10 agent + 26 referans + 11 sektor sablonu
- Konum: `.agents/skills/advertising/`

**5. Semust Ozellik Analizi**
- 12 ozellik analiz edildi (keyword search, SERP analysis, AI Overview tracking, vb.)
- Hazirlik yuzdeleri ve oncelik siralamasi belirlendi
- Botfusions icin yapilabilirlik degerlendirmesi yapildi

---

### 15 Mayıs 2026 — Oturum 3

**GEO Varlık Optimizasyonu İçerik Paketi — Tam Yayın**

**1. İçerik**
- LinkedIn + X + Instagram + Pinterest metinleri yazıldı (turkce-insani-yazar)
- Sosyal medya metinleri: `out/geo-sosyal-medya-metinleri-2026-05-15.md`

**2. Görseller**
- GEO İnfografik: 3 format üretildi
  - `out/geo-infografik-2026-05-15.png` (1080x1350 — orijinal)
  - `out/geo-infografik-1x1-2026-05-15.png` (1080x1080 — X/IG/FB feed)
  - `out/geo-infografik-2x3-pinterest-2026-05-15.png` (1000x1500 — Pinterest)
- Araç: cairosvg (Python), Botfusions renk paleti

**3. Video**
- Yeni bileşen: `src/GEOPostVideo.tsx` (Remotion, 9:16, 45sn)
- Görseller 9:16 crop edildi (Pillow)
- Render: `npm run build:geopost` → `out/geo-post-45s.mp4`

**4. Yayın (OmniSocials)**
- Script: `yayinla-geo-post.ps1` (Supabase log dahil)
- Çağrı A (Reel): Instagram ✅ + Facebook ✅ + YouTube ✅ + TikTok ✅
- Çağrı B (Post): X ✅ + Instagram feed ✅ + Facebook feed ✅ + Pinterest ✅

**5. Onaylanan Yayın Sistemi**
- Her içerik paketi için: Video (9:16) + İnfografik (1:1 + 2:3) birlikte gönderilir
- `yayinla-geo-post.ps1` şablon olarak kullanılır — sadece dosya/metin değişir
- Supabase `social_posts` tablosuna otomatik log kaydedilir

**6. Teknik Düzeltmeler**
- OmniSocials API yanıtı `data.id` altında geliyor (`.id` değil)
- Direkt `/v1/media/upload` çalışıyor — Google Drive gerekmez
- `--ssl-no-revoke` zorunlu, Türkçe karakter metin içinde kullanılmaz
