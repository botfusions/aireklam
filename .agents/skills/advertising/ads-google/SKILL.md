---
name: ads-google
description: "Google Ads deep analysis covering Search, Performance Max, Display, YouTube, and Demand Gen campaigns. Evaluates 80 checks across conversion tracking, wasted spend, account structure, keywords, ads, and settings. Use when user says Google Ads, Google PPC, search ads, PMax, Performance Max, or Google campaign."
user-invokable: false
---

# Google Ads Deep Analysis

## Process

1. Collect Google Ads account data (export, Change History, Search Terms Report)
2. **Validate**: confirm data covers ≥30 days and includes Search Terms Report before proceeding
3. Read `ads/references/google-audit.md` for full 80-check audit
4. Read `ads/references/benchmarks.md` for Google-specific benchmarks
5. Read `ads/references/scoring-system.md` for weighted scoring
6. Evaluate all applicable checks as PASS, WARNING, or FAIL
7. **Validate**: confirm all 80 checks evaluated before calculating score
8. Calculate Google Ads Health Score (0-100)
9. Generate findings report with action plan

## What to Analyze

### Conversion Tracking (25% weight)
- Google tag (gtag.js) installed and firing on all pages
- Enhanced Conversions active (hashed first-party data)
- Consent Mode v2 implemented (required for EU/EEA)
- Conversion actions mapped correctly (primary vs secondary)
- Offline conversion import configured (for lead gen)
- Server-side tagging via GTM (recommended for accuracy)
- Attribution model: data-driven preferred (last-click as fallback only)
- Conversion lag analysis (are conversions still trickling in?)

### Wasted Spend (20% weight)
- Search Terms Report reviewed (last 30 days minimum)
- Negative keyword coverage adequate (shared lists + campaign-level)
- Display placement audit (exclude low-quality sites)
- Invalid click rate within norms (<10%)
- Broad Match only used with Smart Bidding (NEVER without it)
- Brand/non-brand campaigns separated
- Geographic targeting precise (no wasted international spend)

**Negative Keyword Rules (critical: bad negatives kill campaigns):**
- NEVER suggest Broad Match negatives unless explicitly justified; they block too broadly
- Default to **Exact Match** `[keyword]` for specific irrelevant queries
- Use **Phrase Match** `"keyword"` for irrelevant intent patterns
- Source negatives from actual Search Terms Report irrelevant queries, NOT guesses
- Group into themed lists: Informational (how-to, DIY, what is), Job-seeker (jobs, careers, salary), Competitor (only if intentionally excluded), Free-intent (free, crack, torrent)
- Recommend **Shared Negative Lists** at the account level, not just campaign-level
- Review existing negatives for over-blocking (are any negatives accidentally blocking converting queries?)

### Account Structure (15% weight)
- Campaign-level organization follows business logic
- Ad groups themed tightly (15-20 keywords max per group)
- RSA ad groups have ≥3 active ads
- PMax campaigns structured correctly (asset groups, signals)
- SKAGs evaluated (migrate to themed groups if present)
- Campaign labels/naming conventions consistent

### Keywords (15% weight)
- Match type strategy appropriate (Exact → Phrase → Broad progression)
- Quality Score distribution (aim ≥7 average)
- Low QS keywords flagged (<5 = FAIL, 5-6 = WARNING)
- Keyword cannibalization check (same keywords in multiple campaigns)
- Impression share tracked for top keywords
- Keyword bid adjustments set for devices/locations/audiences

