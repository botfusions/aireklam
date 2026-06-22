# Botfusions AI Reklam Ajansi — Skill Manifest

> **Son Guncelleme:** Haziran 2026
> **Toplam Skill:** 78
> **Yapi Surumu:** 2.3.0

---

## Skill Kaynak Deposu

> ⚠️ **TEK KAYNAK:** Yeni skill eklerken veya güncellerken sadece **`coreyhaines31/marketingskills`** reposu kullanılır.
> Diğer repolar (`whyashthakker`, `kostja94` vb.) KULLANILMAZ.
> Detay: `.agents/API-INTEGRATIONS.md` → Bölüm 8

---

## Yeni LLM Baslangic Protokolu

Bu dosyayi okuyan herhangi bir LLM su adimlari izlemelidir:

1. **ONCELIKLE OKU:** `.agents/product-marketing-context.md` → Marka bilgisi, hedef kitle, ton
2. **SONRA BURAYI OKU:** Bu MANIFEST.md → Hangi skill'ler var, ne ise yarar
3. **ENTEGRASTYONLAR:** `.agents/API-INTEGRATIONS.md` → Hangi API'ler kurulu, nasil kullanilir
4. **ORKESTRATOR:** Root `CLAUDE.md` → Is akislari ve skill eslestirme

---

## Skill Kategorileri

### 1. Marketing (48 skill) — v2.3.0
**Konum:** `.agents/skills/marketing/`
**Amac:** Pazarlama stratejisi, icerik, donusum optimizasyonu, CMO fonksiyonlari
> ⚠️ v2.0.0'dan itibaren skill isimleri değişti. Eski isimler (paid-ads, social-content vb.) artık geçersiz.

| Skill | Aciklama | API Gereksinimi |
|-------|----------|----------------|
| ab-testing | A/B testi planlama ve uygulama | - |
| ad-creative | Google/Meta/Instagram reklam kopyasi | - |
| ads | Ucretli reklam kampanya stratejisi (eski: paid-ads) | Google Ads MCP |
| ai-seo | GEO/AEO gorunurluk, LLMO optimizasyonu | Web Search |
| analytics | GA4, GTM, donusum takibi kurulumu (eski: analytics-tracking) | GA4, GTM |
| aso | App Store Optimization denetimi (eski: aso-audit) | - |
| attribution-modeling | Pazarlama atif modelleme, kanal ROI olcumu | GA4 |
| churn-prevention | Kayip onleme ve elde tutma stratejileri | - |
| co-marketing | Ortak marka kampanyasi ve is birligi stratejisi | - |
| cold-email | B2B sicak e-posta dizileri | - |
| community-marketing | Topluluk insa, community-led growth, ambassador | - |
| competitors | Rakip karsilastirma ve istihbarat (eski: competitor-alternatives) | Web Search |
| competitor-audit | Rakip reklam kreatif denetimi | - |
| competitor-profiling | Derinlemesine rakip istihbarati (7 katman) | Web Search |
| content-strategy | Icerik stratejisi ve planlama | - |
| context-analyzer | URL'den context dosyasi olusturma | Web Search |
| copy-editing | Metin duzeltme ve guclendirme | - |
| copywriting | Pazarlama metni yazimi (Hook-Agitate-Solution-CTA) | - |
| cro | Landing page + form donusum optimizasyonu (eski: page-cro + form-cro) | - |
| customer-journey | Musteri yolculugu haritalama | - |
| customer-research | Musteri arastirmasi ve persona olusturma | - |
| directory-submissions | Yerel SEO citation insa, dizin listeleme | - |
| emails | E-posta dizileri ve drip kampanyalar (eski: email-sequence) | - |
| free-tools | Ucretsiz arac stratejisi / lead gen (eski: free-tool-strategy) | - |
| image | AI görsel üretimi (Flux, Nano Banana, Ideogram 3.0, Midjourney v7, ChatGPT Images 2.0) | - |
| influencer-marketing | Influencer/KOL stratejisi ve ROI olcum | - |
| launch | Urun lansmani ve GTM plani (eski: launch-strategy) | - |
| lead-magnets | Lead magnet olusturma (ebook, checklist) | - |
| linkedin-organic | Organik LinkedIn icerik stratejisi ve buyume | - |
| marketing-automation | Tekrar eden isleri otomatik hale getirme | n8n/Make |
| marketing-dashboard | Gunluk/haftalik performans dashboard | GA4, Google Ads |
| marketing-ideas | Pazarlama fikri ve buyume taktikleri (139 fikir) | - |
| marketing-plan | AARRR yapıli kapsamli pazarlama plani (YENİ v2.3.0) | - |
| marketing-psychology | Psikolojik pazarlama prensipleri | - |
| newsletter | E-posta bulletin ve gonderim yonetimi | - |
| onboarding | Kayit sonrasi onboarding optimizasyonu (eski: onboarding-cro) | - |
| paywalls | Paywall ve upgrade ekranlari (eski: paywall-upgrade-cro) | - |
| popups | Popup ve modal optimizasyonu (eski: popup-cro) | - |
| pr-communications | Halkla iliskiler ve kriz iletisimi | - |
| public-relations | Kazanilmis medya, basin pitchi, gazeteci outreach, PR strateji (YENİ v2.4.0) | Web Search |
| pricing | Fiyatlandirma stratejisi (eski: pricing-strategy) | - |
| product-marketing | Urun pazarlama baglam dokumani (eski: product-marketing-context) | - |
| programmatic-seo | Olcekli SEO sayfa uretimi | - |
| prospecting | B2B/SaaS nitelikli lead listesi olusturma (YENİ v2.2.0) | - |
| referrals | Referans ve ortaklik programlari (eski: referral-program) | - |
| revops | Gelir operasyonlari ve lead lifecycle | - |
| sales-enablement | Satis materyalleri ve destek | - |
| schema | JSON-LD ve yapisal veri (eski: schema-markup) | - |
| seo-audit | SEO denetimi ve teknik analiz | Web Search |
| signup | Kayit akisi optimizasyonu (eski: signup-flow-cro) | - |
| site-architecture | Site yapisi ve URL mimarisi | - |
| sms | SMS/MMS pazarlama akislari, uyum (TCPA/GDPR) (YENİ v2.1.0) | - |
| social | Sosyal medya icerigi ve planlama (eski: social-content) | - |
| social-listening | Sosyal medya dinleme ve marka izleme | - |
| video | AI video uretimi (Veo 3, Sora 2, Kling, HeyGen) | - |
| video-marketing | Video pazarlama stratejisi ve planlama | - |
| youtube-organic | YouTube kanal stratejisi, video SEO, lead gen | - |

