# =====================================================
# Botfusions -- OmniSocials Yayin Scripti
# =====================================================

$API_KEY    = $env:OMNISOCIALS_API_KEY
if (-not $API_KEY) {
    Write-Host "HATA: OMNISOCIALS_API_KEY ortam degiskeni bulunamadi." -ForegroundColor Red
    Write-Host "Cozum: secrets.env dosyasini olusturun veya asagidaki komutu calistirin:"
    Write-Host '  $env:OMNISOCIALS_API_KEY = "omsk_live_xxxxx"'
    exit 1
}
$VIDEO_SRC  = Join-Path $PSScriptRoot "04-araclar\remotion-kaynak\out\linkedin-ad-45s.mp4"
$VIDEO_TEMP = "$env:TEMP\bot_video.mp4"

$CAPTION = "Geleneksel SEO mavi link dunyasi, yerini hizla yapay zekanin yonlendirdigi Atif Ekonomisi Citation Economy birakiyor. Gartner verilerine gore geleneksel arama motoru trafiginin yuzde 25i artik yapay zeka asistanlarina kaymis durumda. LLM platformlarinin urettigi yanit setlerinde guvenilir bir kaynak ve atif olarak konumlanmak artik en onemli basari kriteri. Yapay zeka motorlarinin markanizi tanmasi ve onermesi icin gelistirdigimiz cok katmanli optimizasyon: Davranissal Zeka Digital Twins, Makine Anlasabilirligi Interpretability Optimization, Varlik Otoritesi Entity Authority ve Coklu Model Gorunurluk Takibi. ChatGPT, Gemini, Perplexity ve Claude gibi tum buyuk dil modellerinde es zamanli gorunurluk skorunuzu takip ediyoruz. #SEO #AI #SearchEngineOptimization #GenerativeAI #ArtificialIntelligence #CitationEconomy"

$YOUTUBE_TITLE = "Atif Ekonomisi: Yapay Zeka Caginda SEO | Botfusions GEO"

# =====================================================
# ADIM 0 - Videoyu bossuz yola kopyala
# =====================================================
Write-Host "[0/3] Video gecici konuma kopyalaniyor..." -ForegroundColor Cyan
Write-Host "Kaynak: $VIDEO_SRC"

Copy-Item -LiteralPath $VIDEO_SRC -Destination $VIDEO_TEMP -Force
if (-not (Test-Path $VIDEO_TEMP)) {
    Write-Host "HATA: Video kopyalanamadi!" -ForegroundColor Red
    exit 1
}
Write-Host "Kopyalandi: $VIDEO_TEMP" -ForegroundColor Green

# =====================================================
# ADIM 1 - VIDEO YUKLE
# =====================================================
Write-Host ""
Write-Host "[1/3] Video yukleniyor..." -ForegroundColor Cyan

$uploadJson = curl.exe -s `
    -X POST "https://api.omnisocials.com/v1/media/upload" `
    -H "Authorization: Bearer $API_KEY" `
    -F "file=@`"$VIDEO_TEMP`";type=video/mp4"

Write-Host "Upload yaniti: $uploadJson"

if (-not $uploadJson) {
    Write-Host "HATA: API yanit vermedi." -ForegroundColor Red
    Remove-Item $VIDEO_TEMP -Force
    exit 1
}

$uploadResult = $uploadJson | ConvertFrom-Json
$MEDIA_ID = $uploadResult.id

if (-not $MEDIA_ID) {
    Write-Host "HATA: Media ID alinamadi." -ForegroundColor Red
    Remove-Item $VIDEO_TEMP -Force
    exit 1
}

Write-Host "Video yuklendi -- Media ID: $MEDIA_ID" -ForegroundColor Green
Remove-Item $VIDEO_TEMP -Force

# =====================================================
# ADIM 2 - REEL: Instagram, Facebook, YouTube, TikTok
# =====================================================
Write-Host ""
Write-Host "[2/3] Reel yayinlaniyor (Instagram, Facebook, YouTube, TikTok)..." -ForegroundColor Cyan

$reelBodyFile = "$env:TEMP\omni_reel.json"
@"
{
  "content": { "default": "$CAPTION" },
  "accounts": ["881407_instagram","881407_facebook","881407_youtube","881407_tiktok"],
  "media_ids": ["$MEDIA_ID"],
  "type": "reel",
  "youtube": { "title": "$YOUTUBE_TITLE", "privacy_status": "public" },
  "tiktok": { "privacy_level": "PUBLIC_TO_EVERYONE" }
}
"@ | Out-File -FilePath $reelBodyFile -Encoding utf8

$reelResult = curl.exe -s `
    -X POST "https://api.omnisocials.com/v1/posts/create-and-publish" `
    -H "Authorization: Bearer $API_KEY" `
    -H "Content-Type: application/json" `
    --data-binary "@$reelBodyFile"

Write-Host "Reel sonucu:" -ForegroundColor Green
Write-Host $reelResult

# =====================================================
# ADIM 3 - POST: X
# =====================================================
Write-Host ""
Write-Host "[3/3] X Twitter yayinlaniyor..." -ForegroundColor Cyan

$xBodyFile = "$env:TEMP\omni_x.json"
@"
{
  "content": { "default": "$CAPTION" },
  "accounts": ["881407_x"],
  "media_ids": ["$MEDIA_ID"],
  "type": "post"
}
"@ | Out-File -FilePath $xBodyFile -Encoding utf8

$xResult = curl.exe -s `
    -X POST "https://api.omnisocials.com/v1/posts/create-and-publish" `
    -H "Authorization: Bearer $API_KEY" `
    -H "Content-Type: application/json" `
    --data-binary "@$xBodyFile"

Write-Host "X sonucu:" -ForegroundColor Green
Write-Host $xResult

Write-Host ""
Write-Host "TAMAMLANDI -- Instagram, Facebook, YouTube, TikTok, X" -ForegroundColor Green