### Ads (15% weight)
- RSA: ≥8 unique headlines, ≥3 descriptions per ad group
- RSA: Ad Strength puanı tuzak — "Excellent" puan performansı garanti etmez. Gerçek CTR/CPA verisine göre karar ver (Optmyzr 2026, 1M+ RSA analizi)
- Pin stratejisi: Kısmi pinleme tam pinlemeden %40 daha yüksek CTR, %58 daha düşük CPA sağlar
  - ✅ DOĞRU: 1-2 kritik başlık pinle, kalan 13+ başlığı Google'a bırak
  - ❌ YANLIŞ: 4'ten fazla başlık pinlemek — makine öğrenmesini boğar, tek kombinasyona kilitler
  - ❌ YANLIŞ: Hiç pinlememek — marka adı 3-4. sırada kalabilir
  - **Standart kural**: Marka adı → Pozisyon 1'e pinle | USP/CTA → Pozisyon 3'e pinle (opsiyonel) | Kalan tüm başlıklar serbest
- Ad extensions: sitelinks (≥4), callouts (≥4), structured snippets, image
- Dynamic keyword insertion used appropriately
- Ad copy includes CTA, value proposition, differentiators

### Settings (10% weight)
- ECPC (Enhanced CPC) flagged as deprecated. Migrate to full Smart Bidding (tCPA/tROAS/Maximize)
- Bid strategy appropriate for campaign maturity and goals
- Budget pacing: no campaigns limited by budget (unless intentional)
- Ad schedule aligned with business hours/conversion patterns
- Device bid adjustments set based on performance data
- Location targeting: "Presence" not "Presence or Interest"
- Network settings: Search Partners reviewed, Display opt-out for Search

## GAQL & Data Accuracy

Before analyzing data, read `ads/references/gaql-notes.md` for known GAQL field incompatibilities,
deduplication patterns, and filter scope best practices. Key rules:

- Deduplicate keywords by `(ad_group_id + keyword_text + match_type)` before any analysis
- Only analyze ENABLED campaigns and ad groups (exclude paused/removed)
- Filter to keywords with impressions > 0 for theme coherence checks (G03)
- Apply legacy BMM heuristic: BROAD + Manual CPC = legacy BMM, not intentional broad (G17)
- Only flag wasted spend on terms with >$10 spend AND 0 conversions (G16)
- Count shared negative keyword lists alongside campaign-level negatives (G14/G15)

## Google Ads MCP Integration (Optional)

