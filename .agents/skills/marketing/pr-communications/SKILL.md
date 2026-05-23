---
name: pr-communications
version: 1.0.0
author: Botfusions AI Reklam Ajansi
description: Halkla iliskiler ve kriz iletisimi. Basin bulteni, medya iliskileri, kriz plani, thought leadership.
tags: [PR, communications, crisis, press-release, media, thought-leadership]
---

# PR & Communications Skill

## When to Activate

TRIGGER when user says:
- "Basin bulteni", "press release", "medya bildirisi"
- "Medya iliskileri", "gazeteci listesi", "medya erisimi"
- "Kriz iletisimi", "kriz plani", "aciklama yap"
- "Thought leadership", "sektor liderligi", "uzman konumlanmasi"
- "Marka hikayesi", "brand storytelling", "PR stratejisi"
- "Reputasyon yonetimi", "kriz senaryosu"

ALWAYS read `.agents/product-marketing-context.md` before execution.

## Pipeline Architecture

```
[1. STORY IDENTIFICATION]
  Newsworthy angle detection
  Industry hook + data point + human element
  → Story pitch angle document
       ↓
[2. MEDIA TARGETING]
  Journalist database by beat (tech, marketing, AI, business)
  Outlet prioritization: tier 1 national > trade > regional
  → Curated media list (15-30 contacts)
       ↓
[3. CONTENT CREATION]
  Press release or media advisory
  Supporting assets: data, quotes, images
  → Approved press material
       ↓
[4. DISTRIBUTION]
  Direct pitch to tier-1 journalists
  Wire service for broad coverage
  Social amplification
  → Published coverage
       ↓
[5. FOLLOW-UP]
  Journalist relationship nurturing
  Interview scheduling, exclusive offers
  → Ongoing media relationships
       ↓
[6. MEASUREMENT]
  Coverage volume + sentiment + reach
  Share of voice vs competitors
  → PR performance report
```

## Implementation Phases

### Phase 1: Story Identification

```
NEWSWORTHINESS CHECKLIST:
  □ Novelty:     First, only, or biggest in category?
  □ Relevance:   Why now? What trend does it ride?
  □ Impact:      Who does it affect? How many?
  □ Data:        Statistics, research, or survey to anchor?
  □ Human:       Founder story, customer success, team angle?

STORY TYPES:
  - Product Launch:     "Botfusions GEO hizmeti ile AI'da gorunurluk devrimi"
  - Data/Research:      "Turkiye'de X sirketin Y%'i AI pazarlama kullaniyor"
  - Thought Leadership: "CEO: GEO, SEO'nun gelecegi olacak"
  - Milestone:          "Botfusions X musteri / Y ulke esigine ulasti"
  - Crisis Response:    "[Transparent statement about situation]"
```

### Phase 2: Media List Building

```
TURKEY TIER-1 OUTLETS:
  National:    Hurriyet, Milliyet, Sabah, Sozcu, NTV, CNN Turk
  Tech:        Webrazzi, DonanımHaber, Technopat, ShiftDelete
  Business:    Forbes Turkey, Fortune Turkey, Dunya, Capital
  Marketing:   Marketing Turkiye, Campaign Turkey, EJO

TIER SYSTEM:
  Tier 1: National + top trade (5-8 journalists)
  Tier 2: Industry-specific (8-12 journalists)
  Tier 3: Regional + blogs (10-15 contacts)

JOURNALIST PROFILING:
  - Beat: [tech / marketing / business / AI]
  - Recent articles: [last 3 topics]
  - Preferred contact: [email / Twitter DM / phone]
  - Relationship status: [new / warm / strong]
```

### Phase 3: Press Release Template

```markdown
# BASIN BULTENI — [Headline in 10 words max]

## [Subheadline: one sentence expanding the news]

[City], [Date] — [Lead paragraph: who, what, when, where, why in 40 words]

[Body paragraph 1: details and context]
[Body paragraph 2: data, statistics, or evidence]

"[Executive quote with strong opinion or vision]"
— [Name], [Title], Botfusions

[Body paragraph 3: what it means for the industry]

## Botfusions Hakkinda
[2-3 sentence company boilerplate. Always identical.]

## Medya Iletisim
[Name], [Title]
E-posta: [email]
Telefon: [phone]
Web: botfusions.com
```

