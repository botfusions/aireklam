# Medya Geliştirme — Botfusions AI Pazarlama Sistemi

> Önce kendimize kuruyoruz, sonra müşteriye satıyoruz.

---

## Klasör Yapısı

| Klasör | Modül | İş |
|--------|-------|-----|
| `01-veri-toplama/` | Veri Toplama | Rakip analiz, trend scrape, Google Ads verisi, niche research |
| `02-strateji/` | Strateji Katmanı | Hook açısı, CTA varyasyonları, kanal adaptasyon kararı |
| `03-icerik-motoru/` | İçerik Motoru | Viral script, carousel, short-form, 6 kanal adaptasyon |
| `04-gorsel-uretim/` | Görsel Üretim | PNG statik, MP4 video/reel, platform boyut adaptasyonu |
| `05-yayin/` | Yayın | OmniSocials API, scheduling, onay kapısı |
| `06-analytics-loop/` | Analytics Loop | Performans raporu, anomali alarmı, içerik motoruna feedback |
| `hafiza/` | Hafıza Katmanı | İçerik arşivi, hook kütüphanesi, rakip arşivi, performans tarihi |

---

## İnşa Fazları

### Faz 1 — İçerik Fabrikası
**Modüller:** 01 + 02 + 03  
**Hedef:** Her sabah 6 kanal için taslak içerik hazır. İnsan sadece onaylıyor.  
**Süre:** 2-3 hafta

### Faz 2 — Görsel + Yayın
**Modüller:** 04 + 05  
**Hedef:** Onay sonrası görsel otomatik üretilir, yayın tetiklenir.  
**Süre:** 1-2 hafta

### Faz 3 — Feedback Loop
**Modüller:** 06  
**Hedef:** Hangi hook işe yaradı → bir sonraki içeriğe otomatik besleniyor.  
**Süre:** 1 hafta

---

## Onay Kapısı Kuralı

```
İçerik yazılır → Görsel üretilir → SEN ONAYLA → Yayın tetiklenir
```

> Görsel onay olmadan hiçbir şey yayınlanmaz.

---

## Araçlar

| Araç | Kullanım |
|------|----------|
| OmniSocials API | 6 kanal yayın (API Key: `secrets.env`) |
| Google Ads MCP | Performans verisi (`customer_id: 3646875139`) |
| canvas-design skill | Statik görsel üretim |
| HyperFrames | Video / Reel üretim |
| turkce-insani-yazar skill | İçerik yazımı |
| Google Sheets | Hafıza / arşiv (`1XrE0F5PWNXuvtvFv8OdK9-3zr-wUhNnkP4KuKviX3os`) |

---

*Botfusions AI Reklam Ajansı · botfusions.com · Mayıs 2026*
