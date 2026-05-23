# Botfusions AI Reklam Ajansi — Gelisim Plani

**Tarih:** 10 Nisan 2026
**Durum:** Planlama asamasinda
**Hedef:** Mevcut agentic sistemi paketleyip firmalara SaaS olarak sunmak

---

## 1. MEVCUT DURUM

### Elimizdeki Altyapi

| Bilesen | Sayi | Durum |
|---------|------|-------|
| Marketing Skill | 35 | Hazir |
| SEO Machine Komutu | 22 | Hazir |
| Claude Ads Komutu | 13 | Hazir |
| SEO Agent | 11 | Hazir |
| Claude Ads Audit Agent | 10 | Hazir |
| Python Analiz Modulu | 25 | Hazir |
| MCP Sunucu | 2 | Hazir (Google Ads, TrueClicks) |
| Context Sablonu | 9 | Hazir (doldurulmali) |

### Eksikler

| Eksik | Aciklama |
|-------|----------|
| Google Ads Basic Access | Developer Token onayi bekleniyor (1-3 gun) |
| Canva Entegrasyonu | Composio endpoint bozuk, alternatif gerekli |
| Pixa MCP | API key bekleniyor |
| Context dosyalari | Botfusions bilgileriyle doldurulmali |
| Python API key'leri | GA4, GSC, DataForSEO credentials |

---

## 2. URUN VIZYONU

### Ne insa ediyoruz?

**Self-service AI Reklam Agent Platformu** — Bir firma LLM koyar, kendi Google Ads'ini baglar, agent otomatik reklam yonetir.

### 2 Farkli Urun Modeli

#### Model A: SaaS Platform (Firma kendi LLM'ini koyar)

```
Firma → Kayit olur → API key'ini girer (Claude/GPT)
      → Google Ads OAuth ile baglar
      → Agent otomatik calisir
      → Dashboard'dan izler + onaylar
```

**Gelir modeli:** Aylik platform ucreti (2.000 - 10.000 TL)

**Avantaj:** Dusuk maliyet, olceklenebilir
**Dezavantaj:** Firma teknik bilgiye ihtiyac duyar

#### Model B: Managed Service (Biz her seyi saglariz)

```
Firma → Kayit olur → Brief gonderir
      → Bizim LLM'imiz calisir (Claude API)
      → Sonuclari dashboard'da gorur
      → Onaylar veya duzeltme ister
```

**Gelir modeli:** Paket ucreti + token maliyeti (5.000 - 35.000 TL/ay)

**Avantaj:** Firma icin sifir teknik bilgi gerekiyor
**Dezavantaj:** Bizim icin maliyet var (LLM API)

#### Model C: Hibrit (Onerilen)

```
Kucuk firmalar → Managed Service (basit)
Buyuk firmalar → SaaS (kendi LLM, daha fazla kontrol)
```

---

## 3. MIMARI TASARIM

### Genel Mimari

```
Katman 1: MUSTERI PORTALI (Next.js + Supabase)
  ├── Giris/Kayit
  ├── Dashboard (metrikler, kampanyalar)
  ├── Brief Formu
  ├── Rapor Goruntuleme
  ├── Onay/Red mekanizmasi
  └── Fatura/Odeme

Katman 2: AGENT ORCHESTRATOR (Python/FastAPI)
  ├── LLM Router (Claude/GPT/Gemini secimi)
  ├── Skill Dispatcher (35 skill'i cagirma)
  ├── Workflow Engine (komut zincirleri)
  ├── Memory Manager (musteri bazli kontekst)
  └── Queue System (brief kuyrugu)

Katman 3: AI MOTORU (Mevcut Sistem)
  ├── 35 Marketing Skill
  ├── 22 SEO Machine Komutu
  ├── 13 Claude Ads Komutu
  ├── 11 SEO Agent
  ├── 10 Ads Audit Agent
  └── 25 Python Analiz Modulu

Katman 4: DIS BAGLANTILAR (MCP + API)
  ├── Google Ads API
  ├── TrueClicks API
  ├── Meta Ads API
  ├── GA4 / GSC
  ├── DataForSEO
  ├── WordPress REST API
  └── Gorsel uretim (Gemini/Pixa)

Katman 5: VERI (Supabase)
  ├── Auth (kullanici yonetimi)
  ├── Database (musteri, brief, kampanya, rapor)
  ├── Storage (gorseller, PDF'ler)
  ├── Edge Functions (AI tetikleyiciler)
  └── Realtime (canli bildirimler)
```

