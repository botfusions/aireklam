---
name: omni
description: >
  OmniSocials API ile görsel veya video içeriği tüm platformlara (Instagram,
  Facebook, TikTok, X, Pinterest, YouTube) yayınlar veya zamanlar.
  "yayınla", "tüm platformlara gönder", "OmniSocials'a at", "omni ile yayınla"
  tetikleyicilerinde çalıştırılır. Çalışan PowerShell scripti üretir.
version: 2.0.0
category: advertising
model: claude-haiku-4-5-20251001
---

# Omni — OmniSocials Yayın Skill

> **Önemli:** Claude'un sandbox'ı dışarıya bağlantı açamaz. Bu skill her zaman
> kullanıcının makinesinde çalışacak **PowerShell scripti** üretir.
> Kullanıcı scripti terminale paste eder veya dosyadan çalıştırır.

---

## Hesap Bilgileri

```
API_KEY  = {{OMNISOCIALS_API_KEY}}
BASE_URL = https://api.omnisocials.com/v1
```

| Platform   | Account ID           | Tip              |
|------------|----------------------|------------------|
| Instagram  | `881407_instagram`   | post, story, reel|
| Facebook   | `881407_facebook`    | post, story, reel|
| YouTube    | `881407_youtube`     | yalnızca reel    |
| TikTok     | `881407_tiktok`      | post, reel       |
| Pinterest  | `881407_pinterest`   | post             |
| X          | `881407_x`           | post (25K limit) |

**Pinterest Board'ları:**
- AI-Botfusions-GEO: `1091067515915706441`
- Profil: `1091067515915706431`

---

## Akış: Ne Zaman Ne Yapılır

```
Kullanıcı "yayınla" der
    ↓
1. Görsel/video dosyası var mı? → Yoksa canvas-design skill ile üret
2. Platform seçimi (hepsi mi, bazıları mı?)
3. Caption var mı? → Yoksa ad-creative/turkce-insani-yazar ile yaz
4. Zamanlama (hemen / belirli saat)?
5. PowerShell scripti üret → kullanıcıya ver
```

---

## Kritik Kurallar (Öğrenilmiş Hatalar)

### ✅ DOĞRU
- `curl.exe --ssl-no-revoke` kullan
- `media_ids` kullan (`data.id` upload'dan gelir)
- Türkçe path'i `Get-Item "C:\...\AI *Ajans*"` wildcard ile bul
- JSON'u `[System.IO.File]::WriteAllText()` ile yaz
- Pinterest'i **ayrı çağrı** ile gönder + `pinterest_board_id`
- `Out-File -Encoding utf8` kullan
- Tek satır curl komutları yaz (backtick `\`` yok)
- `$PSScriptRoot` fallback ekle

### ❌ YANLIŞ
- `media_urls` → çalışmıyor
- `System.Net.Http.HttpClient` ile upload → boş yanıt döner
- Türkçe `ı` harfini path'e hardcode etmek → `AjansÄ±` hatası
- Backtick satır devamı → terminale paste'de çalışmaz
- Pinterest'i diğer platformlarla aynı çağrıya koymak

---

## Medya Format Rehberi

| Format     | Boyut      | Platform               | Tip  |
|------------|------------|------------------------|------|
| 9:16 Dikey | 1080×1920  | IG Story/Reel, TikTok, YT Short | reel |
| 1:1 Kare   | 1080×1080  | IG Feed, FB, X         | post |
| 2:3 Dikey  | 1000×1500  | Pinterest              | post |

---

## Script Şablonu: GÖRSEL POST (Terminale Paste Edilebilir)

```powershell
# ── DEĞİŞTİRİLECEK ALANLAR ─────────────────────────────────────────
$GORSEL_PATH = "BURAYA\GORSELIN\TAM\YOLU.png"  # .png veya .jpg

$CAPTION_DEFAULT = "INSTAGRAM/FACEBOOK/TIKTOK METNI (Turkce karakter yok)"
$CAPTION_X       = "X METNI (max 280 karakter)"
$CAPTION_PIN     = "PINTEREST METNI (max 500 karakter, keyword odakli)"

$PINTEREST_BOARD = "1091067515915706441"   # AI-Botfusions-GEO
# ────────────────────────────────────────────────────────────────────

$API_KEY = "{{OMNISOCIALS_API_KEY}}"

if (-not (Test-Path -LiteralPath $GORSEL_PATH)) { Write-Host "HATA: Gorsel bulunamadi: $GORSEL_PATH" -ForegroundColor Red; exit }
Write-Host "Gorsel OK" -ForegroundColor Green

$T = "$env:TEMP\omni_upload.png"
Copy-Item -LiteralPath $GORSEL_PATH -Destination $T -Force

$up = curl.exe --ssl-no-revoke -s -S -X POST "https://api.omnisocials.com/v1/media/upload" -H "Authorization: Bearer $API_KEY" -F "file=@`"$T`";type=image/png"
Write-Host "Upload: $up"
Remove-Item $T -Force

$mid = ($up | ConvertFrom-Json).data.id
if (-not $mid) { Write-Host "HATA: media_id alinamadi" -ForegroundColor Red; exit }
Write-Host "Media ID: $mid" -ForegroundColor Green

$pf = "$env:TEMP\omni_post.json"
[System.IO.File]::WriteAllText($pf, "{`"content`":{`"default`":`"$CAPTION_DEFAULT`",`"x`":`"$CAPTION_X`"},`"accounts`":[`"881407_instagram`",`"881407_facebook`",`"881407_tiktok`",`"881407_x`"],`"media_ids`":[`"$mid`"],`"type`":`"post`"}")
$pr = curl.exe --ssl-no-revoke -s -S -X POST "https://api.omnisocials.com/v1/posts/create-and-publish" -H "Authorization: Bearer $API_KEY" -H "Content-Type: application/json" --data-binary "@$pf"
Write-Host "Post: $pr" -ForegroundColor Green
Remove-Item $pf -Force

$pinf = "$env:TEMP\omni_pin.json"
[System.IO.File]::WriteAllText($pinf, "{`"content`":{`"default`":`"$CAPTION_PIN`"},`"accounts`":[`"881407_pinterest`"],`"media_ids`":[`"$mid`"],`"type`":`"post`",`"pinterest_board_id`":`"$PINTEREST_BOARD`"}")
$pinr = curl.exe --ssl-no-revoke -s -S -X POST "https://api.omnisocials.com/v1/posts/create-and-publish" -H "Authorization: Bearer $API_KEY" -H "Content-Type: application/json" --data-binary "@$pinf"
Write-Host "Pinterest: $pinr" -ForegroundColor Green
Remove-Item $pinf -Force