For automated data collection, connect the [Google Ads MCP server](https://github.com/googleads/google-ads-mcp):

- **Tools available**: `search` (GAQL queries), `list_accessible_customers`
- **Setup**: Configure in `.mcp.json` or Claude Code MCP settings
- **Customer ID**: Extract from CLAUDE.md under Accounts > Google Ads, or ask the user
- **Fallback**: If MCP is not configured, fall back to manual data export (the default workflow)

When MCP is available, use it to pull Search Terms Reports, keyword data, conversion actions,
and campaign structure automatically instead of requiring manual exports.

## PMax Deep Dive

If Performance Max campaigns exist, additionally evaluate:
- Asset group diversity (text, images, video, feeds)
- Audience signals configured (custom segments, lists, demographics)
- URL expansion settings reviewed (opt-out of irrelevant pages)
- Brand exclusions applied (prevent cannibalizing brand search), available for all advertisers
- Campaign-level negative keywords now available for ALL advertisers
- Search themes utilized (2024 feature)
- Final URL expansion: enabled or disabled with justification
- Insights tab reviewed (search categories, audience segments)

## AI Max for Search (2026)

AI Max layers broad match + keywordless targeting on existing Search campaigns.
14% avg conversion lift. DSA likely consolidated into AI Max Q2 2026.
Requires strong negative keyword lists.

If AI Max for Search is available/active:
- Broad Match + AI Max integration evaluated
- Auto-generated headline performance monitored
- Search term categories reviewed for relevance
- Budget impact assessed (AI Max can shift spend)
- Negative keyword lists reviewed for completeness (AI Max broadens reach significantly)
- DSA migration path assessed (consolidation expected Q2 2026)

## Demand Gen Campaigns

Replaced Video Action Campaigns (April 2026). Video + image = 20% more conversions.
Frequency capping NOT supported.

If Demand Gen campaigns exist, evaluate:
- Video + image asset mix present (combined format drives 20% more conversions)
- Audience signals configured (custom segments, lookalikes)
- Conversion tracking aligned with upper/mid-funnel goals
- Note: frequency capping is not available. Monitor reach vs frequency manually

## Marka Koruma & Pazaryeri Kannibalizasyon Kontrolü

**Her yeni müşteri onboarding'inde zorunlu kontrol:**

Organik 1. sırada olsan bile marka aramalarının üstünde rakipler veya pazaryerleri (Trendyol, Hepsiburada, Amazon TR, N11) reklam verebilir. Bu "sessiz kayıp" çoğu reklamveren tarafından fark edilmez.

### Tespit Adımları
1. Auction Insights raporunu çek → marka arama terimlerinde kimler görünüyor?
2. Search Terms Report'ta `[marka adı]` aramalarını filtrele → pazaryeri yönlendirmesi var mı?
3. Impression Share hesapla → marka aramasında rakipler / pazaryerleri ne kadar pay alıyor?

### Çözüm: İki Kampanya Modeli

**Kampanya 1 — Marka Koruma**
- Hedef: `[marka]`, `[marka] + yorumlar`, `[marka] + iletişim`, `[marka] + fiyat`
- Eşleme: Tam eşleme (Exact Match) ile başla
- Bütçe: Günlük 150-300 TL yeterli (marka araması düşük hacimli ama yüksek intent)
- Amaç: Kendi sponsorlu reklamın organik sıranın üstüne çıkarak pazaryeri reklamını aşağı iter
- Kurulum notu: "Hedef olmadan devam et" seç — Satışlar hedefi seçilirse Google PMax'e yönlendirir

**Kampanya 2 — Pazaryeri Modifier**
- Hedef: `[marka] + trendyol`, `[marka] + hepsiburada`, `[marka] + indirim kodu`
- Reklam metni: "Resmi sitede %X daha uygun" → kendi sitene yönlendir
- Dikkat: Pazaryeri isimlerini keyword olarak hedefleyebilirsin ama reklam METNİNDE yazamazsın (Google trademark politikası)
- ROAS'ı 30 gün izle; "indirim kodu", "kupon" gibi düşük intent aramaları dışla

### Başarı Göstergesi
Auction Insights'ta pazaryerlerinin marka aramasındaki gösterim payı 2 hafta içinde %30-40'tan %2-5'e düşmeli.

### CRM Kaybı Hesabı (Müşteriye Göster)
```
Pazaryerinden geçen aylık satış × ortalama komisyon oranı = direkt komisyon kaybı
+ Pazaryerinde kalan müşteri verisi = remarketing havuzu kaybı (12 ay boyunca)
```

## Key Thresholds

| Metric | Pass | Warning | Fail |
|--------|------|---------|------|
| Quality Score (avg) | ≥7 | 5-6 | <5 |
| CTR (Search) | ≥6.66% | 3-6.66% | <3% |
| CVR (Search) | ≥7.52% | 3-7.52% | <3% |
| CPC (Search) | ≤$5.26 | $5.26-8.00 | >$8.00 |
| Wasted Spend | <10% | 10-20% | >20% |
| Ad Strength | Good+ | Average | Poor |
| Invalid Clicks | <5% | 5-10% | >10% |

## Output

### Google Ads Health Score

```
Google Ads Health Score: XX/100 (Grade: X)

Conversion Tracking: XX/100  ████████░░  (25%)
Wasted Spend:        XX/100  ██████████  (20%)
Account Structure:   XX/100  ███████░░░  (15%)
Keywords:            XX/100  █████░░░░░  (15%)
Ads:                 XX/100  ████████░░  (15%)
Settings:            XX/100  ██████████  (10%)
```

### Deliverables
- `GOOGLE-ADS-REPORT.md`: Full 80-check findings with pass/warning/fail
- Wasted spend estimate (monthly $ value)
- Quick Wins sorted by impact
- PMax-specific recommendations (if applicable)
- Keyword health matrix with QS, CTR, CVR per keyword group
