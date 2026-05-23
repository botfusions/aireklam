# Botfusions CMO Dashboard — Okara.ai Gap Analizi
**Tarih:** 14 Mayıs 2026 | Referans: okara.ai

---

## Mevcut Durum Karşılaştırması

| Özellik | Okara.ai | Botfusions CMO | Durum |
|---------|----------|----------------|-------|
| Google Ads izleme | ❌ | ✅ | **Botfusions önde** |
| Sosyal medya yayın | ❌ | ✅ (6 kanal) | **Botfusions önde** |
| Media library | ❌ | ✅ (Supabase) | **Botfusions önde** |
| Google Search Console | ✅ | ⏳ (API key eksik) | Eşit sayılır |
| Google Analytics (GA4) | ✅ | ❌ | Okara önde |
| SEO Agent | ✅ | ❌ | Okara önde |
| Reddit Agent | ✅ | ❌ | Okara önde |
| LinkedIn Agent | ✅ | ❌ | Okara önde |
| X (Twitter) Agent | ✅ | ❌ | Okara önde |
| Hacker News Agent | ✅ | ❌ | Okara önde |
| GEO Agent (AI Citation) | ✅ | ❌ | Okara önde |
| Coding Agent (teknik SEO) | ✅ | ❌ | Okara önde |
| Writer Agent (uzun içerik) | ✅ | ❌ | Okara önde |
| UGC Video | ✅ | ⏳ (HyperFrames) | Yakın |
| Action Items (günlük öneriler) | ✅ | ❌ | Okara önde |
| İçerik takibi (X + Reddit) | ✅ | ❌ | Okara önde |
| Link Broker | 🔜 | ❌ | — |
| Influencer Marketplace | 🔜 | ❌ | — |

---

## Eksik Özellikler — Öncelik Sırasına Göre

### 🔴 Kritik (Hemen Yapılmalı)

#### 1. Action Items / Günlük Öneriler Paneli
Okara'nın en çok beğenilen özelliği. Her sabah:
- "Bu hafta şu keywordde fırsat var"
- "Bu post en iyi performansı gösterdi, benzerini yaz"
- "Google Ads'te şu kelime bütçe yiyor, dur"

**Nasıl yapılır:** `gsc_api_server.py`'e `/api/insights` endpoint'i + dashboard'a "Bugünün Öncelikleri" kartı.

#### 2. GA4 Entegrasyonu
GSC var ama GA4 yok. Okara her ikisini birleştiriyor.
- Hangi sayfa trafik getiriyor?
- Bounce rate, session süresi
- Dönüşüm hunisi

**Nasıl yapılır:** Service account JSON → `google-analytics-data` Python kütüphanesi.

#### 3. GEO İzleme (AI Citation Tracker)
Botfusions'ın ana hizmeti GEO ama kendi GEO'sunu takip etmiyor — ironik.
- ChatGPT, Claude, Gemini, Perplexity'de "Botfusions" ne zaman geçiyor?
- Rakipler ne zaman geçiyor?

**Nasıl yapılır:** Otomatik AI araçlarına sorgu gönder + yanıtları Supabase'e kaydet + dashboard'da göster.

---

### 🟡 Orta Öncelik (Bu Ay)

#### 4. SEO İçerik Ajanı
Kelime fırsatı bul → blog taslağı yaz → onay al → yayınla.
- GSC zaten bağlı → düşük pozisyon (4-20. sıra) keywordleri bul
- "Bu kelimede bir makale yazsak 1-3'e girebiliriz" önerisi

#### 5. LinkedIn Ajanı
Profesyonel B2B içerik üretimi.
- Haftalık 3 post taslağı
- Sektör trendi yorumları
- OmniSocials üzerinden direkt yayın

#### 6. X (Twitter) Ajanı
Thread fikirleri + kısa içerik + trend takibi.
- Günlük 1-2 tweet taslağı
- GEO konularında thread serisi

#### 7. İçerik Performans Takibi
Hangi post ne kadar iş yaptı?
- OmniSocials'ta post ID'si var → engagement verisi çek
- En iyi performans gösteren içerikleri listele
- "Bunu tekrar paylaş" önerisi

---

### 🟢 Uzun Vadeli (3+ Ay)

#### 8. Reddit Ajanı
GEO hizmeti için mükemmel kanal:
- "yapay zeka SEO" konuşmaları nereden geliyor?
- Reddit threadlerini bul → Botfusions'ı doğal şekilde tanıt

#### 9. Hacker News Ajanı
Yazılım geliştirici kitlesi → GEO'nun erken adopter'ları.
- İlgili "Show HN" / "Ask HN" threadleri
- Yorum fikirleri

#### 10. Coding Agent (Teknik SEO)
- `botfusions.com/geo-hizmet` sayfa hızı
- Schema markup eksikleri
- Otomatik düzeltme önerileri

---

## Dashboard UI Eksikleri

Okara dashboard incelemesinden:

```
Mevcut CMO tabs:
- Genel Bakış
- Google Ads
- Sosyal Medya
- İçerik
- Sağlık (PageSpeed)

Eklenecek:
+ GEO İzleme (yeni sekme)
+ Öneriler / Action Items (ana sayfaya ekle)
+ İçerik Takvimi (planlama)
+ Performans Raporu (haftalık özet)
```

---

## Hızlı Kazanımlar (Bu Hafta Yapılabilir)

### 1. PageSpeed CORS Düzeltme
`Sağlık` sekmesi çalışmıyor çünkü frontend'den direkt API çağrısı.
→ Flask'a taşı: `GET /api/pagespeed?url=...`