Write-Host "TAMAMLANDI: IG + FB + TikTok + X + Pinterest" -ForegroundColor Green
```

---

## Script Şablonu: VİDEO REEL

```powershell
# ── DEĞİŞTİRİLECEK ALANLAR ─────────────────────────────────────────
$VIDEO_PATH      = "BURAYA\VIDEONUN\TAM\YOLU.mp4"
$CAPTION_DEFAULT = "CAPTION (Turkce karakter yok)"
$YOUTUBE_TITLE   = "YOUTUBE BASLIGI (max 100 karakter)"
$CAPTION_PIN     = "PINTEREST METNI"
$PINTEREST_BOARD = "1091067515915706441"
# ────────────────────────────────────────────────────────────────────

$API_KEY = "{{OMNISOCIALS_API_KEY}}"

$T = "$env:TEMP\omni_video.mp4"
Copy-Item -LiteralPath $VIDEO_PATH -Destination $T -Force

$up = curl.exe --ssl-no-revoke -s -S -X POST "https://api.omnisocials.com/v1/media/upload" -H "Authorization: Bearer $API_KEY" -F "file=@`"$T`";type=video/mp4"
Write-Host "Upload: $up"
Remove-Item $T -Force

$mid = ($up | ConvertFrom-Json).data.id
if (-not $mid) { Write-Host "HATA: media_id alinamadi" -ForegroundColor Red; exit }
Write-Host "Media ID: $mid" -ForegroundColor Green

$rf = "$env:TEMP\omni_reel.json"
[System.IO.File]::WriteAllText($rf, "{`"content`":{`"default`":`"$CAPTION_DEFAULT`",`"youtube`":`"$CAPTION_DEFAULT`"},`"accounts`":[`"881407_instagram`",`"881407_facebook`",`"881407_youtube`",`"881407_tiktok`"],`"media_ids`":[`"$mid`"],`"type`":`"reel`",`"youtube`":{`"title`":`"$YOUTUBE_TITLE`",`"privacy_status`":`"public`"},`"tiktok`":{`"privacy_level`":`"PUBLIC_TO_EVERYONE`"}}")
$rr = curl.exe --ssl-no-revoke -s -S -X POST "https://api.omnisocials.com/v1/posts/create-and-publish" -H "Authorization: Bearer $API_KEY" -H "Content-Type: application/json" --data-binary "@$rf"
Write-Host "Reel: $rr" -ForegroundColor Green
Remove-Item $rf -Force

Write-Host "TAMAMLANDI: IG + FB + YouTube + TikTok (Reel)" -ForegroundColor Green
```

---

## Bu Skill Çağrıldığında Yapılacaklar

1. **Görsel/video path'ini sor** (eğer verilmediyse)
2. **Caption'ları hazırla** (ad-creative veya turkce-insani-yazar skill ile, sonra Türkçe karakterleri ASCII'ye çevir: ş→s, ç→c, ğ→g, ü→u, ö→o, ı→i, İ→I)
3. **Script şablonunu** yukarıdan al, değişkenleri doldur
4. **Kullanıcıya ver:** "Tümünü seç → kopyala → PowerShell'e yapıştır"
5. **Sonucu sor:** `data.id` ve `status` değerlerini kaydet

---

## Bilinen Hatalar

| Hata | Sebep | Çözüm |
|------|-------|-------|
| Upload boş yanıt | HttpClient kullanıldı | curl.exe kullan |
| `AjansÄ±` path hatası | Türkçe `ı` hardcode | `Get-Item "...\AI *Ajans*"` wildcard |
| `data.id` null | `data.url` aranıyor | `($up \| ConvertFrom-Json).data.id` |
| Pinterest hata | Aynı çağrıda gönderildi | Ayrı çağrı + `pinterest_board_id` |
| Backtick çalışmıyor | Terminale paste | Tek satır curl kullan |

---

*Botfusions AI Reklam Ajansı · omni skill v2.0.0 · Mayıs 2026*
