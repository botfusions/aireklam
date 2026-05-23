# OmniSocials — Yayın Rehberi
> **Her yayın öncesi bu dosyayı oku. Doğru sırayı takip et.**
> Son güncelleme: 15 Mayıs 2026

---

## Hesap Bilgileri

| Bilgi | Değer |
|-------|-------|
| API Key | `{{OMNISOCIALS_API_KEY}}` |
| Workspace | Botfusions (881407) |
| Dashboard | https://app.omnisocials.com |
| Dokümantasyon | https://docs.omnisocials.com |

---

## Bağlı Hesaplar

| Platform | Account ID | Kullanıcı | Desteklenen |
|----------|-----------|-----------|-------------|
| Instagram | `881407_instagram` | @botfusions | post, story, reel |
| Facebook | `881407_facebook` | Ömer Tokgöz | post, story, reel |
| YouTube | `881407_youtube` | @botfusionss | reel (Short) — title zorunlu |
| TikTok | `881407_tiktok` | @botfusions | post, reel |
| Pinterest | `881407_pinterest` | cenk0342 | post (yalnızca görsel) |
| X | `881407_x` | @botfusionss | post (X Premium, 25K limit) |

---

## Platform Matrisi — Ne Nereye Gider?

| İçerik | Format | Platformlar | Yayın Tipi |
|--------|--------|-------------|------------|
| Video | 9:16 MP4, max 60sn | Instagram + Facebook + YouTube + TikTok | `reel` |
| Görsel (feed) | 1:1 PNG/JPG (1080x1080) | Instagram + Facebook + X | `post` |
| Görsel (Pinterest) | 2:3 PNG/JPG (1000x1500) | Pinterest | `post` |

> **Pinterest sadece görsel alır — video gönderilemez.**
> **YouTube için `youtube.title` zorunlu.**

---

## ✅ Çalışan Yayın Akışı (15 Mayıs 2026)

### Genel Kural
- Dosyayı direkt `/v1/media/upload` ile yükle (`-F file=@"dosya"`)
- Yanıt `data.id` altında gelir → bunu `media_ids` olarak kullan
- JSON body'yi her zaman `$env:TEMP` dosyasına yaz, `--data-binary "@dosya"` ile gönder
- Her curl.exe'ye `--ssl-no-revoke` ekle

---

### ÇAĞRI A — Video Yayını (Reel)
**Hedef:** Instagram + Facebook + YouTube + TikTok

**Adım 1: Videoyu yükle**
```powershell
$VIDEO_TEMP = "$env:TEMP\video.mp4"
Copy-Item -LiteralPath ".\04-araclar\remotion-kaynak\out\GEO-VIDEO-DOSYASI.mp4" -Destination $VIDEO_TEMP -Force

$upload = curl.exe --ssl-no-revoke -s `
    -X POST "https://api.omnisocials.com/v1/media/upload" `
    -H "Authorization: Bearer {{OMNISOCIALS_API_KEY}}" `
    -F "file=@`"$VIDEO_TEMP`";type=video/mp4"

$MEDIA_ID = ($upload | ConvertFrom-Json).data.id
Write-Host "Video Media ID: $MEDIA_ID"
Remove-Item $VIDEO_TEMP -Force
```

**Adım 2: Reel yayınla**
```powershell
$body = "$env:TEMP\reel.json"
@"
{
  "content": {
    "default": "INSTAGRAM/FACEBOOK/TIKTOK METNİ",
    "youtube": "YOUTUBE AÇIKLAMASI"
  },
  "accounts": ["881407_instagram","881407_facebook","881407_youtube","881407_tiktok"],
  "media_ids": ["$MEDIA_ID"],
  "type": "reel",
  "youtube": { "title": "YOUTUBE BAŞLIĞI (max 100 karakter)", "privacy_status": "public" },
  "tiktok": { "privacy_level": "PUBLIC_TO_EVERYONE" }
}
"@ | Out-File $body -Encoding utf8

curl.exe --ssl-no-revoke -s `
    -X POST "https://api.omnisocials.com/v1/posts/create-and-publish" `
    -H "Authorization: Bearer {{OMNISOCIALS_API_KEY}}" `
    -H "Content-Type: application/json" `
    --data-binary "@$body"
Remove-Item $body -Force
```

---

### ÇAĞRI B — Görsel Yayını (Post)
**Hedef:** Instagram + Facebook + X + Pinterest (ayrı çağrı)

**Adım 1: 1:1 görseli yükle**
```powershell
$IMG_TEMP = "$env:TEMP\gorsel_1x1.png"
Copy-Item -LiteralPath ".\out\INFOGRAFIK-1x1.png" -Destination $IMG_TEMP -Force

$imgUpload = curl.exe --ssl-no-revoke -s `
    -X POST "https://api.omnisocials.com/v1/media/upload" `
    -H "Authorization: Bearer {{OMNISOCIALS_API_KEY}}" `
    -F "file=@`"$IMG_TEMP`";type=image/png"

$IMG_ID = ($imgUpload | ConvertFrom-Json).data.id
Write-Host "Görsel Media ID: $IMG_ID"
Remove-Item $IMG_TEMP -Force
```