---

## 4. TEKNOLOJI YIGINI

| Katman | Teknoloji | Aciklama |
|--------|-----------|----------|
| **Frontend** | Next.js 14+ (App Router) | React tabanli dashboard |
| **UI** | Tailwind CSS + shadcn/ui | Modern, responsive tasarim |
| **Backend** | Supabase | Auth, DB, Storage, Edge Functions |
| **AI Orchestrator** | Python FastAPI | Skill dispatcher, workflow engine |
| **LLM** | Claude API (Anthropic) | Ana AI motor |
| **Database** | PostgreSQL (Supabase) | Multi-tenant veri tabani |
| **Auth** | Supabase Auth + OAuth | Google Ads OAuth flow |
| **Deployment** | Vercel (frontend) + Supabase (backend) | Production ortam |
| **Container** | Docker | Agent orphanic icin |

---

## 5. MUSTERI PORTALI SAYFALARI

### 5.1 Giris ve Kayit

| Sayfa | Yol | Ozellikler |
|-------|-----|------------|
| Giris | `/giris` | E-posta + sifre, Google OAuth |
| Kayit | `/kayit` | Firma bilgileri, paket secimi |
| Sifre Sifirla | `/sifre-sifirla` | E-posta ile sifirlama |

### 5.2 Dashboard

| Sayfa | Yol | Ozellikler |
|-------|-----|------------|
| Ana Panel | `/dashboard` | Toplam metrikler, son kampanyalar, bekleyen onaylar |
| Kampanyalar | `/kampanyalar` | Tum kampanyalar listesi, filtreleme |
| Kampanya Detay | `/kampanya/[id]` | Metrikler, kopyalar, gorseller, zaman cizelgesi |

### 5.3 Brief ve Uretim

| Sayfa | Yol | Ozellikler |
|-------|-----|------------|
| Yeni Brief | `/brief/yeni` | Form: hedef, butce, platform, referans |
| Brief Detay | `/brief/[id]` | Uretim durumu, sonuclar |
| Onay Kuyrugu | `/onaylar` | Bekleyen kopya/gorsel onaylari |

### 5.4 Raporlama

| Sayfa | Yol | Ozellikler |
|-------|-----|------------|
| Raporlar | `/raporlar` | Haftalik/aylik rapor listesi |
| Rapor Detay | `/rapor/[id]` | Grafikler, oneriler, anomaly analizi |
| Rakip Analizi | `/rakip-analiz` | Rakip denetim sonuclari |

### 5.5 Ayarlar

| Sayfa | Yol | Ozellikler |
|-------|-----|------------|
| Profil | `/ayarlar/profil` | Firma bilgileri |
| Baglantilar | `/ayarlar/baglantilar` | Google Ads OAuth, Meta baglantisi |
| API Key | `/ayarlar/api-key` | LLM API key girisi (SaaS modeli) |
| Faturalar | `/ayarlar/faturalar` | Fatura gecmisi, odeme |

### 5.6 Admin Paneli

| Sayfa | Yol | Ozellikler |
|-------|-----|------------|
| Admin Dashboard | `/admin` | Tum musteriler, toplam gelir |
| Musteri Yonetimi | `/admin/musteriler` | Musteri listesi, paket atama |
| Brief Yonetimi | `/admin/briefs` | Brief kuyrugu, AI'a gonder |
| Uretim Takibi | `/admin/uretim` | Aktif uretim, agent durumu |
| Finans | `/admin/finans` | Fatura, odeme, MRR takibi |

---

## 6. AGENT ORCHESTRATOR TASARIMI

### 6.1 LLM Router

```
Gelen brief → LLM Router → En uygun skill/komut zinciri

Ornek:
  Brief: "Google Ads kampanyasi ac, restoran promosyonu"
  Router → paid-ads skill → ad-creative skill → Google Ads MCP

  Brief: "Blog yaz, SEO optimizeli"
  Router → /research komutu → /write komutu → seo-optimizer agent
```

