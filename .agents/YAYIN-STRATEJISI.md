# Botfusions — Platform Yayın Stratejisi
**Tarih:** 14 Mayıs 2026 | **Versiyon:** 1.0

---

## Platform Matrisi

| Platform | İçerik Tipi | Format | Karakter | Not |
|----------|------------|--------|----------|-----|
| Instagram | Reel + Feed post | 9:16 video / 1:1 görsel | 2200 | İkisi de gönderilir |
| Facebook | Reel + Feed post | 9:16 video / 1:1 görsel | 63.206 | İkisi de gönderilir |
| YouTube | Shorts | 9:16 MP4, max 60sn | — | Ayrı title zorunlu |
| TikTok | Video post | 9:16 MP4 | — | |
| X (Twitter) | Yalnızca görsel | 1:1 veya 16:9 JPG/PNG | 280 | **Video desteklemiyor** |
| LinkedIn | Görsel + metin | 1.91:1 veya 1:1 | 3000 | Profesyonel ton |
| Pinterest | Görsel + metin | 2:3 dikey | 500 | Board seçimi gerekli |

---

## Her İçerik Parçası İçin Üretilecekler

### Zorunlu Varlıklar (Assets)
```
1. video_9x16.mp4       → Instagram Reel, Facebook Reel, YouTube Shorts, TikTok
2. image_1x1.jpg        → X, Instagram feed, Facebook feed
3. image_2x3.jpg        → Pinterest (veya 1x1 kırpılabilir)
4. image_linkedin.jpg   → LinkedIn (1.91:1 — opsiyonel, 1x1 de çalışır)
```

### Platform Bazlı Metinler
```
default    → Facebook, Instagram (2200 karakter altı)
x          → 280 karakter, kısa + link + hashtag
linkedin   → 1500-3000 karakter, profesyonel, 3-5 hashtag
pinterest  → 500 karakter, anahtar kelime odaklı, board belirtilmeli
youtube    → title (100 karakter), description (5000 karakter)
```

---

## OmniSocials API — 2 Çağrı Sistemi

### Çağrı A: Video Grubu
```json
{
  "content": {
    "default": "...(Instagram/Facebook metni)...",
    "youtube": "...(YouTube açıklaması)..."
  },
  "accounts": [
    "881407_instagram",
    "881407_facebook",
    "881407_youtube",
    "881407_tiktok"
  ],
  "media_urls": {
    "default": ["https://cdn.../video_9x16.mp4"]
  },
  "youtube_title": "Başlık buraya (max 100 karakter)"
}
```

### Çağrı B: Görsel Grubu
```json
{
  "content": {
    "default": "...(Instagram/Facebook feed metni)...",
    "x": "...(280 karakter)...",
    "linkedin": "...(profesyonel uzun metin)...",
    "pinterest": "...(500 karakter, keyword odaklı)..."
  },
  "accounts": [
    "881407_x",
    "881407_instagram",
    "881407_facebook",
    "881407_pinterest"
  ],
  "media_urls": {
    "default": ["https://cdn.../image_1x1.jpg"],
    "pinterest": ["https://cdn.../image_2x3.jpg"]
  },
  "pinterest_board_id": "1091067515915706441"
}
```

> **Not:** LinkedIn görsel postu için ayrı çağrı yapılabilir veya Çağrı B'ye eklenebilir.

---

## Yayın Akışı (SOP)

```
1. İÇERİK YAZIMI
   ├── default metin (FB + IG)
   ├── X metni (280 karakter)
   ├── LinkedIn metni (1500+ karakter)
   ├── Pinterest açıklaması (500 karakter)
   └── YouTube title + description

2. GÖRSEL ÜRETİMİ
   ├── video_9x16.mp4  ← HyperFrames / mevcut video
   └── image_1x1.jpg   ← canvas-design skill / infografik

3. KULLANICI ONAYI
   └── Metin + görselleri gözden geçir → onayla

4. YAYINLAMA
   ├── Çağrı A: Video → Instagram + Facebook + YouTube + TikTok
   └── Çağrı B: Görsel → X + Instagram + Facebook + Pinterest

5. KAYIT
   ├── social_posts tablosuna her çağrı için kayıt
   └── Dashboard'da durum takibi
```

---

## Dashboard Güncellemeleri Gerekli

### gsc_api_server.py — Yeni Endpoint'ler
```python
# Çağrı A: Video yayınla
POST /api/publish/video
# Çağrı B: Görsel yayınla  
POST /api/publish/image
# Her ikisini birden
POST /api/publish/full
```

### cmo-dashboard.html — Yeni UI
- "Yayın Oluştur" butonu → Modal aç
- Modal: Metin alanları (platform bazlı) + görsel/video yükle
- Önizleme: Her platform için nasıl görüneceği
- Yayınla: İki API çağrısı tetikle

---

## Boyut Referansı

| Format | Boyut | Kullanım |
|--------|-------|----------|
| 9:16 Dikey | 1080x1920 | Reel, Shorts, TikTok |
| 1:1 Kare | 1080x1080 | X, Instagram feed, FB feed |
| 2:3 Dikey | 1000x1500 | Pinterest |
| 16:9 Yatay | 1920x1080 | LinkedIn banner, YouTube thumbnail |

---

## Pinterest Board'ları

| Board Adı | Board ID | Kullanım |
|-----------|---------|---------|
| AI-Botfusions-GEO | 1091067515915706441 | GEO/AI içerikler |
| Profil | 1091067515915706431 | Genel Botfusions |

---

*Botfusions AI Reklam Ajansı · botfusions.com*