---

### 2. Advertising (18 skill)
**Konum:** `.agents/skills/advertising/`
**Amac:** Platform bazli reklam denetimi ve optimizasyonu

| Skill | Aciklama | API Gereksinimi |
|-------|----------|----------------|
| ads | Ana reklam orkestrator (225+ kontrol) | Google Ads MCP |
| ads-apple | Apple Search Ads denetimi | Apple Ads API |
| ads-audit | Coklu platform tam denetim | Tum platform API'leri |
| ads-budget | Butce dagitimi ve bidding stratejisi | Google Ads MCP |
| ads-competitor | Rakip reklam istihbarati | Web Search |
| ads-create | Kampanya konsept ve kopya brief | - |
| ads-creative | Kreatif kalite denetimi | - |
| ads-dna | Marka DNA cikarma (web tarama) | Web Scraping |
| ads-generate | AI gorsel uretimi | Banana MCP |
| ads-google | Google Ads derin analiz (74 kontrol) | Google Ads MCP |
| ads-landing | Landing page kalite degerlendirmesi | - |
| ads-linkedin | LinkedIn Ads derin analiz (25 kontrol) | LinkedIn API |
| ads-meta | Meta/Facebook/Instagram analiz (46 kontrol) | Meta API |
| ads-microsoft | Microsoft/Bing Ads analiz (20 kontrol) | Microsoft API |
| ads-photoshoot | Urun fotografisi gelistirme | Banana MCP |
| ads-plan | Stratejik reklam planlama | - |
| ads-tiktok | TikTok Ads analiz (25 kontrol) | TikTok API |
| ads-youtube | YouTube Ads kampanya ve kreatif analiz | YouTube API |
| ads-math | PPC matematik: ROAS, CPA, bütçe, hedef hesaplama | - |
| ads-test | Reklam A/B testi kurulum ve analiz framework | - |
| ads-report | PDF müşteri raporu: Health Score (0-100), platform grafikleri, aksiyon planı | reportlab (opsiyonel) |
| social-publisher | OmniSocials API ile 11 kanala cross-posting, zamanlama, medya dağıtımı | OmniSocials API ✅ |

---

### 3. SEO (1 skill)
**Konum:** `.agents/skills/seo/`
**Amac:** SEO uzmanlik ve vaka analizleri

| Skill | Aciklama | API Gereksinimi |
|-------|----------|----------------|
| seo-expert | SEO icerik pipeline + referans vaka analizi | Web Search |

---

### 4. Video (1 skill)
**Konum:** `.agents/skills/video/`
**Amac:** Video uretimi ve Remotion entegrasyonu

| Skill | Aciklama | API Gereksinimi |
|-------|----------|----------------|
| remotion | Remotion tabanli video uretim rehberi | Node.js, Remotion |

---

### 5. Media Production (3 skill)
**Konum:** `.agents/skills/media/`
**Amac:** AI gorsel/video uretim platformlari

