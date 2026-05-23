---
name: influencer-marketing
version: 1.0.0
author: Botfusions AI Reklam Ajansi
description: Influencer ve KOL stratejisi. Dogru influencer secimi, kampanya yonetimi, ROI olcum, kontrat ve uyum.
tags: [influencer, KOL, campaign, ROI, partnership]
---

# Influencer Marketing Skill

## When to Activate

TRIGGER when user says:
- "Influencer bul", "KOL stratejisi", "influencer kampanya"
- "Influencer secimi", "hangi influencer", "micro influencer"
- "Influencer ROI", "kampanya performans", "etki olcum"
- "Influencer kontrat", "uyum kurallari", "ISKUR", "Reklam Kurulu"
- "Influencer outreach", "isbirliği teklifi"

ALWAYS read `.agents/product-marketing-context.md` before execution.

## Pipeline Architecture

```
[1. GOAL SETTING]
  Campaign objective: awareness / consideration / conversion
  Budget allocation + KPI targets
       ↓
[2. INFLUENCER RESEARCH]
  Platform-specific search (Instagram, TikTok, YouTube, LinkedIn)
  Audience match score + authenticity vetting
  → Shortlist of 20-30 candidates
       ↓
[3. OUTREACH]
  Personalized pitch templates
  Rate negotiation framework
  → Signed LOI or contract
       ↓
[4. CREATIVE BRIEF]
  Content guidelines + do's/don'ts
  Brand voice alignment
  → Approved brief document
       ↓
[5. CAMPAIGN EXECUTION]
  Content creation + review cycle
  Posting schedule + amplification
  → Live content + engagement monitoring
       ↓
[6. ROI MEASUREMENT]
  Attribution: UTM + promo codes + pixel tracking
  EMV (Earned Media Value) calculation
  → Performance report + learnings
```

## Implementation Phases

### Phase 1: Campaign Goal Definition

```
OBJECTIVE MATRIX:
  AWARENESS:
    KPIs: Reach, Impressions, Share of Voice
    Budget split: 70% macro, 30% micro

  CONSIDERATION:
    KPIs: Engagement Rate, Video Views, Saves
    Budget split: 50% macro, 40% micro, 10% nano

  CONVERSION:
    KPIs: Clicks, Signups, Sales (promo code)
    Budget split: 30% macro, 50% micro, 20% nano
```

### Phase 2: Influencer Identification

**Tier Classification:**
| Tier | Followers | Avg Rate (TRY) | Use Case |
|------|-----------|---------------|----------|
| Nano | 1K-10K | 500-2,000 | Niche trust, high engagement |
| Micro | 10K-50K | 2,000-10,000 | Best ROI, authentic voice |
| Mid | 50K-250K | 10,000-50,000 | Balanced reach + trust |
| Macro | 250K-1M | 50,000-200,000 | Mass awareness |
| Mega | 1M+ | 200,000+ | Splash launches only |

**Vetting Checklist:**
- [ ] Audience demographics match (age 25-45, B2B decision makers)
- [ ] Engagement rate > 3% (Instagram), > 5% (TikTok)
- [ ] No fake followers (audit via Modash/HypeAuditor)
- [ ] Brand-safe content history
- [ ] Turkish market relevance
- [ ] Previous competitor partnerships (cool-down check)

### Phase 3: Outreach Templates

```
DM PITCH (Instagram/TikTok):
  "Merhaba [Name], [specific content] iceriginizi cok begendik.
   Botfusions olarak [campaign concept] kampanyamizda sizinle
   isbirligi yapmak isteriz. Detaylari konusmak icin
   uygun musunuz?"

EMAIL PITCH (LinkedIn/YouTube):
  Subject: "[Brand] x [Name] Isbirligi Teklifi"
  Body:
  - Personal compliment (specific to their content)
  - Brand intro (1 sentence)
  - Campaign concept overview
  - Why them (audience fit rationale)
  - Budget range indication
  - CTA: 15-min call or direct reply
```

### Phase 4: Pricing & Contract

```
PRICING MODELS:
  Flat Fee:        Fixed payment per deliverable
  Performance:     Base + CPM/CPA bonus
  Affiliate:       Commission per sale (15-30%)
  Product Gifting: Free product + minimal fee (nano tier)

CONTRACT ESSENTIALS:
  - Deliverables: format, count, timeline
  - Usage rights: duration, platforms, exclusivity
  - Approval process: 48h review before posting
  - Compliance: "Reklam" / "Sponsorlu" disclosure required
  - Kill fee: 50% if cancelled after approval
  - Exclusivity: category lock for 30-90 days
```

### Phase 5: Campaign Brief Structure

```markdown
# [Campaign Name] — Influencer Brief

## Marka Hakkinda
[2-3 sentences about Botfusions]

## Kampanya Amaci
[Objective + what success looks like]

## Hedef Kitle
Demographics, interests, pain points

## Icerik Kurallari
- DO: [tone, style, key messages]
- DON'T: [competitors, claims, tone]
- Mandatory: [CTA, hashtag, link placement]

## Zaman Cizelgesi
- Brief approval: [date]
- Draft submission: [date]
- Go live: [date]
- Report: [date]
```

### Phase 6: ROI Measurement

```
TRACKING STACK:
  UTM Parameters: ?utm_source=influencer&utm_medium=social&utm_campaign=[name]&utm_content=[influencer]
  Promo Codes: [INFLUENCER10] — unique per creator
  Pixel Tracking: Meta CAPI + Google Ads conversion
  EMV Formula: Impressions x CPM / 1000

ROI = (Revenue attributed - Influencer cost) / Influencer cost x 100
```

## Error Handling

| Error | Solution |
|-------|----------|
| Influencer flakes | Backup list of 3 per tier, contract penalty clause |
| Content off-brand | 48h review buffer, clear brief guidelines |
| Fake engagement | Pre-campaign audit, performance-based pricing |
| Low ROI | Mid-campaign optimization, shift budget to top performers |
| Compliance breach | Immediate takedown request, contractual remedy |

## Best Practices

**DO:**
- Prioritize micro-influencers for B2B AI/tech niche in Turkey
- Always use written contracts with usage rights clause
- Require "Reklam" / "Sponsorlu" disclosure per Turkish ad law
- Track unique promo codes per influencer for clean attribution
- Build long-term ambassador relationships over one-off deals

**DON'T:**
- Never select influencers based on follower count alone
- Never allow unreviewed content to go live
- Don't ignore nano influencers in B2B niche communities
- Never pay 100% upfront (use milestone payments)
- Don't run influencer campaigns without tracking infrastructure

## Compliance Notes (Turkey)

- **Reklam Kurulu**: Sponsored content MUST be labeled "Reklam" or "Sponsorlu"
- **Tuketici Kanunu**: No misleading claims about product capabilities
- **KVKK**: Influencer must not share user data without consent
- **ISKUR**: Employee influencers require disclosure of employment relationship
- **ETIK**: Industry-specific advertising ethics board rules apply