### 6.2 Skill Dispatcher

```python
# Orchestration mantigi
class AgentOrchestrator:
    def __init__(self, customer_id):
        self.customer = get_customer(customer_id)
        self.context = load_context(customer_id)  # Firma bazli kontekst
        self.mcp_clients = connect_mcps(customer_id)  # Firma bazli MCP

    async def process_brief(self, brief):
        # 1. Brief'i analiz et
        intent = await self.analyze_intent(brief)

        # 2. Uygun skill zincirini olustur
        chain = self.build_skill_chain(intent)

        # 3. Sirayla calistir
        results = []
        for skill in chain:
            result = await self.execute_skill(skill, brief, self.context)
            results.append(result)

        # 4. Sonuclari kaydet
        await self.save_results(results)

        # 5. Musteriye bildir
        await self.notify_customer(results)
```

### 6.3 Multi-Tenant Yapı

```
Her firma icin izole alan:

tenant_12345/
├── context/
│   ├── brand-voice.md       ← Firma ozel marka sesi
│   ├── features.md           ← Firma urun ozellikleri
│   ├── target-keywords.md    ← Firma hedef kelimeler
│   └── competitor-analysis.md
├── credentials/
│   ├── google-ads.yaml      ← Firma Google Ads kimlik
│   └── .env                  ← Firma API key'leri
├── output/
│   ├── drafts/               ← Uretilen taslaklar
│   ├── reports/              ← Raporlar
│   └── assets/               ← Gorseller, videolar
└── memory/
    └── preferences.json      ← Ogrencen tercihler
```

---

## 7. SERVIS PAKETLERI (Urun Fiyatlama)

### Tier 1: Baslangic — 5.000 TL/ay

| Ozellik | Detay |
|---------|-------|
| Kampanya | 1 Google Ads kampanya |
| Reklam Kopyasi | 10 adet (AI uretimi) |
| Rapor | Haftalik performans raporu |
| Landing Page | 1 inceleme |
| Destek | E-posta (48 saat yanit) |
| Token Limit | 50.000 token/ay |

### Tier 2: Profesyonel — 15.000 TL/ay

| Ozellik | Detay |
|---------|-------|
| Kampanya | 3 kampanya (Google + Meta) |
| Reklam Kopyasi | 30 adet + gorsel onerileri |
| Rakip Analizi | 1 rakip kreatif denetimi |
| Rapor | Gunluk rapor + anomali uyari |
| A/B Test | Yonetim + analiz |
| Blog Icerik | 4 makale/ay (SEO optimizeli) |
| Destek | E-posta + chat (24 saat yanit) |
| Token Limit | 200.000 token/ay |

### Tier 3: Kurumsal — 35.000 TL/ay

| Ozellik | Detay |
|---------|-------|
| Kampanya | 5+ kampanya (tum platformlar) |
| Reklam Kopyasi | Sinirsiz |
| Rakip Analizi | 3 rakip denetimi |
| Rapor | Gunluk + ozel raporlar |
| SEO Icerik | 8 makale/ay |
| Donusum Takibi | GA4 + GTM kurulumu |
| Destek | Oncelikli + aylik stratejitoplantisi |
| Token Limit | 500.000 token/ay |

---

## 8. GELISIM FAZLARI

### Faz 1: MVP — Temel Portal (Hafta 1-2)

**Hedef:** Müşteri kayıt olsun, brief gönderebilsin

- [ ] Next.js projesi oluştur
- [ ] Supabase bağlantısı kur
- [ ] Auth sistemi (e-posta + Google OAuth)
- [ ] Kayıt formu (firma bilgileri + paket seçimi)
- [ ] Dashboard ana sayfa (temel)
- [ ] Brief formu (tek sayfa)
- [ ] Brief'leri Supabase'e kaydetme

**Teknoloji:** Next.js 14, Supabase Auth, Tailwind, shadcn/ui

### Faz 2: Agent Orchestrator (Hafta 3-4)

**Hedef:** Brief → AI motoru → sonuç

