---
name: seo-expert
description: "End-to-end SEO content creation pipeline: trend analysis, deep research, outline-first writing, inline quality gate with retry loop, and clean HTML output. Works in Claude Desktop, Claude Web, and Claude Code — no scripts or database required."
argument-hint: "topic | URL | keyword"
version: 1.0.0
license: MIT
---

# SEO Expert Skill

End-to-end SEO content creation pipeline: trend analysis, deep research, outline-first writing, inline quality gate with retry loop, and clean HTML output.

## When to Activate

TRIGGER when the user:
- Asks to write SEO content, blog posts, or articles
- Wants keyword research or content strategy
- Requests SEO optimization of existing content
- Mentions "SEO", "content writing", "blog post", "article"
- Wants landing page SEO audit
- Asks about search intent or keyword clustering
- Requests competitor content gap analysis

## The Three Pillars

### 1. Search Intent Segmentation
Her arama niyeti farklidir. Icerik uretirken 3 niyet katmanina gore strateji belirle:

| Niyet Turu | Ornek Aramalar | Kullanici Durumu | Icerik Stratejisi |
|-----------|---------------|-----------------|-------------------|
| **Bilgi arayan** | "katkisiz tarhana nasil anlasilir", "dogal urun nasil secilir" | Satin almaya hazir degil, zihni acik | Blog icerikleri → Egit → Guven insa et |
| **Urun arayan** | "organik tarhana", "glutensiz un" | Karar asamasina yakin | Dogrudan satis sayfasi → Net mesaj → Karar hizlandir |
| **Karsilastirma yapan** | "en iyi organik tarhana hangisi", "X marka mi Y marka mi" | Kritik esikte | Guven icerigi → Effaflık → Itiraz kir |

> **Uygulama Kurali:** Ayni anahtar kelime icin tek icerik uretme. Niyete gore ayri landing page veya icerik tipi belirle.

### 2. Product/Shopping Title Optimization
Google algoritmasi, aramayla **en iyi eslesen dili** odullendirir. Urun basliklarini potansiyel musteriin arama kutusuna yazacagi dogal dille kur.

**Yanlis:** "Organik sertifikali glutensiz karabugday unu 500gr"
**Dogru:** "glutensiz un" / "dogal tarhana" / "katkisiz bebek corbasi"

> **Kural:** H1, meta title ve product title yazarken once "Bu urunu almak isteyen kisi Google'a tam olarak ne yazar?" sorusunu sor.

### 3. Platform Intent Difference

| Platform | Temel Mantik | SEO Yaklasimi |
|----------|-------------|---------------|
| **Google** | Var olan talebi yakala | Niyet bazli anahtar kelime + landing page |
| **Meta/TikTok** | Talep olustur | Dikkat cekici creative + broad audience |

> **Prensip:** Google, Meta, TikTok sadece dagitim kanallaridir. Asil isi insani tanimaktir. **"Insani tanirisan ona satis yaparsin."**

---

## Pipeline Architecture

```
Topic / Keyword
     ↓
[1. TREND ANALYSIS]
  Web search → trending topics → validate demand
     ↓
[2. DEEP RESEARCH]
  SERP analysis → top 10 content → gap identification
  Keyword clustering → intent mapping
     ↓
[3. OUTLINE CREATION]
  Structure first → H2/H3 hierarchy → internal links
     ↓
[4. SECTION WRITING]
  Section-by-section → inline quality gate
  Retry loop if quality score < 8/10
     ↓
[5. SEO OPTIMIZATION]
  Meta title/description → schema markup → internal links
     ↓
[6. OUTPUT]
  Clean HTML → ready for WordPress/CMS
```

---

## Referans Vaka Analizleri & Kanıtlanmış Stratejiler

Bu bolum, gercek kampanyalardan cikarilmis SEO ve icerik stratejisi prensiplerini icerir.
Her prensip dogrudan icerik uretim pipeline'ina uygulanmalidir.

### Vaka: Dogal Gida Markasi — 5M Ciro / %3 CR (Google Ads + SEO)

**Kaynak:** Botfusions referans vaka analizi, Nisan 2026

#### 1. Niyet Yakalama Sistemi (Search Intent Segmentation)

Google'da her arama ayni degildir. Insan kelime degil, **niyet yazar**.
Icerik uretirken 3 niyet katmanina gore strateji belirle:

| Niyet Turu | Ornek Aramalar | Kullanici Durumu | Icerik Stratejisi |
|-----------|---------------|-----------------|-------------------|
| **Bilgi arayan** | "katkisiz tarhana nasil anlasilir", "dogal urun nasil secilir" | Satin almaya hazir degil, zihni acik | Blog icerikleri → Egit → Guven insa et |
| **Urun arayan** | "organik tarhana", "glutensiz un" | Karar asamasina yakin | Dogrudan satis sayfasi → Net mesaj → Karar hizlandir |
| **Karsilastirma yapan** | "en iyi organik tarhana hangisi", "X marka mi Y marka mi" | Kritik esikte | Guven icerigi → Effaflık → Itiraz kir |