| Skill | Aciklama | Entegrasyon |
|-------|----------|-------------|
| krea-ai | 64+ AI modeli (Flux, Imagen, GPT Image, Veo, Kling, LoRA egitim, 22K upscale) | API (`KREA_API_TOKEN`) |
| kie-ai | Birlesik API gateway (Nano Banana Pro, Kling, Sora, Veo — en ucuz erisim) | API (`KIE_API_KEY`) |
| pixa | Claude MCP-native araclari (bg kaldir, gorsel olustur, enhance, video, nesne sil) | MCP (`mcp.pixa.com`) |
| **wavespeed** | **1.000+ AI model tek API** (GPT Image 2, Veo 3.1, Kling O3, Seedance 2.0, FLUX 2, Lyria 3 — Ana uretim platformu) | **API (`WAVESPEED_API_KEY`)** |

**Hangi platform ne zaman:**
| Senaryo | Platform |
|---------|----------|
| Hizli duzenleme (bg kaldir, nesne sil) | **Pixa** (MCP-native) |
| **Ana uretim (1.000+ model, gorsel+video+muzik)** | **WaveSpeed** (ana platform) |
| Profesyonel uretim (marka LoRA, 4K) | **Krea.ai** (64+ model) |
| Ucuz batch uretim (API pipeline) | **Kie.ai** (en dusuk maliyet) |

---

## Is Akisi Eslestirme

| Kullanici Istegi | Kullanilacak Skill |
|-----------------|-------------------|
| "Reklam kopyasi yaz" | `marketing/ad-creative` |
| "Kampanya kur / optimize et" | `marketing/paid-ads` veya `advertising/ads-google` |
| "GEO / AI'da gorunurluk" | `marketing/ai-seo` |
| "Takip / donusum kur" | `marketing/analytics-tracking` |
| "A/B testi" | `marketing/ab-test-setup` |
| "Sosyal medya icerik" | `marketing/social-content` |
| "Icerik stratejisi" | `marketing/content-strategy` |
| "Metin duzelt / guclendir" | `marketing/copywriting` |
| "Google Ads denetle" | `advertising/ads-google` |
| "Meta/Facebook reklam" | `advertising/ads-meta` |
| "Tum platformlari denetle" | `advertising/ads-audit` |
| "SEO icerik yaz" | `seo/seo-expert` |
| "Video uret" | `video/remotion` |
| "Landing page denetle" | `advertising/ads-landing` |
| "Rakip analizi" | `advertising/ads-competitor` |
| "Marka DNA cikar" | `advertising/ads-dna` |
| "Butce / ROAS / CPA hesapla" | `advertising/ads-math` |
| "Reklam A/B testi" | `advertising/ads-test` |
| "PDF rapor / müşteri sunum" | `advertising/ads-report` |
| "Sosyal medyaya yayınla / gönder" | `advertising/social-publisher` |
| "Tüm platformlara zamanla" | `advertising/social-publisher` |
| "Cross-posting yap" | `advertising/social-publisher` |
| "Gorsel uret (profesyonel)" | `media/krea-ai` |
| "Gorsel uret (ucuz batch)" | `media/kie-ai` |
| "Arka plan kaldir / hizli duzenle" | `media/pixa` |
| "Reklam gorseli olustur" | `media/pixa` veya `media/krea-ai` |
| "Urun fotografi + video" | `media/kie-ai` (pipeline) |
| "Ortak marka kampanyasi / partner" | `marketing/co-marketing` |
| "Topluluk kur / community-led growth" | `marketing/community-marketing` |
| "Rakip derinlemesine analiz et" | `marketing/competitor-profiling` |
| "App Store / Google Play optimizasyonu" | `marketing/aso-audit` |
| "Dizin listeleme / yerel SEO citation" | `marketing/directory-submissions` |
| "LinkedIn organik buyume / post yaz" | `marketing/linkedin-organic` |
| "YouTube kanal stratejisi / video SEO" | `marketing/youtube-organic` |

---

## Surum Gecmisi

| Surum | Tarih | Degisiklik |
|-------|-------|------------|
| 1.0.0 | Nisan 2026 | Ilki yapi: 54 skill kategorize edildi, MANIFEST olusturuldu |
| 1.1.0 | Nisan 2026 | Media kategorisi eklendi (krea-ai, kie-ai, pixa) → 58 skill |
| 2.0.0 | Nisan 2026 | CMO bosluk skill'leri + context-analyzer eklendi → 68 skill. Context dosyalari Botfusions verileriyle dolduruldu. |
| 2.1.0 | Mayis 2026 | 7 yeni skill eklendi: aso-audit, co-marketing, community-marketing, competitor-profiling, directory-submissions, linkedin-organic, youtube-organic → 75 skill. coreyhaines31 + kostja94 repolarindan guncelleme. |
| 2.4.0 | Haziran 2026 | coreyhaines31/marketingskills senkronizasyonu: 20 skill v2.0.0'a guncellendi (ad-creative, churn-prevention, co-marketing, cold-email, community-marketing, competitor-profiling, content-strategy, copy-editing, copywriting, customer-research, directory-submissions, lead-magnets, marketing-ideas, marketing-psychology, programmatic-seo, revops, sales-enablement, seo-audit, site-architecture, social v2.1.0). 2 yeni skill eklendi: marketing-plan, public-relations → 81 skill. |
