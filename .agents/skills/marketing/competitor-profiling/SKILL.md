---
name: competitor-profiling
description: Build a deep competitive intelligence profile for one or more competitors. Use when the user needs a comprehensive picture of a specific competitor — their positioning, messaging, pricing, ads, SEO, strengths, and weaknesses. Triggers on "deep dive on competitor," "competitive profile," "analyze [brand]," "spy on competitor," "competitive research," "what is [brand] doing," "competitor breakdown." Distinct from competitor-audit (which scans ad creatives) and competitor-alternatives (which builds comparison landing pages). This skill focuses on full-spectrum intelligence.
metadata:
  version: 1.0.0
---

# Competitor Profiling

You are an expert competitive intelligence analyst. Your goal is to build a comprehensive profile of a competitor that reveals their strategy, strengths, weaknesses, and gaps your brand can exploit.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists, read it. Know your own brand's positioning before analyzing a competitor.

Understand what the user needs:

1. **Who is the competitor?** — Company name, URL, market position
2. **What's the purpose?** — Positioning refresh, ad strategy, pricing, product roadmap, sales battlecard
3. **Depth required?** — Quick overview (30 min) vs full intelligence report (2–4 hours of research)
4. **Any specific focus?** — Messaging, SEO, paid ads, pricing, product, ICP

---

## Research Framework: 7 Intelligence Layers

### Layer 1: Positioning & Messaging

**Sources:** Homepage, About page, tagline, hero section, email sequences

Capture:
- Primary value proposition (headline + subheadline)
- ICP signals (who they say they're for)
- Key differentiators they emphasize
- Tone of voice (formal/casual, fear/aspiration, feature/outcome)
- What pain points they lead with
- What they avoid saying (gaps = opportunities)

**Ask:** What story are they telling? Who is the hero of that story?

---

### Layer 2: Pricing & Packaging

**Sources:** Pricing page, Capterra/G2 reviews, sales decks (if leaked), Product Hunt

Capture:
- Pricing model (per seat, usage, flat, freemium)
- Tier names and limits
- What's in free vs paid
- Annual discount amount
- Enterprise: hidden pricing or "contact sales"
- Price anchoring tactics

**Ask:** Where is the value metric? What do they hide from prospects?

---

### Layer 3: SEO & Content Strategy

**Sources:** Semrush/Ahrefs data (if available), sitemap, blog index, resource pages

Capture:
- Estimated organic traffic (ballpark)
- Top ranking pages and keywords
- Content categories (blog, docs, case studies, comparison pages, glossary)
- Content publishing cadence
- Topic clusters they dominate
- Gaps in their content coverage

**Ask:** What keywords are they ranking for that we're not targeting?

---

### Layer 4: Paid Advertising

**Sources:** Meta Ad Library, Google Transparency Center, LinkedIn Ad Library, SpyFu

Capture:
- Active ad count and formats
- Primary hooks and angles
- Audiences targeted (signals from creative)
- Offers being promoted (free trial, demo, discount)
- Landing page strategy (dedicated LP vs homepage)
- How long have they been running specific ads (longevity = winning)

**Ask:** What messages are they spending money to amplify?

---

### Layer 5: Product & Features

**Sources:** Product changelog, G2/Capterra reviews, YouTube demos, help docs, job postings

Capture:
- Core feature set
- Recently launched features (signals roadmap priority)
- Known limitations (1-star reviews are gold)
- Integrations offered
- Job postings (hiring ML = building AI features)

**Ask:** What are users complaining about in reviews? What are they hiring for?

---

### Layer 6: ICP & Customer Base

**Sources:** Case studies, testimonials, customer logos, G2 reviews, LinkedIn (who follows them)

Capture:
- Company size they target (SMB / mid-market / enterprise)
- Industries with most case studies
- Personas featured in testimonials
- Geographic focus
- Verticals they're pushing into (expansion signals)

**Ask:** Who are their happiest customers? Who is underserved?

---

### Layer 7: Go-to-Market & Distribution

**Sources:** Social profiles, podcast appearances, partnerships, affiliate/partner page, conferences

Capture:
- Primary acquisition channels (paid, SEO, PLG, sales, community)
- Social media activity and engagement
- Partnerships and integrations as distribution
- Community presence (Slack, Discord, subreddit)
- Events and sponsorships
- PR and media mentions

**Ask:** How are they growing? Where do their leads come from?

---

## Competitive Intelligence Matrix

| Dimension | Their Strength | Their Weakness | Our Opportunity |
|-----------|---------------|----------------|-----------------|
| Messaging | | | |
| Pricing | | | |
| SEO | | | |
| Paid Ads | | | |
| Product | | | |
| ICP | | | |
| Distribution | | | |

---

## SWOT for Competitor

**Strengths** — What they genuinely do well
**Weaknesses** — Gaps, complaints, blind spots
**Opportunities** — What they're not doing that the market wants
**Threats** — Where they're moving that could hurt you

---

## Battlecard Format (for Sales)

If the output is for a sales team:

```
COMPETITOR: [Name]
ONE-LINE SUMMARY: [What they are + who they're for]

WHY WE WIN:
• [Specific advantage 1]
• [Specific advantage 2]
• [Specific advantage 3]

WHY THEY WIN:
• [Honest strength 1]
• [Honest strength 2]

COMMON OBJECTIONS + RESPONSES:
"They have X feature" → "We do Y which solves the same problem better because..."
"They're cheaper" → "Our pricing includes Z which they charge extra for..."

TRAP QUESTIONS TO ASK PROSPECTS:
• "How important is [our strength area] to you?"
• "Have you ever had issues with [their known weakness]?"
```

---

## Output Format

Deliver a competitive profile with:
1. **Executive summary** — 3 sentences: who they are, who they target, what they're good at
2. **Positioning analysis** — Their story, ICP, differentiators
3. **Pricing breakdown** — Model, tiers, strategy
4. **Content + SEO snapshot** — Traffic estimate, top topics, content gaps
5. **Ad intelligence** — Active messages, formats, offers
6. **Product strengths and gaps** — Based on reviews and changelog
7. **ICP profile** — Who their best customers are
8. **GTM channels** — How they acquire
9. **Opportunity map** — Where we can win, where we should avoid
10. **Battlecard** (if requested)

---

## Türkçe Not (Botfusions Bağlamı)

Türk pazarında rakip analizi için: Webrazzi, Ekşi Sözlük incelemeleri, LinkedIn Türkiye profilleri, Google Ads Şeffaflık Merkezi Türkiye filtrelemesi. Yerel rakipler için fiyatlandırma benchmarkı kritik — Türk müşteriler fiyat karşılaştırması sıkça yapar.
