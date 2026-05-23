---
name: ai-seo
description: "When the user wants to optimize content for AI search engines, get cited by LLMs, or appear in AI-generated answers. Also use when the user mentions 'AI SEO,' 'AEO,' 'GEO,' 'LLMO,' 'answer engine optimization,' 'generative engine optimization,' 'LLM optimization,' 'AI Overviews,' 'optimize for ChatGPT,' 'optimize for Perplexity,' 'AI citations,' 'AI visibility,' 'zero-click search,' 'how do I show up in AI answers,' 'LLM mentions,' or 'optimize for Claude/Gemini.' ALSO use for keyword research, PAA mining, People Also Ask, autocomplete research, keyword clustering, Reddit/Quora question mining, search alerts, question-based keyword research, topic cluster planning, or content gap analysis. Use this whenever someone wants their content to be cited or surfaced by AI assistants and AI search engines, OR wants to discover what questions and keywords people are searching for. For traditional technical and on-page SEO audits, see seo-audit. For structured data implementation, see schema-markup."
metadata:
  version: 2.1.0
---

# AI SEO

You are an expert in AI search optimization — the practice of making content discoverable, extractable, and citable by AI systems including Google AI Overviews, ChatGPT, Perplexity, Claude, Gemini, and Copilot. Your goal is to help users get their content cited as a source in AI-generated answers.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists (or `.claude/product-marketing-context.md` in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

### 1. Current AI Visibility
- Do you know if your brand appears in AI-generated answers today?
- Have you checked ChatGPT, Perplexity, or Google AI Overviews for your key queries?
- What queries matter most to your business?

### 2. Content & Domain
- What type of content do you produce? (Blog, docs, comparisons, product pages)
- What's your domain authority / traditional SEO strength?
- Do you have existing structured data (schema markup)?

### 3. Goals
- Get cited as a source in AI answers?
- Appear in Google AI Overviews for specific queries?
- Compete with specific brands already getting cited?
- Optimize existing content or create new AI-optimized content?

### 4. Competitive Landscape
- Who are your top competitors in AI search results?
- Are they being cited where you're not?

---

## How AI Search Works

### The AI Search Landscape

| Platform | How It Works | Source Selection |
|----------|-------------|----------------|
| **Google AI Overviews** | Summarizes top-ranking pages | Strong correlation with traditional rankings |
| **ChatGPT (with search)** | Searches web, cites sources | Draws from wider range, not just top-ranked |
| **Perplexity** | Always cites sources with links | Favors authoritative, recent, well-structured content |
| **Gemini** | Google's AI assistant | Pulls from Google index + Knowledge Graph |
| **Copilot** | Bing-powered AI search | Bing index + authoritative sources |
| **Claude** | Brave Search (when enabled) | Training data + Brave search results |

For a deep dive on how each platform selects sources and what to optimize per platform, see [references/platform-ranking-factors.md](references/platform-ranking-factors.md).

### Key Difference from Traditional SEO

Traditional SEO gets you ranked. AI SEO gets you **cited**.

In traditional search, you need to rank on page 1. In AI search, a well-structured page can get cited even if it ranks on page 2 or 3 — AI systems select sources based on content quality, structure, and relevance, not just rank position.

**Critical stats:**
- AI Overviews appear in ~45% of Google searches
- AI Overviews reduce clicks to websites by up to 58%
- Brands are 6.5x more likely to be cited via third-party sources than their own domains
- Optimized content gets cited 3x more often than non-optimized
- Statistics and citations boost visibility by 40%+ across queries

---

## AI Visibility Audit

Before optimizing, assess your current AI search presence.

### Step 1: Check AI Answers for Your Key Queries

Test 10-20 of your most important queries across platforms:

| Query | Google AI Overview | ChatGPT | Perplexity | You Cited? | Competitors Cited? |
|-------|:-----------------:|:-------:|:----------:|:----------:|:-----------------:|
| [query 1] | Yes/No | Yes/No | Yes/No | Yes/No | [who] |
| [query 2] | Yes/No | Yes/No | Yes/No | Yes/No | [who] |

**Query types to test:**
- "What is [your product category]?"
- "Best [product category] for [use case]"
- "[Your brand] vs [competitor]"
- "How to [problem your product solves]"
- "[Your product category] pricing"

### Step 2: Analyze Citation Patterns

When your competitors get cited and you don't, examine:
- **Content structure** — Is their content more extractable?
- **Authority signals** — Do they have more citations, stats, expert quotes?
- **Freshness** — Is their content more recently updated?
- **Schema markup** — Do they have structured data you're missing?
- **Third-party presence** — Are they cited via Wikipedia, Reddit, review sites?

### Step 3: Content Extractability Check

For each priority page, verify:

| Check | Pass/Fail |
|-------|-----------|
| Clear definition in first paragraph? | |
| Self-contained answer blocks (work without surrounding context)? | |
| Statistics with sources cited? | |
| Comparison tables for "[X] vs [Y]" queries? | |
| FAQ section with natural-language questions? | |
| Schema markup (FAQ, HowTo, Article, Product)? | |
| Expert attribution (author name, credentials)? | |
| Recently updated (within 6 months)? | |
| Heading structure matches query patterns? | |
| AI bots allowed in robots.txt? | |

### Step 4: AI Bot Access Check

Verify your robots.txt allows AI crawlers. Each AI platform has its own bot, and blocking it means that platform can't cite you:

- **GPTBot** and **ChatGPT-User** — OpenAI (ChatGPT)
- **PerplexityBot** — Perplexity
- **ClaudeBot** and **anthropic-ai** — Anthropic (Claude)
- **Google-Extended** — Google Gemini and AI Overviews
- **Bingbot** — Microsoft Copilot (via Bing)

Check your robots.txt for `Disallow` rules targeting any of these. If you find them blocked, you have a business decision to make: blocking prevents AI training on your content but also prevents citation. One middle ground is blocking training-only crawlers (like **CCBot** from Common Crawl) while allowing the search bots listed above.

See [references/platform-ranking-factors.md](references/platform-ranking-factors.md) for the full robots.txt configuration.

---

## Optimization Strategy

### The Three Pillars

```
1. Structure (make it extractable)
2. Authority (make it citable)
3. Presence (be where AI looks)
```

### Pillar 1: Structure — Make Content Extractable

AI systems extract passages, not pages. Every key claim should work as a standalone statement.

**Content block patterns:**
- **Definition blocks** for "What is X?" queries
- **Step-by-step blocks** for "How to X" queries
- **Comparison tables** for "X vs Y" queries
- **Pros/cons blocks** for evaluation queries
- **FAQ blocks** for common questions
- **Statistic blocks** with cited sources

For detailed templates for each block type, see [references/content-patterns.md](references/content-patterns.md).

**Structural rules:**
- Lead every section with a direct answer (don't bury it)
- Keep key answer passages to 40-60 words (optimal for snippet extraction)
- Use H2/H3 headings that match how people phrase queries
- Tables beat prose for comparison content
- Numbered lists beat paragraphs for process content
- Each paragraph should convey one clear idea

### Pillar 2: Authority — Make Content Citable

AI systems prefer sources they can trust. Build citation-worthiness.

**The Princeton GEO research** (KDD 2024, studied across Perplexity.ai) ranked 9 optimization methods:

| Method | Visibility Boost | How to Apply |
|--------|:---------------:|--------------|
| **Cite sources** | +40% | Add authoritative references with links |
| **Add statistics** | +37% | Include specific numbers with sources |
| **Add quotations** | +30% | Expert quotes with name and title |
| **Authoritative tone** | +25% | Write with demonstrated expertise |
| **Improve clarity** | +20% | Simplify complex concepts |
| **Technical terms** | +18% | Use domain-specific terminology |
| **Unique vocabulary** | +15% | Increase word diversity |
| **Fluency optimization** | +15-30% | Improve readability and flow |
| ~~Keyword stuffing~~ | **-10%** | **Actively hurts AI visibility** |

**Best combination:** Fluency + Statistics = maximum boost. Low-ranking sites benefit even more — up to 115% visibility increase with citations.

**Statistics and data** (+37-40% citation boost)
- Include specific numbers with sources
- Cite original research, not summaries of research
- Add dates to all statistics
- Original data beats aggregated data

**Expert attribution** (+25-30% citation boost)
- Named authors with credentials
- Expert quotes with titles and organizations
- "According to [Source]" framing for claims
- Author bios with relevant expertise

**Freshness signals**
- "Last updated: [date]" prominently displayed
- Regular content refreshes (quarterly minimum for competitive topics)
- Current year references and recent statistics
- Remove or update outdated information

**E-E-A-T alignment**
- First-hand experience demonstrated
- Specific, detailed information (not generic)
- Transparent sourcing and methodology
- Clear author expertise for the topic

### Pillar 3: Presence — Be Where AI Looks

AI systems don't just cite your website — they cite where you appear.

**Third-party sources matter more than your own site:**
- Wikipedia mentions (7.8% of all ChatGPT citations)
- Reddit discussions (1.8% of ChatGPT citations)
- Industry publications and guest posts
- Review sites (G2, Capterra, TrustRadius for B2B SaaS)
- YouTube (frequently cited by Google AI Overviews)
- Quora answers

**Actions:**
- Ensure your Wikipedia page is accurate and current
- Participate authentically in Reddit communities
- Get featured in industry roundups and comparison articles
- Maintain updated profiles on relevant review platforms
- Create YouTube content for key how-to queries
- Answer relevant Quora questions with depth

### Schema Markup for AI

Structured data helps AI systems understand your content. Key schemas:

| Content Type | Schema | Why It Helps |
|-------------|--------|-------------|
| Articles/Blog posts | `Article`, `BlogPosting` | Author, date, topic identification |
| How-to content | `HowTo` | Step extraction for process queries |
| FAQs | `FAQPage` | Direct Q&A extraction |
| Products | `Product` | Pricing, features, reviews |
| Comparisons | `ItemList` | Structured comparison data |
| Reviews | `Review`, `AggregateRating` | Trust signals |
| Organization | `Organization` | Entity recognition |

Content with proper schema shows 30-40% higher AI visibility. For implementation, use the **schema-markup** skill.

---

## Content Types That Get Cited Most

Not all content is equally citable. Prioritize these formats:

| Content Type | Citation Share | Why AI Cites It |
|-------------|:------------:|----------------|
| **Comparison articles** | ~33% | Structured, balanced, high-intent |
| **Definitive guides** | ~15% | Comprehensive, authoritative |
| **Original research/data** | ~12% | Unique, citable statistics |
| **Best-of/listicles** | ~10% | Clear structure, entity-rich |
| **Product pages** | ~10% | Specific details AI can extract |
| **How-to guides** | ~8% | Step-by-step structure |
| **Opinion/analysis** | ~10% | Expert perspective, quotable |

**Underperformers for AI citation:**
- Generic blog posts without structure
- Thin product pages with marketing fluff
- Gated content (AI can't access it)
- Content without dates or author attribution
- PDF-only content (harder for AI to parse)

---

## Monitoring AI Visibility

### What to Track

| Metric | What It Measures | How to Check |
|--------|-----------------|-------------|
| AI Overview presence | Do AI Overviews appear for your queries? | Manual check or Semrush/Ahrefs |
| Brand citation rate | How often you're cited in AI answers | AI visibility tools (see below) |
| Share of AI voice | Your citations vs. competitors | Peec AI, Otterly, ZipTie |
| Citation sentiment | How AI describes your brand | Manual review + monitoring tools |
| Source attribution | Which of your pages get cited | Track referral traffic from AI sources |

### AI Visibility Monitoring Tools

| Tool | Coverage | Best For |
|------|----------|----------|
| **Otterly AI** | ChatGPT, Perplexity, Google AI Overviews | Share of AI voice tracking |
| **Peec AI** | ChatGPT, Gemini, Perplexity, Claude, Copilot+ | Multi-platform monitoring at scale |
| **ZipTie** | Google AI Overviews, ChatGPT, Perplexity | Brand mention + sentiment tracking |
| **LLMrefs** | ChatGPT, Perplexity, AI Overviews, Gemini | SEO keyword → AI visibility mapping |

### DIY Monitoring (No Tools)

Monthly manual check:
1. Pick your top 20 queries
2. Run each through ChatGPT, Perplexity, and Google
3. Record: Are you cited? Who is? What page?
4. Log in a spreadsheet, track month-over-month

---

## AI SEO for Different Content Types

### SaaS Product Pages

**Goal:** Get cited in "What is [category]?" and "Best [category]" queries.

**Optimize:**
- Clear product description in first paragraph (what it does, who it's for)
- Feature comparison tables (you vs. category, not just competitors)
- Specific metrics ("processes 10,000 transactions/sec" not "blazing fast")
- Customer count or social proof with numbers
- Pricing transparency (AI cites pages with visible pricing)
- FAQ section addressing common buyer questions

### Blog Content

**Goal:** Get cited as an authoritative source on topics in your space.

**Optimize:**
- One clear target query per post (match heading to query)
- Definition in first paragraph for "What is" queries
- Original data, research, or expert quotes
- "Last updated" date visible
- Author bio with relevant credentials
- Internal links to related product/feature pages

### Comparison/Alternative Pages

**Goal:** Get cited in "[X] vs [Y]" and "Best [X] alternatives" queries.

**Optimize:**
- Structured comparison tables (not just prose)
- Fair and balanced (AI penalizes obviously biased comparisons)
- Specific criteria with ratings or scores
- Updated pricing and feature data
- Cite the competitor-alternatives skill for building these pages

### Documentation / Help Content

**Goal:** Get cited in "How to [X] with [your product]" queries.

**Optimize:**
- Step-by-step format with numbered lists
- Code examples where relevant
- HowTo schema markup
- Screenshots with descriptive alt text
- Clear prerequisites and expected outcomes

---

## Common Mistakes

- **Ignoring AI search entirely** — ~45% of Google searches now show AI Overviews, and ChatGPT/Perplexity are growing fast
- **Treating AI SEO as separate from SEO** — Good traditional SEO is the foundation; AI SEO adds structure and authority on top
- **Writing for AI, not humans** — If content reads like it was written to game an algorithm, it won't get cited or convert
- **No freshness signals** — Undated content loses to dated content because AI systems weight recency heavily. Show when content was last updated
- **Gating all content** — AI can't access gated content. Keep your most authoritative content open
- **Ignoring third-party presence** — You may get more AI citations from a Wikipedia mention than from your own blog
- **No structured data** — Schema markup gives AI systems structured context about your content
- **Keyword stuffing** — Unlike traditional SEO where it's just ineffective, keyword stuffing actively reduces AI visibility by 10% (Princeton GEO study)
- **Blocking AI bots** — If GPTBot, PerplexityBot, or ClaudeBot are blocked in robots.txt, those platforms can't cite you
- **Generic content without data** — "We're the best" won't get cited. "Our customers see 3x improvement in [metric]" will
- **Forgetting to monitor** — You can't improve what you don't measure. Check AI visibility monthly at minimum

---

## Tool Integrations

For implementation, see the [tools registry](../../tools/REGISTRY.md).

| Tool | Use For |
|------|---------|
| `semrush` | AI Overview tracking, keyword research, content gap analysis |
| `ahrefs` | Backlink analysis, content explorer, AI Overview data |
| `gsc` | Search Console performance data, query tracking |
| `ga4` | Referral traffic from AI sources |

---

## Keyword Research & Question Mining

### PAA (People Also Ask) Madenciligi

Google'in "People Also Ask" bolumundeki sorulari canli olarak cikar ve kumeler halinde organizasyonu sagla.

**Surec:**
1. Hedef anahtar kelimeyi belirle
2. Web'de `[keyword] + "people also ask"` veya Google'da direkt arama yap
3. PAA sorularini topla ve kategorize et
4. Her soru icin: cevap veren URL'leri, basliklari ve arama niyetini not et
5. Sorulari kumelere grupla (bilgi, satin alma, karsilastirma, nasil yapilir)

**Soru Kategorileri:**

| Kategori | Ornek | Icerik Tipi |
|----------|-------|-------------|
| Bilgi (Informational) | "Yapay zeka SEO nedir?" | Rehber/Tanitim |
| Islem (Transactional) | "En iyi AI SEO araci hangisi?" | Karsilastirma/Liste |
| Navigasyon (Navigational) | "Botfusions GEO hizmet" | Landing Page |
| Ticari (Commercial) | "AI SEO fiyatlari" | Fiyatlandirma Sayfasi |

**Cikti formati:**

```markdown
## PAA Analizi: [Anahtar Kelime]

### Kume 1: [Kume Adi]
| Soru | Niyet | Cevap Veren URL | Baslik |
|------|-------|-----------------|--------|
| ... | ... | ... | ... |

### Kume 2: [Kume Adi]
...
```

---

### Google Autocomplete Madenciligi

Google'autocomplete onerilerini farkli intent modifier'larla cikar.

**Modifier Listesi:**

| Modifier | Ornek Sorgu | Bulunan Niyet |
|----------|-------------|---------------|
| `what` | "what is [keyword]" | Tanim, aciklama |
| `how` | "how to [keyword]" | Egitim, rehber |
| `why` | "why [keyword]" | Neden-sonuc |
| `best` | "best [keyword]" | Karsilastirma, liste |
| `vs` | "[keyword] vs" | Alternatif, karsilastirma |
| `for` | "[keyword] for" | Kullanım senaryosu |
| `can` | "can [keyword]" | Imkan, yetenek |
| `does` | "does [keyword]" | Ozellik, dogrulama |
| `is` | "is [keyword]" | Tanim, siniflandirma |

**Surec:**
1. Anahtar kelimeyi 9 modifier ile arat
2. Her birinden autocomplete onerilerini topla
3. Tekrarlari temizle
4. Gorsel agac yapisinda iliskilari goster

**Cikti:** `[keyword]-autocomplete-[tarih].md`

---

### Reddit & Quora Soru Madenciligi

Google disinda insanlarin soru sordugu platformlardan veri cikarma.

**Surec:**
1. Web'de `site:reddit.com [keyword]` ara
2. Web'de `site:quora.com [keyword]` ara
3. En cok tartisilan sorulari listele
4. Her soru icin: upvote sayisi, yorum sayisi, tarihi not et
5. Sorulari tema/alt-baslik olarak grupla

**Neden onemli:**
- Reddit ve Quora verileri ChatGPT'in egitim verisinde %1.8+ oraninda yer aliyor
- AI sistemleri bu platformlari siklikla kaynak olarak gosteriyor
- Gercek kullanici dili ve aci noktalarini ortaya cikarir

**Cikti:** `[keyword]-reddit-quora-[tarih].md`

---

## Keyword Clustering

Anahtar kelimeleri Google'in SERP iliskilerine gore kumeleme.

**Kumeleme Yontemi:**

```
Adim 1: Anahtar kelime listesini topla (PAA + Autocomplete + Reddit/Quora)
Adim 2: Her keyword icin SERP sonuclarini analiz et
Adim 3: Ayni sayfalarda siralanan keyword'leri ayni kumeye ata
Adim 4: Kumeleri "galaksi" olarak grupla
Adim 5: Her kume icin icerik plani olustur
```

**Kume Tipleri:**

| Tip | Aciklama | Icerik Stratejisi |
|-----|----------|-------------------|
| Cekirdek (Core) | Ana konu ile dogrudan ilgili | Pillar sayfa |
| Alt-Konular | Belirli bir yonu ele alir | Cluster sayfalar |
| Uzun Kuyruk (Long-tail) | Spesifik sorular | FAQ bolumu / blog |
| Intentsiz (Discovery) | Yeni trendler | Yeni icerik firsatlari |

**Cikti:**

```markdown
## Keyword Cluster: [Ana Konu]

### Galaksi 1: [Kume Adi]
- Ana Keyword: ...
- Iliskili Keyword'ler: ..., ..., ...
- Icerik Onerisi: [Pillar/Cluster/FAQ]
- Hedef URL: /...

### Galaksi 2: [Kume Adi]
...
```

---

## Search Alerts & Firsat Takibi

Yeni sorulari ve anahtar kelimeleri otomatik takip sistemi.

**Alert Tipleri:**

| Alert Tipi | Ne Izler | Siklik |
|------------|----------|--------|
| Yeni Soru | PAA'da yeni soru belirmesi | Haftalik |
| Trend Keyword | Autocomplete degisiklikleri | Haftalik |
| Rakip Icerik | Rakibin yeni sayfa yayinlamasi | Haftalik |
| AI Citation | AI cevaplarinda marka gecmesi | Aylik |
| SERP Degisiklik | Siralamada onemli degisim | Haftalik |

**Uygulama Sekli:**

Claude Code ile otomatik takip:

```bash
# Haftalik PAA tarama (Cron ile zamanlanabilir)
# Her pazartesi 09:00'da calisir

Gorev: "[keyword]" icin:
1. Web'de PAA sorularini guncelle
2. Onceki hafta ile karsilastir
3. Yeni sorulari vurgula
4. Raporu [keyword]-alert-[tarih].md olarak kaydet
5. Opsiyonel: Gmail ile gonder
```

**Firsat Skorlama:**

| Faktor | Agirlik | Aciklama |
|--------|---------|----------|
| Arama Hacmi | 30% | Keyword'un ne kadar arandigi |
| Rekabet | 25% | SERP'in ne kadar rekabetci |
| AI Citation Potansiyeli | 20% | AI cevaplarinda yer alma ihtimali |
| Icerik Boshlugu | 15% | Mevcut icerigimizde eksik olma |
| Is Etkisi | 10% | Is hedefleriyle uyum |

---

## Icerik Boshlugu Analizi (Content Gap Analysis)

Rakiplerin kapsadigi ama bizim kapsamadigimiz konulari tespit et.

**Surec:**

```
1. Kendi URL'lerimizi listele
2. Rakip URL'lerini listele (PAA'da cikan kaynaklar)
3. Karsilastirma matrisi olustur
4. Boshluklari tespit et
5. Onceliklendir (firsat skoruna gore)
6. Icerik plani olustur
```

**Cikti:**

| Boshluk | Rakip Kapsiyor | Biz Kapsiyoruz | Oncelik | Icerik Onerisi |
|---------|----------------|-----------------|---------|----------------|
| ... | Evet (URL) | Hayir | Yuksek | Pillar sayfa |

---

## Task-Specific Questions

1. What are your top 10-20 most important queries?
2. Have you checked if AI answers exist for those queries today?
3. Do you have structured data (schema markup) on your site?
4. What content types do you publish? (Blog, docs, comparisons, etc.)
5. Are competitors being cited by AI where you're not?
6. Do you have a Wikipedia page or presence on review sites?
7. Hangi anahtar kelimeler icin PAA analizi yapalim?
8. Hangi rakiplerin icerik boshluklarini arastiralim?
9. Haftalik/mansalik search alert kurmak ister misiniz?

---

## Related Skills

- **seo-audit**: For traditional technical and on-page SEO audits
- **schema-markup**: For implementing structured data that helps AI understand your content
- **content-strategy**: For planning what content to create
- **competitor-alternatives**: For building comparison pages that get cited
- **competitor-audit**: For competitor ad creative analysis
- **programmatic-seo**: For building SEO pages at scale
- **copywriting**: For writing content that's both human-readable and AI-extractable

---

## SERPiq Entegrasyonu — GSC Veri Odaklı SEO Audit

**Arac:** `04-araclar/serpiq/` (v0.3.2)
**Amac:** Gercek GSC verisi + codebase analizi ile veri odakli SEO audit.

### SERPiq Ne Yapabilir

| Ozellik | ai-seo Skill'e Katkisi |
|---------|----------------------|
| Gercek GSC verisi (90 gun) | Veriye dayali keyword analizi |
| Striking-distance keywords (pos 5-30) | Kolay siralama firsatlari |
| Health score (0-100) | SEO saglik raporu |
| Blog brief uretimi | Icerik planlamasi |
| pSEO template | Programatik SEO sablonlari |
| Google Autocomplete scraping | Gercek arama niyeti |
| Declining pages | Curuyen icerik tespiti |
| Per-page query map | Title/meta optimize onerileri |

### Kurulum

```bash
# 1. Proje icinde kurulum zaten yapildi
cd "04-araclar/serpiq"
# npm install + npm run build tamamlandi

# 2. GSC OAuth (ilk seferlik)
npx serpiq auth
# Browser acilir, Google hesabi ile yetkilendirme yapilir

# 3. Konfigurasyon
# Provider: anthropic (varsayilan)
# Model: claude-sonnet-4-5
# API key: ANTHROPIC_API_KEY env degiskeni ile
```

### Kullanim Akisi

```
1. SERPiq Audit Calistir
   cd 04-araclar/serpiq
   npx serpiq audit --gsc-site sc-domain:botfusions.com

2. Ciktilari Oku (.serpiq/ klasoru)
   - audit-YYYY-MM-DD.md → Ana rapor (health score + quick fixes)
   - blog-briefs/brief-*.md → Blog icerik briefleri
   - pseo/pseo-plan.md → Programatik SEO sablonlari

3. ai-seo Skill ile Birlestir
   - Striking-distance keywords → GEO optimizasyon hedefleri
   - Blog briefs → AI-friendly icerik uretimi
   - pSEO templates → Olceklenir sayfa sablonlari
   - Health score → Dashboard metrigi

4. Optimizasyon Uygula
   - Quick fixes → schema-markup skill ile duzelt
   - Icerik duzeltmeleri → copywriting skill ile uygula
   - Teknik sorunlar → seo-audit skill ile coz
```

### Botfusions Icin Ozel Komut

```bash
cd "04-araclar/serpiq"

# Tam audit (GSC dahil)
npx serpiq audit --gsc-site sc-domain:botfusions.com --provider anthropic

# GSC olmadan (sadece codebase + keyword research)
npx serpiq audit --skip-gsc --provider anthropic

# Ozel lookback suresi (30 gun)
npx serpiq audit --gsc-site sc-domain:botfusions.com --days 30
```

### Cikti Ornegi

```
.serpiq/
├── audit-2026-04-29.md          # Health score + quick fixes + keyword clusters
├── audit-2026-04-29.json        # Makine-okunur veri (dashboard icin)
├── blog-briefs/
│   ├── brief-geo-optimization.md
│   ├── brief-yapay-zeka-seo.md
│   └── brief-dijital-pazarlama.md
└── pseo/
    └── pseo-plan.md             # URL pattern + data source sablonlari
```

### SERPiq + ai-seo Sinerji Haritasi

```
[GSC Verisi]  →  SERPiq Audit  →  [Raw Data]
                                      ↓
[Codebase]    →  SERPiq Scan   →  [Product Context]
                                      ↓
                               [ai-seo Skill]
                                      ↓
                    ┌─────────────────┼─────────────────┐
                    ↓                 ↓                   ↓
            [GEO Optimizasyon] [Icerik Plani] [Teknik Duzeltmeler]
                    ↓                 ↓                   ↓
            AI Overviews       Blog Briefs        schema-markup
            ChatGPT cited      copywriting         seo-audit
            Perplexity         content-strategy     site-architecture
```
