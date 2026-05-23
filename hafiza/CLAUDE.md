# Hafiza Wiki — CLAUDE.md

## Amac

Bu klasor **kalici bilgi arsivi**dir. LLM ile birlikte insa edilen, artimli, bakimli bir wiki sistemidir.
Ajanlar ve insanlar ortak bir bilgi yuzeyine sahip olur — bir sey ogrenildiginde buraya yazilir, bir sey soruldugunda once buraya bakilir.

## Dil

- TUM wiki sayfalari **Turkce** yazilir.
- Teknik terimler (API, MCP, OAuth, webhook vb.) Ingilizce kalabilir.
- Dosya adlari **kebab-case**: `google-ads-kurulum.md`, `omnisocials-api.md`

## Sayfa Formati

Her sayfa su yapiya uyar:

```markdown
---
title: "Sayfa Basligi"
tags: [etiket1, etiket2]
source: "raw/kaynak-adi.md veya URL"
date: 2026-05-17
status: aktif | arsiv | draft
---

# Sayfa Basligi

Icerik buraya...

## Sources

- [Kaynak 1](../raw/sources/kaynak-1.md)
- [Dis baglanti](https://...)

## Related

- [[ilgili-kavram]]
- [[ilgili-karar]]
```

### Frontmatter Alanlari

| Alan | Zorunlu | Aciklama |
|------|---------|----------|
| title | Evet | Sayfa basligi |
| tags | Evet | En az 1 etiket |
| source | Hayir | Ham kaynak dosyasi veya URL |
| date | Evet | Olusturulma tarihi (YYYY-MM-DD) |
| status | Evet | `aktif`, `arsiv`, `draft` |

## Klasor Yapisi

```
hafiza/
├── raw/              ← Ham kaynaklar (DOKUNULMAZ)
│   ├── sources/      ← Dis kaynaklar, dokumanlar
│   ├── docs/         ← Statik dokumanlar
│   └── assets/       ← Resimler, PDF'ler
├── sources/          ← Ham kaynaklarin ozet sayfalari
├── entities/         ← Dosyalar, fonksiyonlar, servisler, kisiler
├── concepts/         ← Soyut kavramlar
├── decisions/        ← Atomik kararlar (her karar = tek sayfa)
├── issues/           ← Duzeltilen sorunlar: kok neden + fix
├── syntheses/        ← Ust duzey genel bakis sayfalari
├── archive/          ← Eskimis sayfalar (asla silinmez)
├── index.md          ← Icerik katalogu
├── log.md            ← Append-only olay kaydi
└── CLAUDE.md         ← Bu dosya
```

## Uc Operasyon Workflow'u

### 1. INGEST (Bilgi Alma)

```
raw/ icindeki dosyalari oku
    ↓
sources/ altinda ozet sayfa yaz
    ↓
entities/, concepts/, decisions/ sayfalarini capraz-guncelle
    ↓
index.md ve log.md'yi guncelle
```

**Adimlar:**
1. `raw/sources/` veya `raw/docs/` icindeki yeni dosyalari tespit et
2. Her dosya icin `sources/` altinda bir ozet sayfasi olustur
3. Ozette gecen varliklari `entities/` altinda ara veya olustur
4. Ozette gecen kavramlari `concepts/` altinda ara veya olustur
5. Varsa kararlar `decisions/` altinda belgele
6. `index.md` katalogunu guncelle
7. `log.md`'ye zaman damgali kayit ekle

### 2. QUERY (Sorgulama)

```
Soru gelince
    ↓
index.md'den ilgili sayfalari bul
    ↓
Sayfalari oku, sentezle
    ↓
Her iddiaya kaynak referansı ver
    ↓
Iyi cevaplari syntheses/ veya concepts/ altinda geri dosyala
```

**Kurallar:**
- Once `index.md`'ye bak, sonra ilgili klasorlere in
- Her iddia icin `source` referansi ver
- "Bilmiyorum" demek tahmin uretmekten iyidir
- Sorgu sonucunda degerli bir sentez olustuysa `syntheses/` altina kaydet

### 3. LINT (Bakim)

```
Tum sayfalari tara
    ↓
Celiskileri, eskimis iddialari, yetim sayfalari tespit et
    ↓
Duzeltme onerisi olustur veya otomatik duzelt
    ↓
log.md'ye kaydet
```

**Kontrol Listesi:**
- [ ] Celisen iddialar var mi?
- [ ] Eskimis bilgiler var mi? (6+ ay once yazilmis, guncellenmemis)
- [ ] Yetim sayfalar var mi? (hicbir yerden referans verilmeyen)
- [ ] Eksik kavram sayfalari var mi? (birden fazla yerde gecen ama sayfasi olmayan)
- [ ] Tek yonlu cross-reference var mi? (A→B var ama B→A yok)
- [ ] Kaynak boslugu var mi? (source alani bos olan sayfalar)
- [ ] Frontmatter eksik mi?
- [ ] Tag tutarliligi saglandi mi?

## Sert Kurallar (Hard Rules)

| Kural | Aciklama |
|-------|----------|
| raw/ DOKUNULMAZ | raw/ klasoru altindaki dosyalar asla degistirilmez, silinmez |
| Kaynaksiz iddia yasak | Her iddia bir kaynakla desteklenmeli |
| Sayfa silme yok | Silmek yerine `archive/` altina tasima yap, status: arsiv yap |
| Celiski isaretleme | Celiskiler `## CELISKI` basligiyla isaretlenir, silinmez |
| Append-only log | log.md'ye sadece ekleme yapilir, mevcut kayitlar degistirilmez |
| kebab-case | Tum dosya adlari kebab-case formatinda olmalidir |
| Turkce icerik | Tum sayfalar Turkce (teknik terimler haric) |

## Obsidian Uyumlulugu

Bu wiki **Obsidian ile uyumlu** calisir:
- `[[wiki-link]]` formatı kullanilir
- Frontmatter YAML standardindadir
- Tag'lar `tags: [etiket1, etiket2]` formatindadir
- Gorseller `raw/assets/` altinda tutulur

## Mevcut Icerik

Mevcut dosyalar (wiki kurulumundan once):
- `rakip-arsivi/rakip-listesi.md` — Rakip analiz listesi
- `GOREV.md` — Gorev takip dosyasi

Bu dosyalar oldugu yerde kalir, INGEST sirasinda `sources/` altinda ozet sayfalari olusturulur.