### Phase 4: Crisis Communication Plan

```
CRISIS RESPONSE FRAMEWORK:

LEVEL 1 — MINOR (social media complaint, minor bug)
  Response time:  2 hours
  Spokesperson:   Social media manager
  Channel:        Social media reply
  Template:       Acknowledge → Fix → Follow up

LEVEL 2 — MODERATE (negative press, customer data issue)
  Response time:  1 hour
  Spokesperson:   Communications lead
  Channel:        Official statement + direct outreach
  Template:       Acknowledge → Investigate → Commit → Timeline

LEVEL 3 — SEVERE (data breach, legal action, major outage)
  Response time:  30 minutes
  Spokesperson:   CEO or Co-founder
  Channel:        Press conference + official statement
  Template:       Own it → Action plan → Timeline → Accountability

CRISIS DO's:
  - Be first with the truth (don't let others define the narrative)
  - Show empathy before facts
  - Provide specific next steps with deadlines
  - Update every 4 hours until resolved
  - Document everything for legal protection

CRISIS DON'Ts:
  - Never say "no comment"
  - Never blame customers or partners publicly
  - Don't over-apologize (legal liability)
  - Never speculate on causes before investigation
  - Don't go silent (silence = guilt in public perception)
```

### Phase 5: Thought Leadership Strategy

```
PLATFORMS FOR POSITIONING:
  LinkedIn:    Weekly long-form posts + articles (CEO/Founders)
  Twitter/X:   Daily commentary on AI/marketing trends
  Webrazzi:    Monthly op-ed or guest column
  Podcasts:    Turkish tech/marketing podcasts (bi-monthly)
  Conferences: Summit, Webrazzi Summit, Marketing Meetup (quarterly)

CONTENT PILLARS:
  1. GEO / AI Visibility  — Category creation, education
  2. Turkish AI Market    — Data-driven market commentary
  3. Agency Future        — How AI changes advertising
  4. Founder Journey      — Startup building in Turkey

EXECUTIVE POSITIONING:
  - Secure 2-3 speaking engagements per quarter
  - Publish 1 LinkedIn article per week
  - Comment on industry news within 24 hours
  - Build journalist Rolodex of 20+ active contacts
```

### Phase 6: PR Measurement

```
METRICS DASHBOARD:
  Coverage Volume:   Total articles per month (target: 8-12)
  Sentiment:         Positive / Neutral / Negative ratio (target: 80%+)
  Reach:             Estimated audience via media impressions
  Share of Voice:    Botfusions vs competitors in media (target: 20%+)
  Link Value:        Backlinks from media coverage (SEO benefit)
  Message Pull:      Key messages appearing in coverage (target: 60%+)

PR ROI ESTIMATION:
  Ad Value Equivalent (AVE) = Coverage column-cm x ad rate
  EMV for earned media = Impressions x CPM / 1000
  Cost per mention = Total PR spend / Coverage count
```

## Error Handling

| Error | Solution |
|-------|----------|
| Journalist ignores pitch | Follow up once after 48h, then try alternative contact |
| Negative coverage published | Crisis team activation, prepare response within 1h |
| Press release leaked early | Accelerate distribution, contact primary targets immediately |
| Quote misattributed | Request correction, provide written confirmation |
| Event cancellation | Pivot to virtual/digital format within 24h, notify all media |

## Best Practices

**DO:**
- Build journalist relationships before you need them (coffee meetings, events)
- Always have a holding statement ready for foreseeable crises
- Include data and statistics in every press release (journalists love numbers)
- Personalize every pitch (never send mass press releases as BCC)
- Maintain an updated media list quarterly (journalists change beats often)

**DON'T:**
- Never spam journalists with irrelevant pitches
- Never go off-record without explicit agreement
- Don't write press releases longer than 1 page
- Never promise exclusivity you cannot deliver
- Don't ignore trade press (they reach your actual buyers)

## Annual PR Calendar Template

| Quarter | Focus | Key Activities |
|---------|-------|---------------|
| Q1 | Category Education | GEO report launch, conference talks |
| Q2 | Customer Stories | Case study press releases, podcast tour |
| Q3 | Thought Leadership | Op-ed series, industry survey results |
| Q4 | Year in Review | Annual report, predictions for next year |
