# Botfusions AI Reklam Ajansı — Dashboard

> **İlk açılışta bu dosyayı oku, sonra göreve başla.**
> Detaylar için: `.agents/MANIFEST.md` · `.agents/API-INTEGRATIONS.md` · `.agents/product-marketing-context.md`
> **Medya/içerik işi için:** `medya-gelistirme/SISTEM-KONTEKST.md` — niş, hedef kitle, rakip, hook formülleri burada. Önce oku, sonra sor.
> **Beyin/Hafıza:** `hafiza/` — Ajan geçmişi, öğrenilen dersler, karar kayıtları. Bir şey sorulduğunda önce buraya bak. İşleyiş: `hafiza/CLAUDE.md`

---

## Sistem Durumu

| Bileşen | Durum | Detay |
|---------|-------|-------|
| Google Ads MCP | ✅ Aktif | Customer ID: `3646875139` |
| OmniSocials API | ✅ Aktif | 6 kanal bağlı |
| Google Sheets | ✅ Aktif | Sheet ID: `1XrE0F5PWNXuvtvFv8OdK9-3zr-wUhNnkP4KuKviX3os` |
| GA4 / GSC Pipeline | ⏳ Bekliyor | API key gerekli |
| Dönüşüm Takibi | ❌ Eksik | `analytics-tracking` skill ile kur |

---

## Sosyal Medya Hesapları (OmniSocials)

| Platform | Account ID | Kullanıcı |
|----------|-----------|-----------|
| Instagram | `881407_instagram` | @botfusions — post/story/reel |
| Facebook | `881407_facebook` | Ömer Tokgöz — post/story/reel |
| YouTube | `881407_youtube` | @botfusionss — yalnızca reel |
| TikTok | `881407_tiktok` | @botfusions — post/reel |
| Pinterest | `881407_pinterest` | cenk0342 — post |
| X | `881407_x` | @botfusionss — post **(X Premium, 25K limit)** |

**Pinterest Boards:** `AI-Botfusions-GEO` → `1091067515915706441` · `Profil` → `1091067515915706431`
**API Key:** `secrets.env` dosyasindan okunur (`OMNISOCIALS_API_KEY`)

---

## Aktif Kampanya: GEO Hizmet

- **Landing:** `botfusions.com/geo-hizmet`
- **Sorun:** Bütçenin %99,4'ü tek keyword'de — dağıtım gerekli
- **Görseller:** `02-gorseller/geo-gorseller/` (3 format hazır)
- **Kopyalar:** `01-reklam-kopyalari/geo-reklam-kopyalari.md`

---

## Model Seçimi

| Görev | Model |
|-------|-------|
| Strateji / kopya / yaratıcı iş | `claude-opus-4-6` |
| Agentic workflow / skill okuma | `claude-sonnet-4-6` |
| Kod / render / format dönüşüm | `claude-haiku-4-5-20251001` |
| **Web araştırması / internet search** | `claude-haiku-4-5-20251001` |

---

## Skill Haritası (Hızlı Referans)

| Ne istendi | Skill |
|-----------|-------|
| Reklam kopyası | `marketing/ad-creative` |
| Kampanya stratejisi | `marketing/paid-ads` |
| GEO / AI görünürlük | `marketing/ai-seo` |
| Sosyal medya içerik | `marketing/social-content` |
| Türkçe metin / blog | `marketing/copywriting` |
| Google Ads denetim | `advertising/ads-google` |
| Meta reklam | `advertising/ads-meta` |
| Tüm platform denetim | `advertising/ads-audit` |
| Görsel üret | `advertising/ads-generate` |
| **Sosyal medyaya yayınla** | `advertising/social-publisher` |
| PDF rapor | `advertising/ads-report` |
| SEO makale | `seo/seo-expert` |
| Video üret | `video/remotion` |

**Tam liste:** `.agents/MANIFEST.md` · **Skill klasörü:** `.agents/skills/<kategori>/<skill>/SKILL.md`

---

## İçerik Üretim Sırası

```
1. Post yaz       → content-repurposer / turkce-insani-yazar
2. Kullanıcı onayı al
3. Görsel üret    → canvas-design (statik) · HyperFrames (video)
4. Yayınla        → social-publisher skill (OmniSocials API)
```

> Görsel onaydan önce üretilmez. Yayın her zaman son adım.

---

## Video / Görsel Araçlar

| İhtiyaç | Araç | Komut |
|---------|------|-------|
| Video / animasyon | HyperFrames | `npx hyperframes render index.html -o cikti.mp4` |
| Statik görsel | canvas-design skill | — |
| Çıktı klasörü | `04-araclar/remotion-kaynak/out/` | — |

---

## Öncelik Listesi

1. ❌ **Dönüşüm takibi** — `analytics-tracking` skill → geo-hizmet form submit
2. ⏳ **GA4/GSC API key** — `04-araclar/seo-machine-modules/` için
3. 📊 **Günlük rapor ajanı** — Google Ads spend + anomali → Gmail
4. 📝 **Context dosyaları** — `context/` klasörünü Botfusions bilgileriyle doldur

---

## Kurallar

- Terminal: **her zaman PowerShell**, asla bash/Linux
- İçerik üretimde **önce yaz, onay al, sonra görsel**
- Agentic workflow tercih edilir, N8N yalnızca zorunluysa
- Detaylı API/skill bilgisi için `.agents/API-INTEGRATIONS.md` oku
- **Web/internet araştırması her zaman `claude-haiku-4-5-20251001` modeli ile yapılır** — token kullanımını minimize et

---

*Botfusions AI Reklam Ajansı · Mayıs 2026 · botfusions.com · info@botfusions.com · +90 850 302 74 60*
