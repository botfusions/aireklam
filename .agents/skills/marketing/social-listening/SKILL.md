---
name: social-listening
version: 1.0.0
author: Botfusions AI Reklam Ajansi
description: Sosyal medya dinleme ve marka izleme. Marka bahsleri, rakip aktivite, trend tespiti, kriz uyarisii.
tags: [social-listening, sentiment, monitoring, crisis, trends]
---

# Social Listening Skill

## When to Activate

TRIGGER when user says:
- "Marka bahslerini izle", "sosyal dinleme", "ne soyluyorlar"
- "Sentiment analizi", "marka algisi", "nabiz olc"
- "Rakip sosyal aktivite", "rekabet takibi"
- "Trend tespit", "viral icerik", "kriz uyarisii"
- "Sosyal medya raporu", "mention tracking"

ALWAYS read `.agents/product-marketing-context.md` before execution.

## Pipeline Architecture

```
[1. KEYWORDS SETUP]
  Brand terms + competitor names + industry keywords
  → Turkish + English keyword matrix
       ↓
[2. MONITOR MENTIONS]
  Social platforms: Twitter/X, Instagram, LinkedIn, Reddit, TikTok
  News sites, forums, blogs
  → Real-time mention stream
       ↓
[3. SENTIMENT ANALYSIS]
  Positive / Neutral / Negative classification
  Turkish NLP considerations (slang, sarcasm)
  → Sentiment score + volume trend
       ↓
[4. TREND DETECTION]
  Emerging topics, viral content signals
  Hashtag velocity, engagement spikes
  → Opportunity + threat alerts
       ↓
[5. ALERT SYSTEM]
  Crisis threshold triggers
  Negative sentiment spike > 20% in 1 hour
  → Priority notification
       ↓
[6. RESPONSE]
  Template-based reply framework
  Escalation matrix for crisis scenarios
  → Actionable response cards
```

## Implementation Phases

### Phase 1: Keyword Matrix Construction

```
Input:  Brand name, product names, executive names, competitor list
Output: Structured keyword groups (exact match, broad, negation)

Categories:
  - Brand:       ["Botfusions", "botfusions.com", "#botfusions"]
  - Product:     ["GEO hizmet", "AI SEO", "yapay zeka pazarlama"]
  - Competitor:  ["competitor1", "competitor2", "alternatif SEO"]
  - Industry:    ["AI reklam", "dijital pazarlama AI", "GEO optimization"]
  - Negation:    [-"botfusions crack", -"fake botfusions"]
```

### Phase 2: Monitoring Setup

Monitor these Turkish + global platforms:
- **Twitter/X**: Real-time keyword stream, hashtag tracking
- **Instagram**: Brand tags, story mentions, comment sentiment
- **LinkedIn**: Company page mentions, employee advocacy signals
- **Reddit**: Subreddit mentions (r/Turkey, r/marketing, r/SEO)
- **TikTok**: Brand sound/hashtag usage, duet/stitch reactions
- **Forums**: DonanimHaber, Ekşi Sözlük, Technopat

### Phase 3: Sentiment Scoring

Turkish sentiment model considerations:
- Detect sarcasm: "Harika, yine calismiyor" → NEGATIVE
- Handle slang: "cok iyi", "süper", "berbat", "rezil"
- Code-switching: Turkish-English mixed sentences
- Scale: -100 (crisis) to +100 (love), 0 = neutral

### Phase 4: Trend & Crisis Detection

```
ALERT TIERS:
  GREEN  (Info):     Mention volume normal, positive trend
  YELLOW (Warning):  Negative sentiment +15% above baseline
  ORANGE (Urgent):   Negative sentiment +25%, potential crisis
  RED    (Crisis):   Negative spike >40%, media pickup detected

Crisis Signals:
  - Coordinated negative campaign
  - Influencer complaint
  - Media investigation
  - Legal/regulatory mention
```

### Phase 5: Response Templates

```
POSITIVE MENTION:
  "Tesekkurler [Name]! [specific detail] hakkinda yorumunuz icin
   minnettariz. Daha fazla bilgi icin [link]"

NEGATIVE MENTION (Standard):
  "Merhaba [Name], yasadiniz sorundan dolayi uzgunuz.
   [escalation channel] uzerinden size yardimci olalim."

CRISIS RESPONSE:
  1. Acknowledge within 30 minutes
  2. Do NOT be defensive
  3. State corrective action plan
  4. Provide direct contact channel
  5. Follow up within 24 hours
```

## Error Handling

| Error | Solution |
|-------|----------|
| API rate limit hit | Exponential backoff, cache last known state |
| False positive sentiment | Manual review queue for score < +-20 |
| Platform access revoked | Rotate credentials, log access change |
| Turkish NLP inaccuracy | Sarcasm whitelist + manual override |
| Duplicate mentions | Deduplicate by URL + timestamp window (5min) |

## Output Format

```markdown
# Sosyal Dinleme Raporu — [Tarih]

## Ozet
- Toplam mention: [X] (+[Y]% vs onceki hafta)
- Sentiment skoru: [+Z] (positive / neutral / negative dagilimi)
- Alert seviyesi: [GREEN/YELLOW/ORANGE/RED]

## Trend Konular
1. [Trend 1] — mention: [N], sentiment: [score]
2. [Trend 2] — mention: [N], sentiment: [score]

## Kriz Uyarilari (varsa)
- [Zaman] | [Platform] | [Ozet] | [Oncelik]

## Rakip Aktivite
- [Rakip 1]: [Son aktivite ve sentiment]
- [Rakip 2]: [Son aktivite ve sentiment]

## Aksiyon Maddeleri
1. [ ] [Aksiyon] — Sorumlu: [Kisi] — Deadline: [Tarih]
2. [ ] [Aksiyon] — Sorumlu: [Kisi] — Deadline: [Tarih]
```

## Best Practices

**DO:**
- Monitor 24/7 with automated alerts; human review during business hours
- Track sentiment baseline for each brand separately
- Include Ekşi Sözlük and Turkish forums in monitoring
- Set up competitor benchmark alerts weekly
- Archive all crisis communications for post-mortem

**DON'T:**
- Never auto-reply to negative mentions without human review
- Never ignore micro-influencer complaints (they can escalate fast)
- Don't rely solely on automated sentiment (Turkish NLP has gaps)
- Never engage trolls or coordinated attack threads
- Don't share internal sentiment data externally

## Metrics to Track

| Metric | Target | Frequency |
|--------|--------|-----------|
| Share of Voice | > 25% in category | Weekly |
| Sentiment Score | > +40 baseline | Daily |
| Response Time | < 30 min (crisis) | Real-time |
| Crisis Incidents | 0 per quarter | Monthly |
| Trend Capitalization | 2+ per month | Monthly |
