---
name: customer-journey
description: When the user wants to map, analyze, or optimize the customer journey. Also use when the user mentions "customer journey," "musteri yolculugu," "buyer journey," "funnel mapping," "touchpoint analysis," "awareness to purchase," "channel mapping," "musteri deneyimi," or "how do customers find us."
metadata:
  version: 1.0.0
---

# Customer Journey Mapping

Design complete customer journeys connecting the right content, channels, and metrics at every stage from awareness to retention.

## When to Activate

- "Musteri yolculugu haritala" / "buyer journey"
- "Her asama icin icerik plani" / "touchpoint analizi"
- "Hangi kanalda ne yayinlamaliyiz" / "retention stratejisi"
- Customer lifecycle optimization needed

## Pipeline Architecture

```
[Persona] → [Touchpoint Map] → [Stage Assignment] → [Channel Assignment] → [Content Plan] → [Metric Framework]
```

## Journey Stages

### Awareness (Farkindalik)
Goal: Make prospects aware of the problem and your brand.
Channels: SEO/blog, social organic, YouTube, PR | Content: Educational posts, explainer videos
Metrics: Impressions, reach, organic traffic, brand search volume | Attribution: First-touch

### Consideration (Degerlendirme)
Goal: Position brand as the best solution among alternatives.
Channels: Retargeting ads, email nurture, comparison pages | Content: Case studies, demos, free tools
Metrics: Engagement, time on site, demo requests | Attribution: Linear, time-decay

### Decision (Karar)
Goal: Remove friction and convert prospects to customers.
Channels: Branded search ads, landing pages, sales calls | Content: Pricing page, testimonials, trial CTA
Metrics: CVR, CPA, ROAS, trial-to-paid | Attribution: Last-click, position-based

### Retention (Elde Tutma)
Goal: Maximize LTV through ongoing engagement.
Channels: Email, in-app, community, support | Content: Onboarding guides, newsletters, upsell
Metrics: Churn rate, NPS, expansion revenue | Attribution: Health score, cohort analysis

## Implementation

### Step 1: Persona Definition
Define: (1) Who is the ideal customer? (2) What problem are they solving? (3) Where do they spend time online? (4) How do they decide? (5) What are their objections?

### Step 2: Touchpoint Inventory
Map every customer interaction: Touchpoint | Stage | Channel | Current Asset | Gap?

### Step 3: Channel-Stage Matrix
| Channel | Awareness | Consideration | Decision | Retention |
|---------|-----------|---------------|----------|-----------|
| SEO/Blog | Primary | Primary | Secondary | - |
| Google Ads | Secondary | Primary | Primary | - |
| Meta Ads | Primary | Primary | Secondary | - |
| Email | - | Secondary | Primary | Primary |
| Social Organic | Primary | Secondary | - | Secondary |
| Landing Pages | - | Secondary | Primary | - |

### Step 4: Content Plan Per Stage
For each stage: content pieces (title, format, channel), priority (gap-based), production requirements, timeline.

### Step 5: Metric Framework
Awareness → Impressions, Reach, Brand Search | Consideration → Engagement, Demo Requests | Decision → CVR, CPA, ROAS | Retention → Churn, NPS, Expansion Revenue

## Gap Analysis

| Gap Type | Signal | Action |
|----------|--------|--------|
| Missing touchpoint | High drop-off between stages | Create transition content |
| Wrong channel | Low engagement | Reassign budget |
| Content mismatch | High bounce rate | Realign with stage intent |
| Measurement blindspot | No data for a stage | Set up `analytics-tracking` |

## Error Handling

| Issue | Solution |
|-------|----------|
| Non-linear paths | Use feedback loops, not strict funnel |
| Too many touchpoints | Prioritize top 80% impact |
| Attribution confusion | Start simple, evolve to multi-touch |
| Content gaps everywhere | Focus Decision stage first, work outward |

## Best Practices

**DO**: Start with customer research. Map actual journey (data-backed). Include emotional states. Plan for non-linear paths. Review quarterly.
**DON'T**: Map once and forget. Assume all personas follow same path. Ignore post-purchase. Over-index top-of-funnel. Skip attribution.

## Related Skills

- **content-strategy** — content pillars for journey stages
- **analytics-tracking** — measuring touchpoint effectiveness
- **attribution-modeling** — multi-touch attribution
- **copywriting** — stage-specific messaging
- **marketing-automation** — automating stage transitions
