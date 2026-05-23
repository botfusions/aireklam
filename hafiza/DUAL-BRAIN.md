---
title: "Dual-Brain Hafıza Sistemi"
tags: [sistem, hafiza, obsidian, claude-memory]
date: 2026-05-17
status: aktif
---

# Dual-Brain Hafıza Sistemi

Her kayıt **iki beyne** yazılır. Hiçbir bilgi tek yerde tutulmaz.

---

## Beyin 1 — Obsidian Wiki (`hafiza/`)

**Ne için:** Yapısal, uzun vadeli, insan tarafından da okunabilen bilgi.

| Klasör | İçerik | Kim yazar |
|--------|--------|-----------|
| `rakip-arsivi/` | Günlük rakip snapshot'ları | Modül 01 agent |
| `trend-log/` | Haftalık trend özetleri | Modül 01 agent |
| `performans-tarihi/` | Google Ads + OmniSocials metrikleri | Modül 06 agent |
| `hook-kutuphanesi/` | Çalışan / çalışmayan hook'lar | Modül 02 + 06 agent |
| `icerik-arsivi/` | Yayınlanan içerik paketleri | Modül 03 agent |
| `entities/` | Rakipler, platformlar, araçlar | Tüm agentlar |
| `concepts/` | GEO, hook tipleri, stratejiler | Modül 02 agent |
| `decisions/` | Alınan stratejik kararlar | Modül 02 agent |
| `issues/` | Sorunlar ve çözümler | Tüm agentlar |
| `syntheses/` | Üst düzey sentezler | Modül 06 agent |

### Kayıt Kuralı
1. Her ajan çalışması → `log.md`'ye satır ekle (append-only)
2. Her yeni sayfa → `index.md` kataloğunu güncelle
3. Frontmatter zorunlu: `title`, `tags`, `date`, `status`
4. Dosya adı: `YYYY-MM-DD-konu.md` (tarihli) veya `konu.md` (kalıcı)

---

## Beyin 2 — Claude Auto-Memory (`spaces/.../memory/`)

**Ne için:** Claude'un oturumlar arası hatırladığı kritik öğrenmeler.

| Memory tipi | Ne zaman yazılır | Örnek |
|-------------|-----------------|-------|
| `reference` | Yeni araç/servis bağlandığında | WaveSpeed API parametreleri |
| `project` | Proje durumu değiştiğinde | Aktif kampanya sorunları |
| `feedback` | Bir yaklaşım işe yaradığında/yaramadığında | "output_format parametresi çalışmıyor" |
| `user` | Kullanıcı tercihi öğrenildiğinde | Obsidian vault yapısı tercihi |

### Kayıt Kuralı
1. Kritik öğrenme → hem `hafiza/` hem memory'ye yaz
2. Geçici durum → sadece `hafiza/` (memory'e yazma)
3. Tekrar eden hata → `feedback` memory olarak kaydet

---

## Senkronizasyon Akışı

```
Agent çalışır
    ↓
Beyin 1: hafiza/log.md → satır ekle
    ↓
Beyin 1: ilgili klasöre (rakip-arsivi/ trend-log/ vb.) MD dosyası yaz
    ↓
Beyin 1: hafiza/index.md → yeni sayfayı kataloğa ekle
    ↓
Kritik öğrenme varsa?
    ├── EVET → Beyin 2: memory/ dosyası yaz + MEMORY.md güncelle
    └── HAYIR → sadece Beyin 1 yeterli
```

---

## Medya-Geliştirme Klasörü ile İlişki

`medya-gelistirme/hafiza/` klasörü **artık kullanılmıyor.**
Tüm medya kayıtları doğrudan ana `hafiza/` klasörüne yazılır.

| Eski yol | Yeni yol |
|----------|----------|
| `medya-gelistirme/hafiza/rakip-arsivi/` | `hafiza/rakip-arsivi/` |
| `medya-gelistirme/hafiza/trend-log/` | `hafiza/trend-log/` |
| `medya-gelistirme/hafiza/performans-tarihi/` | `hafiza/performans-tarihi/` |
| `medya-gelistirme/hafiza/hook-kutuphanesi/` | `hafiza/hook-kutuphanesi/` |
