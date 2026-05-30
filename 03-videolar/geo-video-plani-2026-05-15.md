# GEO Video Planı — HyperFrames
**Tarih:** 15 Mayıs 2026 | **Araç:** HyperFrames (index.html → mp4)  
**Süre:** ~30–45 saniye | **Format:** 1080×1350 (Reels/TikTok) veya 1080×1080 (kare)  
**Müzik:** Ayrı sağlanacak (background track)

---

## Genel Konsept

**Mesaj:** "Yapay zeka seni tanımıyorsa, seni önermez."  
**Ton:** Minimalist, teknik-cool, karanlık arka plan + mor/mavi neon aksanlar  
**Hedef:** LinkedIn Reels, Instagram Reels, TikTok

---

## Sahne Planı (2 Görsel + Animasyon Katmanları)

### 🎬 SAHNE 1 — Açılış (0:00 – 0:08)
**Kullanılacak:** Siyah ekran → Text animasyonu

```
Animasyon: Fade-in (opacity 0 → 1, 1.2s)
Metin: "Yapay zeka seni neden önermez?"
Font: Büyük, beyaz, bold
Efekt: Metin soldan kayarak gelir (translateX: -40px → 0)
Müzik: Beat başlar (0. saniye)
```

---

### 🎬 SAHNE 2 — Görsel 1 (0:08 – 0:18)
**Kullanılacak:** [Görsel 1 — kullanıcı tarafından sağlanacak]

```
Animasyon Katmanları:
1. Görsel: Scale 1.05 → 1.0 (Ken Burns etkisi, 10s)
2. Overlay: Mor gradient (sol kenar, opacity 0.4)
3. Üst metin: "Çünkü seni bir 'varlık' olarak tanımıyor."
   → Görsel üzerinde, alt orta, fade-in (0.5s gecikme)
4. Alt etiket: "#EntityOptimization" — küçük, mor, opacity 0.7

Geçiş: Cross-fade (0.4s) → Sahne 3
```

---

### 🎬 SAHNE 3 — Ana Mesaj / İnfografik Özeti (0:18 – 0:32)
**Kullanılacak:** Animasyonlu liste (kod ile oluşturulur)

```
4 madde sırayla belirir (her biri 0.3s arayla):
  01 → Knowledge Graph   [mor]
  02 → Varlık İlişkilendirmesi  [mavi]
  03 → JSON-LD Yapısal Veri  [turuncu]
  04 → Topical Authority  [mor]

Animasyon: Her madde soldan kayar (translateX: -30px → 0, opacity 0→1)
Arka plan: Koyu (#0a0a1a) + ince grid çizgiler (opacity 0.05)
Müzik: Yükseliş noktası
```

---

### 🎬 SAHNE 4 — Görsel 2 (0:32 – 0:42)
**Kullanılacak:** [Görsel 2 — kullanıcı tarafından sağlanacak]

```
Animasyon Katmanları:
1. Görsel: Tam ekran, scale 1.0 → 1.04
2. Overlay: Koyu vignette (kenarlar)
3. Merkez metin: "GEO Stratejisi" — büyük, mor
4. Alt metin: "Yapay zekanın hafızasına gir." — küçük, beyaz

Geçiş: Fade to black (0.6s)
```

---

### 🎬 SAHNE 5 — CTA Kapanış (0:42 – 0:50)
**Kullanılacak:** Animasyonlu logo + CTA

```
Animasyon:
1. Botfusions logosu/adı: Fade-in, ortada
2. Alt metin: "botfusions.com" — soluk mor
3. CTA badge: "Sitenizi Analiz Edelim →" 
   → Çerçeveli, mor outline, pulse animasyonu

Müzik: Fade-out son 2 saniye
Son kare: 1 saniye sabit durur (thumbnail için ideal)
```

---

## HyperFrames Teknik Notlar

```bash
# Render komutu
npx hyperframes render index.html -o out/geo-video-2026-05-15.mp4

# Çıktı klasörü
04-araclar/remotion-kaynak/out/
```

### index.html Yapısı
```
/ (proje kökü)
├── index.html         ← Ana video dosyası
├── assets/
│   ├── gorsel-1.jpg   ← Kullanıcı sağlayacak
│   ├── gorsel-2.jpg   ← Kullanıcı sağlayacak
│   └── muzik.mp3      ← Kullanıcı sağlayacak
└── out/
    └── geo-video-2026-05-15.mp4
```

### Müzik Sync Noktaları
| Saniye | Olay |
|--------|------|
| 0:00 | Beat başlar |
| 0:08 | Görsel 1 giriş (downbeat) |
| 0:18 | Liste animasyonu (ritim hızlanır) |
| 0:32 | Görsel 2 (müzik yükselir) |
| 0:42 | CTA (müzik fade-out) |

---

## Renk Referansı (HyperFrames CSS)

```css
:root {
  --bg: #0a0a1a;
  --purple: #A855F7;
  --purple-dark: #7C3AED;
  --blue: #3B82F6;
  --orange: #F97316;
  --text: #ffffff;
  --text-muted: #94a3b8;
}
```

---

## Bir Sonraki Adım

1. **Görsel 1 ve Görsel 2'yi paylaş** → index.html'e yerleştireceğim
2. **Müzik dosyasını ekle** → sync noktalarını finalleştireceğim
3. **HyperFrames ile render** → `npx hyperframes render index.html -o geo-video.mp4`

---

*Botfusions AI Reklam Ajansı · Mayıs 2026*