### 2. Günlük Özet Kartı
Dashboard açılışında basit bir kart:
```
📊 Bugün:
- Google Ads: 150₺ harcandı (dün: 145₺)
- En son post: 2 saat önce (Instagram)
- Bekleyen: 0 taslak
```

### 3. GSC Bağlantısını Tamamla
API key alınarak günlük keyword raporu dashboard'a eklenir.

---

## Karşılaştırma Özeti

**Botfusions'ın güçlü yönleri:**
- Google Ads entegrasyonu Okara'da yok
- 6 platformda direkt yayın Okara'da yok
- Türkçe içerik üretimi native
- Kendi altyapısı (Supabase, VPS) → veri sahipliği

**Okara'dan öğrenilecekler:**
- Action Items / günlük öneri sistemi → kullanıcı sadakati
- GA4 entegrasyonu → tam analitik tablo
- GEO izleme → kendi hizmeti için proof
- İçerik performans takibi → döngüyü kapat

---

---

## Multi-Tenant SaaS — CMO Dashboard Müşteri Paneli

**Hedef:** CMO Dashboard'u Botfusions müşterilerine satılan bir SaaS ürününe dönüştürmek.
Her müşteri kendi dashboard'ında kendi verisini görecek. Okara'nın onboarding akışından esinlenildi.

### Mimari Plan

```
Kullanıcı (Müşteri)
    │
    ▼
[Lambda@Edge / NGINX]
    │
    ▼
[Next.js veya Flask Frontend]  ←  Supabase Auth
    │
    ▼
[Flask API — gsc_api_server.py]
    │
    ├── Google Ads API  (müşteri bazlı Customer ID)
    ├── GSC API         (müşteri bazlı Site URL)
    ├── GA4 API         (müşteri bazlı Property ID)
    ├── OmniSocials     (müşteri bazlı hesap seti)
    └── Supabase        (customer_id ile izole veri)
```

### Aşama 1 — Supabase Auth (Önce Bu)

| Öğe | Detay |
|------|-------|
| Login ekranı | Email/şifre + Google OAuth |
| Tablo | `auth.users` (Supabase built-in) |
| Profil tablosu | `public.profiles` → role, company, avatar |
| Roller | `admin` (Botfusions) · `client` (müşteri) |

```sql
-- profiles tablosu
CREATE TABLE profiles (
  id         UUID PRIMARY KEY REFERENCES auth.users(id),
  email      TEXT,
  full_name  TEXT,
  role       TEXT DEFAULT 'client' CHECK (role IN ('admin','client')),
  company    TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Aşama 2 — Veri İzolasyonu

Tüm tablolara `customer_id` kolonu eklenir. Supabase RLS her sorguda otomatik filtre uygular.

```sql
-- social_posts, media_library, geo_scans, google_ads_cache vb.
ALTER TABLE social_posts ADD COLUMN customer_id UUID REFERENCES profiles(id);
ALTER TABLE media_library ADD COLUMN customer_id UUID REFERENCES profiles(id);
ALTER TABLE geo_scans     ADD COLUMN customer_id UUID REFERENCES profiles(id);

-- RLS: müşteri sadece kendi verisini görür
CREATE POLICY "Client sees own data" ON social_posts
  FOR SELECT USING (customer_id = auth.uid());
```

### Aşama 3 — Admin Paneli (Botfusions İç)

| Sayfa | İşlev |
|-------|-------|
| Müşteri Listesi | Tüm müşteriler + durum (aktif/pasif) |
| Müşteri Ekle | İsim, email, Google Ads CID, GSC URL, GA4 Property |
| API Key Yönetimi | Müşteri başına OmniSocials hesap seti |
| Kullanım Metrikleri | Her müşterinin API çağrı, harcama, yayın sayısı |
| Faturalandırma | Aylık ücret, kullanım bazlı veya sabit |

### Aşama 4 — Müşteri Self-Service

Müşteriler kendi panellerinde:
- Google Ads kampanya metriklerini görür
- GSC keyword performansını izler
- Sosyal medya yayınlar / planlar
- GEO skorunu kontrol eder
- Haftalık AI önerilerini okur (Action Items)

### Aşama 5 — Dağıtım & Güvenlik

| Bileşen | Teknoloji |
|---------|-----------|
| Frontend | Next.js (SSR) veya mevcut HTML + Supabase JS |
| Backend | Flask (mevcut) veya FastAPI'e geçiş |
| Veritabanı | Supabase (PostgreSQL + RLS + Auth) |
| Hosting | VPS veya Vercel + Cloudflare |
| Şifreleme | Okara'dan esinlenme: client-side AES-256-GCM (opsiyonel) |
| Domain | `dashboard.botfusions.com` veya müşteri bazlı subdomain |

### Fiyatlandırma Modeli (Taslak)

| Plan | Aylık | İçerik |
|------|-------|--------|
| Starter | ₺2.999 | 1 site, GSC + PageSpeed, temel rapor |
| Pro | ₺6.999 | 3 site, + Google Ads, GA4, sosyal medya yayın |
| Enterprise | ₺14.999+ | Sınırsız site, özel agent'lar, API erişimi |

### Geçiş Sırası

```
1. Mevcut 6 görevi tamamla (PageSpeed ✓, GEO path ✓, Google Ads ✓, Supabase ✓, GA4, Dönüşüm)
2. Supabase Auth ekle → login ekranı
3. customer_id kolonları + RLS policy'ler
4. Admin panel (müşteri CRUD)
5. Müşteri self-service panel
6. Dağıtım (VPS/Vercel + domain)
7. İlk müşteri onboarding
```

---

*Botfusions AI Reklam Ajansı · Mayıs 2026*