> **Uygulama Kurali:** Ayni anahtar kelime icin tek icerik uretme. Niyete gore ayri landing page veya icerik tipi belirle.

#### 2. Urun/Shopping Basligi Optimizasyonu — Insan Gibi Yaz

**Yanlis yaklaşim (SEO gibi yazilan baslik):**
> "Organik sertifikali glutensiz karabugday unu 500gr"

**Dogru yaklaşim (Insan gibi aranan baslik):**
> "glutensiz un" / "dogal tarhana" / "katkisiz bebek corbasi"

**Prensip:** Google algoritmasi, aramayla **en iyi eslesen dili** odullendirir. Urun basliklarini potansiyel musteriin arama kutusuna yazacagi dogal dille kur.

> **Uygulama Kurali:** H1, meta title ve product title yazarken once "Bu urunu almak isteyen kisi Google'a tam olarak ne yazar?" sorusunu sor.

#### 3. Rakip Analizi — Herkes Ayni Seyi Soyliyorsa Sukut Altindar

SERP'te herkes sunu soyliyorsa:
- "%100 dogal"
- "Organik sertifikali"
- "Katkisiz"

...hicbiri anlam ifade etmiyor. Rekabetten sirilsmak icin **hikaye anlat, ozellik degil**.

**Sorulmasi gereken sorular (urun sayfasi icin):**
- Bu urunu kim yapiyor?
- Hangi koyde yapiliyor?
- Nasil kurutuluyor?
- Kac gunde hazirlaniyor?

> **Prensip:** Insan urunu satin almaz, arkasindaki insani satin alir. Endustriyel ile el yapimi arasindaki fark sadece icerik degil, **algidir**.

#### 4. Goster, Soyleme (Show Don't Tell)

Iddia yazmak degil, sureci gostermek donusumu artirir.

| Yapma | Yap |
|-------|-----|
| "Dogaldir" demek | Nasil dogal oldugunu goster |
| "Organiktir" demek | Uretim surecini anlat |
| "Kalitelidir" demek | Emeği ve zanaati goster |

> **Uygulama Kurali:** Icerikte her iddia icin somut bir kanit veya surec aciklamasi ekle. "Dogal" kelimesi tek basina SEO degeri tasimaz, baglam tasir.

#### 5. Platform Niyet Farki (Google vs Sosyal Medya)

| Platform | Temel Mantik | SEO Yaklasimi |
|----------|-------------|---------------|
| **Google** | Var olan talebi yakala | Niyet bazli anahtar kelime + landing page |
| **Meta/TikTok** | Talep olustur | Dikkat cekici creative + broad audience |

> **Prensip:** Google, Meta, TikTok sadece dagitim kanallaridir. Asil isi insani tanimaktir. **"Insani tanirisan ona satis yaparsin."**

#### Ozet — Bu Vakadan Cikan SEO Kurallari

1. Niyet segmentasyonu yapilmadan icerik yazma
2. Urun basliklarini insanin arama dilinde yaz
3. Competitor gap analizi: Herkes ne soyluyor, sen ne farkli soyleyeceksin?
4. Iddia degil surec goster — trust signal'lari surece gom
5. Platform stratejisini niyete gore belirle

---

## Implementation Phases

### Phase 1: Research & Planning
1. Keyword research → search volume, difficulty, intent
2. SERP analysis → top 10 content structure
3. Competitor gap → what's missing
4. Topic clustering → pillar + supporting content

### Phase 2: Content Structure
1. Create outline with H2/H3 hierarchy
2. Map keywords to sections
3. Plan internal links
4. Define CTAs per section

### Phase 3: Writing
1. Section-by-section writing
2. Inline quality check per section
3. Retry loop if quality < 8/10
4. Apply case study principles above

### Phase 4: Optimization
1. Meta title + description
2. Schema markup (FAQ, HowTo, Article)
3. Internal link integration
4. Image alt tags
5. URL structure

### Phase 5: Output
1. Clean HTML output
2. WordPress-ready format
3. Performance tracking setup

---

## Error Handling

- If keyword has no search volume → suggest alternative long-tail keywords
- If SERP is dominated by authority sites → pivot to long-tail niche
- If content quality gate fails → identify specific issues and retry section
- If API rate limits hit → use cached data and note limitations
- If schema validation fails → provide manual fallback markup

---

## Best Practices

### DO
- Always start with search intent
- Write for humans, optimize for engines
- Use the vaka analizi principles for every piece of content
- Show don't tell — evidence over claims
- Segment content by intent type
- Use natural language in titles (how people actually search)

### DON'T
- Don't keyword stuff titles
- Don't write one-size-fits-all content
- Don't ignore platform-specific intent
- Don't make claims without evidence/process proof
- Don't use the same strategy for Google and social media