**Adım 2: Post yayınla (IG + FB + X)**
```powershell
$body = "$env:TEMP\post.json"
@"
{
  "content": {
    "default": "INSTAGRAM/FACEBOOK METNİ",
    "x": "X METNİ (max 280 karakter)"
  },
  "accounts": ["881407_instagram","881407_facebook","881407_x"],
  "media_ids": ["$IMG_ID"],
  "type": "post"
}
"@ | Out-File $body -Encoding utf8

curl.exe --ssl-no-revoke -s `
    -X POST "https://api.omnisocials.com/v1/posts/create-and-publish" `
    -H "Authorization: Bearer {{OMNISOCIALS_API_KEY}}" `
    -H "Content-Type: application/json" `
    --data-binary "@$body"
Remove-Item $body -Force
```

**Adım 3: 2:3 görseli yükle ve Pinterest'e yayınla**
```powershell
$PIN_TEMP = "$env:TEMP\gorsel_2x3.png"
Copy-Item -LiteralPath ".\out\INFOGRAFIK-2x3.png" -Destination $PIN_TEMP -Force

$pinUpload = curl.exe --ssl-no-revoke -s `
    -X POST "https://api.omnisocials.com/v1/media/upload" `
    -H "Authorization: Bearer {{OMNISOCIALS_API_KEY}}" `
    -F "file=@`"$PIN_TEMP`";type=image/png"

$PIN_ID = ($pinUpload | ConvertFrom-Json).data.id
Remove-Item $PIN_TEMP -Force

$body = "$env:TEMP\pinterest.json"
@"
{
  "content": { "default": "PİNTEREST AÇIKLAMASI (keyword odaklı, 500 karakter)" },
  "accounts": ["881407_pinterest"],
  "media_ids": ["$PIN_ID"],
  "type": "post",
  "pinterest_board_id": "1091067515915706441"
}
"@ | Out-File $body -Encoding utf8

curl.exe --ssl-no-revoke -s `
    -X POST "https://api.omnisocials.com/v1/posts/create-and-publish" `
    -H "Authorization: Bearer {{OMNISOCIALS_API_KEY}}" `
    -H "Content-Type: application/json" `
    --data-binary "@$body"
Remove-Item $body -Force
```

---

## Hazır Script — Tek Seferde Yayınla

Yeni içerik için `yayinla-geo-post.ps1` şablonunu kopyala, metinleri değiştir, çalıştır:

```powershell
cd "C:\Users\user\Downloads\Z.ai_claude code\AI  Reklam  Ajansı"
.\yayinla-geo-post.ps1
```

Yeni içerik için şunu değiştirmek yeterli:
- `$VIDEO_SRC` → yeni video dosyası
- `$IMAGE_SRC` → yeni 1:1 infografik
- `$IMAGE_PIN` → yeni 2:3 infografik
- `$CAPTION_DEFAULT`, `$CAPTION_X`, `$CAPTION_PINTEREST` → metinler
- `$YOUTUBE_TITLE` → YouTube başlığı

---

## Pinterest Board'ları

| Board | ID | Kullanım |
|-------|----|---------|
| AI-Botfusions-GEO | `1091067515915706441` | GEO/AI içerikler |
| Profil | `1091067515915706431` | Genel Botfusions |

---

## Görsel Format Rehberi

| Format | Boyut | Platform |
|--------|-------|---------|
| 9:16 Dikey | 1080×1920 | Reel, Short, TikTok |
| 1:1 Kare | 1080×1080 | Instagram feed, Facebook, X |
| 2:3 Dikey | 1000×1500 | Pinterest |

> Infografikleri 3 formatta üretmek için `canvas-design` skill + Python cairosvg kullan.
> Video görsellerini 9:16 crop etmek için Pillow kullan.

---

## Bilinen Hatalar ve Çözümler

| Hata | Sebep | Çözüm |
|------|-------|-------|
| `invalid_api_key` | Key yanlış yazılmış | OMNISOCIALS.md'den kopyala |
| `data.id` boş geliyor | `$result.id` yerine `$result.data.id` | `.data.id` kullan |
| Türkçe karakter bozulması | PowerShell encoding | Metin içinde ö,ü,ş,ç,ğ,ı kullanma |
| `AjansÄ±` path hatası | Hardcoded Türkçe path | `$PSScriptRoot` ve `Join-Path` kullan |
| SSL sertifika hatası | Windows Schannel | `--ssl-no-revoke` ekle |
| 500 upload-from-url | Google Drive link formatı | Direkt `/v1/media/upload` kullan (`-F file=@`) |

---

## Başarılı Yayın Geçmişi

| Tarih | İçerik | Video ID | Görsel ID | Platformlar |
|-------|--------|----------|-----------|-------------|
| 14 Mayıs 2026 | Atıf Ekonomisi / GEO | 1881 | — | IG ✅ FB ✅ YT ✅ TikTok ✅ X ✅ |
| 15 Mayıs 2026 | GEO Varlık Optimizasyonu | 2214 | — | IG ✅ FB ✅ YT ✅ TikTok ✅ X ✅ Pinterest ✅ |

---

*Botfusions AI Reklam Ajansı · botfusions.com · Mayıs 2026*
