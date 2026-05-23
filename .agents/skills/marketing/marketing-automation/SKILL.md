---
name: marketing-automation
description: When the user wants to automate repetitive marketing tasks. Also use when the user mentions "marketing automation," "otomasyon," "lead scoring," "email trigger," "workflow," "n8n," "Make," "Zapier," "otomatik rapor," "pipeline automation," or "isleri otomatik hale getir."
metadata:
  version: 1.0.0
---

# Marketing Automation

Identify repetitive marketing tasks and build reliable automated workflows that scale outreach, nurture leads, and deliver reports without manual intervention.

## When to Activate

- "Bu isleri otomatik hale getir" / "lead scoring kur"
- "n8n workflow lazim" / "email trigger tasarla"
- "Gunluk rapor otomatik gitsin" / "Zapier/Make workflow kur"

## Pipeline Architecture

```
[Identify Tasks] → [Design Workflow] → [Set Triggers] → [Configure Actions] → [Test & Validate] → [Monitor & Optimize]
```

## Automation Categories

### 1. Lead Scoring
Behavioral: visited_pricing (+10), requested_demo (+25), downloaded_ebook (+15), attended_webinar (+20), opened_3_emails (+10)
Demographic: company_size_match (+15), industry_match (+10), decision_maker_title (+20)
Negative: unsubscribed (-30), bounced_email (-10), no_activity_30d (-15)
Thresholds: HOT (60+ → sales outreach), WARM (30-59 → nurture), COLD (0-29 → awareness)

### 2. Email Trigger Workflows
| Trigger | Action | Delay |
|--------|--------|-------|
| Form submission | Welcome email | Immediate |
| Ebook download | Nurture sequence (3 emails) | Day 0, 3, 7 |
| Pricing page visit 3x | Sales alert | Immediate |
| Trial signup | Onboarding (5 emails) | Day 0, 1, 3, 7, 14 |
| No activity 30 days | Re-engagement email | Immediate |

### 3. Report Automation
Daily spend (09:00, Google Ads MCP → Slack/Gmail) | Weekly performance (Monday, GA4+Ads → Sheets+Email) | Monthly executive (1st, all channels → PDF+Email) | Anomaly alert (real-time → Slack+Email)

### 4. Social Scheduling
Blog published → auto-post LinkedIn/X (n8n) | Weekly digest → schedule top content | Mention detected → Slack alert

## Implementation

### Step 1: Task Audit
Ask: (1) Daily/weekly repetitive tasks? (2) Manual data copying between tools? (3) Manually generated reports? (4) Where do leads get stuck? (5) What follow-ups are missed?

### Step 2: Workflow Design
Document each: Trigger | Conditions/Filters | Actions per step | Error path | Success metric | Tool (n8n/Make/Zapier/Python)

### Step 3: Tool Selection
n8n: complex workflows, self-hosted, API-heavy (free self-hosted) | Make: visual builder, multi-step ($9/mo+) | Zapier: simple integrations, large library ($20/mo+) | Python: full control, data processing (dev time)

### Step 4: n8n Template
cron(0 9 * * *) → googleAds.queryReport → googleSheets.appendRow → gmail.send

### Step 5: Lead Scoring Setup
Define model → Connect data sources (CRM, email, ads, website) → Set scoring rules → Define hot/warm/cold thresholds → Create routing rules → Test with historical data

## Error Handling

| Error | Solution |
|-------|----------|
| API rate limit | Delay/retry with exponential backoff |
| Auth token expired | Auto-refresh; alert on failure |
| Data mismatch | Add validation step; alert on anomalies |
| Workflow stuck | Add timeout + fallback path |
| Duplicate sends | Add deduplication check |

Monitoring: Review execution logs weekly. Keep error rate <1%. Check lead score distribution monthly. Email deliverability >95%.

## Best Practices

**DO**: Start with one high-impact workflow. Document every workflow (trigger, steps, errors). Add error notifications. Test with small sample first. Review monthly. Refine lead scoring with data.
**DON'T**: Automate broken processes (fix first). Over-automate human-touch interactions. Set and forget. Create circular dependencies. Ignore compliance (KVKK/GDPR). Build without fallback paths.

## Related Skills

- **analytics-tracking** — tracking automation-triggered events
- **email-sequence** — designing email nurture content
- **marketing-dashboard** — automated reporting dashboards
- **customer-journey** — mapping automation to journey stages
- **lead-magnets** — creating assets that feed lead scoring