- [ ] Python FastAPI orchestrator servisi
- [ ] LLM Router (Claude API entegrasyonu)
- [ ] Skill Dispatcher (mevcut 35 skill'i çağırma)
- [ ] Multi-tenant context yönetimi
- [ ] Brief → skill zinciri eşleştirme
- [ ] Sonuçları Supabase'e kaydetme
- [ ] Müşteriye bildirim (e-posta)

**Teknoloji:** Python FastAPI, Anthropic SDK, Supabase client

### Faz 3: Ajans Paneli (Hafta 5)

**Hedef:** Admin müşterileri ve üretimi yönetebilsin

- [ ] Admin giriş (role-based)
- [ ] Müşteri listesi + detay sayfası
- [ ] Brief → "AI ile üret" butonu
- [ ] Üretim kuyruğu takibi
- [ ] Sonuç teslimi + müşteri onay akışı
- [ ] Temel finans (fatura oluşturma)

### Faz 4: Google Ads Entegrasyonu (Hafta 6)

**Hedef:** Dashboard'dan Google Ads veri çekme ve yönetim

- [ ] Google Ads OAuth flow (müşteri kendi hesabını bağlar)
- [ ] TrueClicks MCP → dashboard'a veri aktarma
- [ ] Kampanya metrikleri gösterimi (grafikler)
- [ ] Otomatik haftalık rapor üretimi
- [ ] Rapor şablonları (HTML/PDF)

### Faz 5: Otomasyon ve Finans (Hafta 7)

**Hedef:** Tam otomatik çalışma + ödeme sistemi

- [ ] Cron job: Otomatik haftalık rapor
- [ ] Cron job: Anomali tespiti (bütçe aşımı)
- [ ] E-posta bildirimleri (Supabase Edge Functions)
- [ ] Ödeme sistemi (Iyzico veya Stripe)
- [ ] Fatura oluşturma (PDF)
- [ ] SaaS modeli: Müşteri kendi API key'ini girsin

### Faz 6: Görsel ve İçerik Pipeline (Hafta 8)

**Hedef:** Dashboard'dan görsel üretim + blog yazma

- [ ] Görsel üretim butonu (Gemini/Pixa entegrasyonu)
- [ ] Blog yazma pipeline'ı (/research → /write → /optimize)
- [ ] WordPress yayınlama entegrasyonu
- [ ] Rakip analiz raporu görüntüleme
- [ ] Görsel galeri + onay mekanizması

### Faz 7: Production ve Lansman (Hafta 9-10)

**Hedef:** Canlıya alma + ilk müşteriler

- [ ] Domain: ajans.botfusions.com
- [ ] SSL + Vercel deployment
- [ ] Supabase production ortamı
- [ ] Monitoring (Sentry, analytics)
- [ ] Landing page: botfusions.com/ai-reklam-ajansi
- [ ] İlk 3 müşteri ile beta test
- [ ] Geri bildirim → iterasyon

### Faz 8: Bilgi Bankası — claude-obsidian (Hafta 11-12)

**Hedef:** Kalıcı, bileşik bilgi bankası (Karpathy LLM Wiki pattern)

**Kaynak:** `github.com/AgriciDaniel/claude-obsidian`

**Neden gerekli:**
- Her müşterinin kendi wiki vault'u olur → marka bilgisi birikir
- Rakip araştırma bulguları kaybolmaz → `ingest` ile kalıcı olur
- `/autoresearch` ile otonom araştırma döngüsü çalışır
- Oturumlar arası "hot cache" ile bağlam korunur
- Obsidian graph view ile görsel bilgi ağı

- [ ] `claude-obsidian` reposunu klonla → `04-araclar/claude-obsidian/`
- [ ] Obsidian vault yapısını kur (wiki/, wiki/concepts/, wiki/entities/, wiki/sources/)
- [ ] Mode C (Business) aktif et → proje wiki, rekabetçi istihbarat
- [ ] `setup-vault.sh` çalıştır → graph view, CSS snippet'ler, dashboard
- [ ] Local REST API plugin kur → MCP entegrasyonu
- [ ] `context/` dosyalarını wiki'ye ingest et → marka bilgisi aktarımı
- [ ] CLAUDE.md'e wiki cross-reference ekle
- [ ] Her müşteri için izole vault alanı oluştur (multi-tenant)
- [ ] `/autoresearch` program.md'i pazarlama odaklı yapılandır
- [ ] `/canvas` ile görsel bilgi panelleri oluştur
- [ ] Obsidian Git plugin → 15 dakikada bir otomatik commit
- [ ] Dashboard'da wiki erişimi (müşteri kendi marka bilgisini görsün)

**Teknoloji:** Obsidian + Local REST API + mcp-obsidian + Templater

**Kullanım Senaryoları:**

| Senaryo | Komut | Sonuç |
|---------|-------|-------|
| Rakip site analizini kaydet | `ingest [URL]` | 8-15 wiki sayfası, cross-ref'ler |
| Oturum sonunda not al | `/save` | Konuşma wiki sayfası olur |
| Yeni konu araştır | `/autoresearch [konu]` | Otonom ara→oku→sentezle→dosyala |
| Marka bilgisini sorgula | `/wiki` | Hot cache → index → detay |
| Wiki sağlığını kontrol et | `lint the wiki` | Orphan sayfalar, kırık linkler |
| Görsel panel | `/canvas` | Obsidian canvas ile bilgi haritası |

**Dosya Yapısı:**
```
04-araclar/claude-obsidian/
├── wiki/
│   ├── hot.md              ← Oturumlar arası bağlam (hot cache)
│   ├── index.md            ← Master katalog
│   ├── log.md              ← İşlem günlüğü
│   ├── overview.md         ← Yönetici özeti
│   ├── concepts/           ← Pazarlama kavramları
│   ├── entities/           ← Rakipler, müşteriler, platformlar
│   ├── sources/            ← İnjest edilen kaynaklar
│   └── meta/
│       └── dashboard.base  ← Bases dashboard
├── _templates/             ← Templater şablonları
├── .raw/                   ← Ham kaynak belgeler
├── skills/                 ← wiki, ingest, query, lint, save, autoresearch, canvas
├── agents/                 ← wiki-ingest.md, wiki-lint.md
├── commands/               ← /wiki, /save, /autoresearch, /canvas
└── WIKI.md                 ← Tam şema referansı
```

---

## 9. VERI TABANI SEMASI

```sql
-- Kullanicilar ve yetkiler
users (
  id UUID PRIMARY KEY,
  email TEXT,
  full_name TEXT,
  role ENUM('musteri', 'admin', 'superadmin'),
  created_at TIMESTAMP
)

-- Firmalar
companies (
  id UUID PRIMARY KEY,
  name TEXT,
  slug TEXT UNIQUE,           -- botfusions.com/ajans/firma-adi
  tier ENUM('baslangic', 'profesyonel', 'kurumsal'),
  google_ads_customer_id TEXT,
  llm_api_key TEXT ENCRYPTED,  -- SaaS modeli icin
  status ENUM('aktif', 'beklemede', 'iptal'),
  created_at TIMESTAMP
)

-- Firma kullanicilari
company_users (
  user_id UUID REFERENCES users(id),
  company_id UUID REFERENCES companies(id),
  role ENUM('owner', 'editor', 'viewer'),
  PRIMARY KEY (user_id, company_id)
)

-- Brief'ler
briefs (
  id UUID PRIMARY KEY,
  company_id UUID REFERENCES companies(id),
  title TEXT,
  description TEXT,
  target_audience TEXT,
  budget DECIMAL,
  platforms TEXT[],             -- ['google', 'meta', 'linkedin']
  goals TEXT[],                 -- ['trafik', 'donusum', 'marka']
  reference_urls TEXT[],
  status ENUM('taslak', 'gonderildi', 'uretimde', 'tamamlandi'),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)

-- Kampanyalar
campaigns (
  id UUID PRIMARY KEY,
  company_id UUID REFERENCES companies(id),
  brief_id UUID REFERENCES briefs(id),
  name TEXT,
  platform ENUM('google', 'meta', 'linkedin', 'tiktok', 'microsoft'),
  status ENUM('taslak', 'aktif', 'duraklatildi', 'tamamlandi'),
  start_date DATE,
  end_date DATE,
  budget DECIMAL,
  metrics JSONB,               -- {impressions, clicks, cost, conversions, ctr}
  updated_at TIMESTAMP
)

-- Reklam Kopyalari
ad_copies (
  id UUID PRIMARY KEY,
  campaign_id UUID REFERENCES campaigns(id),
  headline TEXT,
  primary_text TEXT,
  description TEXT,
  cta TEXT,
  platform ENUM('google_rsa', 'meta_feed', 'linkedin_sponsored'),
  status ENUM('uretiliyor', 'beklemede', 'onaylandi', 'reddedildi', 'yayinda'),
  customer_notes TEXT,
  approved_at TIMESTAMP,
  created_at TIMESTAMP
)

-- Gorseller ve Videolar
assets (
  id UUID PRIMARY KEY,
  campaign_id UUID REFERENCES campaigns(id),
  type ENUM('gorsel', 'video'),
  format ENUM('1:1', '16:9', '9:16', 'mp4', 'carousel'),
  url TEXT,
  prompt TEXT,                 -- AI uretimi icin kullanilan prompt
  status ENUM('uretiliyor', 'beklemede', 'onaylandi', 'reddedildi'),
  created_at TIMESTAMP
)

-- Raporlar
reports (
  id UUID PRIMARY KEY,
  company_id UUID REFERENCES companies(id),
  campaign_id UUID REFERENCES campaigns(id),
  type ENUM('gunluk', 'haftalik', 'aylik', 'ozel'),
  period_start DATE,
  period_end DATE,
  data JSONB,                  -- Metrikler, grafik verisi
  summary TEXT,                -- AI uretimi ozet
  recommendations TEXT[],      -- Oneriler
  score INTEGER,               -- Kampanya saglik skoru (0-100)
  anomalies TEXT[],            -- Tespit edilen anomaliler
  created_at TIMESTAMP
)

-- Rakip Analizleri
competitor_audits (
  id UUID PRIMARY KEY,
  company_id UUID REFERENCES companies(id),
  competitor_name TEXT,
  competitor_url TEXT,
  analysis JSONB,              -- 6 boyutlu analiz sonuclari
  gaps TEXT[],                 -- Boshluk firsatlari
  steal_ideas TEXT[],          -- "Bunu Cal" fikirleri
  created_at TIMESTAMP
)

-- Faturalar
invoices (
  id UUID PRIMARY KEY,
  company_id UUID REFERENCES companies(id),
  amount DECIMAL,
  tier ENUM('baslangic', 'profesyonel', 'kurumsal'),
  period_start DATE,
  period_end DATE,
  status ENUM('bekliyor', 'odendi', 'gecikmiş', 'iptal'),
  pdf_url TEXT,
  due_date DATE,
  paid_at TIMESTAMP,
  created_at TIMESTAMP
)

-- Agent Islem Gunlugu
agent_logs (
  id UUID PRIMARY KEY,
  company_id UUID REFERENCES companies(id),
  brief_id UUID REFERENCES briefs(id),
  skill_used TEXT,             -- Hangi skill calisti
  input JSONB,                 -- Girdi
  output JSONB,                -- Cikti
  tokens_used INTEGER,
  cost_usd DECIMAL,
  duration_ms INTEGER,
  status ENUM('basarili', 'basarisiz', 'kismi'),
  created_at TIMESTAMP
)
```

---

## 10. ONEMLI KARARLAR (Karar Verilmesi Gerekenler)

| # | Karar | Secenekler | Oneri |
|---|-------|-----------|-------|
| 1 | **LLM Saglayici** | Claude API / OpenAI / kendi model | Claude API (mevcut sistem uyumlu) |
| 2 | **Odeme Sistemi** | Iyzico / Stripe / PayTR | Iyzico (Turkiye odakli) |
| 3 | **Hosting** | Vercel + Supabase / AWS / GCP | Vercel + Supabase (baslangic icin) |
| 4 | **Multi-tenant** | Schema-based / DB-based / Row-based | Row Level Security (Supabase RLS) |
| 5 | **Agent Calisma Sekli** | Senkron / Asenkron (kuyruk) | Asenkron + bildirim |
| 6 | **Ucretlandirme** | Sabit aylik / Kullanim bazli / Hibrit | Hibrit (taban ucret + asgi token) |
| 7 | **MCP Erisimi** | Firma kendi MCP'si / Bizim MCP'ler | Baslangicta bizim MCP'ler, sonra self-service |

---

## 11. MALIYET ANALIZI

### Teknik Maliyetler (Aylik)

| Kalemler | Maliyet |
|----------|---------|
| Supabase Pro | $25 |
| Vercel Pro | $20 |
| Claude API (token) | $100-500 (musteri sayisina gore) |
| Google Ads API | Ucretsiz |
| Domain + SSL | $2 |
| Monitoring (Sentry) | $26 |
| **Toplam** | **$175-575/ay** |

### Gelir Projeksiyonu (Aylik)

| Musteri Sayisi | Ortalama Paket | Gelir |
|----------------|---------------|-------|
| 5 musteri | 10.000 TL | 50.000 TL |
| 10 musteri | 12.000 TL | 120.000 TL |
| 25 musteri | 15.000 TL | 375.000 TL |
| 50 musteri | 15.000 TL | 750.000 TL |

### BASABA (Break-even)

- Maliyet: ~$500/ay (~16.000 TL)
- 2 musteri (Baslangic paketi) ile basaba

---

## 12. RISKLER VE COZUMLER

| Risk | Ihtimal | Etki | Cozum |
|------|---------|------|-------|
| Google Ads API onayi gecikir | Yuksek | Yuksek | TrueClicks MCP ile araci cozum |
| Claude API maliyeti artar | Orta | Yuksek | Token limiti + kullanim bazli ucret |
| Musteri veri guvenligi | Dusuk | Cok Yuksek | Supabase RLS + sifreleme |
| AI uretim kalitesi dusuk | Orta | Orta | Insan onay adimi zorunlu |
| Rakip cikar (ayni urun) | Dusuk | Orta | Hizli MVP + musteri iliskisi |
| Teknik borc birikir | Yuksek | Orta | Faz bazli gelisim + test |

---

## 13. ONCELIK MATRISI

```
Acil + Onemli          Acil + Onemsiz
┌──────────────────┐   ┌──────────────────┐
│ Google Ads MCP   │   │ Gorsel uretim    │
│ TrueClicks fix   │   │ Landing page     │
│ Context doldur   │   │ Email bildirim   │
└──────────────────┘   └──────────────────┘

Onemli + Acil Degil   Onemsiz + Acil Degil
┌──────────────────┐   ┌──────────────────┐
│ Dashboard MVP    │   │ .exe paketleme   │
│ Agent Orchestr.  │   │ Mobil uygulama   │
│ Multi-tenant     │   │ API dokumantasyon│
│ claude-obsidian  │   │                  │
└──────────────────┘   └──────────────────┘
```

---

## 14. ZAMAN CIZELGESI

```
Hafta 1-2:  MVP (Musteri portal + brief)
Hafta 3-4:  Agent Orchestrator
Hafta 5:    Admin Paneli
Hafta 6:    Google Ads Entegrasyonu
Hafta 7:    Otomasyon + Finans
Hafta 8:    Gorsel + Icerik Pipeline
Hafta 9-10: Production + Lansman
Hafta 11-12: Bilgi Bankasi (claude-obsidian)

Toplam: 12 hafta (~3 ay)
```

---

## 15. BASARI METRIKLERI

| Metrik | Hedef (3 ay) | Hedef (6 ay) | Hedef (12 ay) |
|--------|-------------|--------------|---------------|
| Musteri sayisi | 5 | 15 | 50 |
| Aylik gelir | 50.000 TL | 200.000 TL | 750.000 TL |
| Musteri elde tutma | %80 | %85 | %90 |
| NPS skoru | 40+ | 50+ | 60+ |
| Kampanya basari orani | %70 | %80 | %85 |
| Token maliyet/oran | %20 | %15 | %10 |

---

*Botfusions AI Reklam Ajansi — Gelisim Plani*
*Bu dokuman bir LLM veya gelistirici tarafindan okunarak sistemin urunlestirme yol haritasi anlasilabilir.*
