# =====================================================
# Botfusions -- GEO Post Yayin Scripti
# 15 Mayis 2026
# Cagri A: Video (IG+FB+YT+TikTok Reel)
# Cagri B: Infografik (X+IG+FB+Pinterest post)
# Supabase social_posts tablosuna otomatik kayit
# =====================================================

$API_KEY     = $env:OMNISOCIALS_API_KEY
if (-not $API_KEY) {
    Write-Host "HATA: OMNISOCIALS_API_KEY ortam degiskeni bulunamadi." -ForegroundColor Red
    Write-Host "Cozum: secrets.env dosyasini olusturun veya asagidaki komutu calistirin:"
    Write-Host '  $env:OMNISOCIALS_API_KEY = "omsk_live_xxxxx"'
    exit 1
}
$SUPA_URL    = $env:SUPABASE_URL ?? "https://supabase.turklawai.com"
$SUPA_KEY    = $env:SUPABASE_ANON_KEY
if (-not $SUPA_KEY) {
    Write-Host "HATA: SUPABASE_ANON_KEY ortam degiskeni bulunamadi." -ForegroundColor Red
    exit 1
}
$CAMPAIGN    = "GEO-Varlik-Optimizasyonu-$(Get-Date -Format 'yyyy-MM-dd')"

# Supabase'e kayit fonksiyonu
function Save-ToSupabase {
    param($PostId, $Caption, $Platforms, $PostType, $YoutubeTitle = "")
    $body = "$env:TEMP\supa_log.json"
    $platformsJson = ($Platforms | ForEach-Object { "`"$_`"" }) -join ","
    @"
{
  "omnisocials_post_id": "$PostId",
  "caption": "$Caption",
  "platforms": [$platformsJson],
  "post_type": "$PostType",
  "status": "posting",
  "campaign": "$CAMPAIGN",
  "youtube_title": "$YoutubeTitle",
  "published_at": "$(Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ')"
}
"@ | Out-File $body -Encoding utf8
    $result = curl.exe --ssl-no-revoke -s `
        -X POST "$SUPA_URL/rest/v1/social_posts" `
        -H "Authorization: Bearer $SUPA_KEY" `
        -H "apikey: $SUPA_KEY" `
        -H "Content-Type: application/json" `
        -H "Prefer: return=minimal" `
        --data-binary "@$body"
    Remove-Item $body -Force
    if ($result -and $result -ne "") {
        Write-Host "  Supabase kayit: $result" -ForegroundColor DarkGray
    } else {
        Write-Host "  Supabase kayit: OK" -ForegroundColor DarkGray
    }
}
$VIDEO_SRC   = Join-Path $PSScriptRoot "04-araclar\remotion-kaynak\out\geo-post-45s.mp4"
$IMAGE_SRC   = Join-Path $PSScriptRoot "out\geo-infografik-1x1-2026-05-15.png"
$IMAGE_PIN   = Join-Path $PSScriptRoot "out\geo-infografik-2x3-pinterest-2026-05-15.png"

$CAPTION_DEFAULT = "Yapay zeka seni neden onermez? Cunku seni bir varlik olarak tanımiyor. Buna GEO diyoruz. Knowledge Graph girisi, JSON-LD yapisal veri, varlik iliskilendirmesi ve Topical Authority ile markanizi AI'in hafizasina yerlestiriyoruz. ChatGPT bahsetme orani %13, Claude %9 -- ve yukseltiyoruz. Sitenizi ucretsiz analiz etmemizi ister misiniz? botfusions.com/geo-hizmet #GEO #EntityOptimization #AIMarketing #Botfusions"

$CAPTION_X = "Yapay zeka seni neden onermez? Cunku seni bir varlik olarak tanımiyor. GEO ile AI hafizasina girin: Knowledge Graph + JSON-LD + Entity Authority botfusions.com/geo-hizmet #GEO #AIMarketing"

$CAPTION_PINTEREST = "GEO - Generative Engine Optimization: Yapay zekanin hafizasina girmek icin 4 adim. Knowledge Graph Wikidata, Varlik Iliskilendirmesi, JSON-LD Yapisal Veri, Topical Authority. Botfusions GEO Hizmeti ile markanizi AI motorlarinda gorunur kilin. botfusions.com/geo-hizmet"

$YOUTUBE_TITLE = "GEO Nedir? Yapay Zeka Sizi Neden Onermez | Botfusions"

# =====================================================
# CAGRI A - VIDEO YUKLEME + REEL YAYINI
# =====================================================
Write-Host ""
Write-Host "=== CAGRI A: VIDEO ===" -ForegroundColor Magenta

# Video yukle
Write-Host "[1/4] Video yukleniyor..." -ForegroundColor Cyan
$VIDEO_TEMP = "$env:TEMP\geo_post_video.mp4"
Copy-Item -LiteralPath $VIDEO_SRC -Destination $VIDEO_TEMP -Force

$videoUpload = curl.exe --ssl-no-revoke -s `
    -X POST "https://api.omnisocials.com/v1/media/upload" `
    -H "Authorization: Bearer $API_KEY" `
    -F "file=@`"$VIDEO_TEMP`";type=video/mp4"

Write-Host "Yanit: $videoUpload"
$videoResult  = $videoUpload | ConvertFrom-Json
$VIDEO_MEDIA_ID = $videoResult.data.id

if (-not $VIDEO_MEDIA_ID) {
    Write-Host "HATA: Video Media ID alinamadi!" -ForegroundColor Red
    exit 1
}
Write-Host "Video Media ID: $VIDEO_MEDIA_ID" -ForegroundColor Green
Remove-Item $VIDEO_TEMP -Force

# Reel yayinla
Write-Host "[2/4] Reel yayinlaniyor (IG + FB + YT + TikTok)..." -ForegroundColor Cyan
$reelFile = "$env:TEMP\geo_reel.json"
@"
{
  "content": {
    "default": "$CAPTION_DEFAULT",
    "youtube": "$CAPTION_DEFAULT"
  },
  "accounts": ["881407_instagram","881407_facebook","881407_youtube","881407_tiktok"],
  "media_ids": ["$VIDEO_MEDIA_ID"],
  "type": "reel",
  "youtube": { "title": "$YOUTUBE_TITLE", "privacy_status": "public" },
  "tiktok": { "privacy_level": "PUBLIC_TO_EVERYONE" }
}
"@ | Out-File -FilePath $reelFile -Encoding utf8

$reelResult = curl.exe --ssl-no-revoke -s `
    -X POST "https://api.omnisocials.com/v1/posts/create-and-publish" `
    -H "Authorization: Bearer $API_KEY" `
    -H "Content-Type: application/json" `
    --data-binary "@$reelFile"

Write-Host "Reel sonucu: $reelResult" -ForegroundColor Green
Remove-Item $reelFile -Force
$reelPostId = ($reelResult | ConvertFrom-Json).data.id
Save-ToSupabase -PostId $reelPostId -Caption $CAPTION_DEFAULT -Platforms @("instagram","facebook","youtube","tiktok") -PostType "reel" -YoutubeTitle $YOUTUBE_TITLE
Write-Host "Supabase kaydi: Reel" -ForegroundColor DarkGreen

# =====================================================
# CAGRI B - INFOGRAFIK YUKLEME + POST YAYINI
# =====================================================
Write-Host ""
Write-Host "=== CAGRI B: INFOGRAFIK ===" -ForegroundColor Magenta

# 1:1 gorsel yukle (X, IG, FB)
Write-Host "[3/4] Infografik (1:1) yukleniyor..." -ForegroundColor Cyan
$IMG_TEMP = "$env:TEMP\geo_infografik_1x1.png"
Copy-Item -LiteralPath $IMAGE_SRC -Destination $IMG_TEMP -Force

$imgUpload = curl.exe --ssl-no-revoke -s `
    -X POST "https://api.omnisocials.com/v1/media/upload" `
    -H "Authorization: Bearer $API_KEY" `
    -F "file=@`"$IMG_TEMP`";type=image/png"

Write-Host "Yanit: $imgUpload"
$imgResult = $imgUpload | ConvertFrom-Json
$IMG_MEDIA_ID = $imgResult.data.id

if (-not $IMG_MEDIA_ID) {
    Write-Host "HATA: Gorsel Media ID alinamadi!" -ForegroundColor Red
    exit 1
}
Write-Host "Gorsel Media ID: $IMG_MEDIA_ID" -ForegroundColor Green
Remove-Item $IMG_TEMP -Force

# Pinterest 2:3 gorsel yukle
Write-Host "[4/4] Pinterest gorseli (2:3) yukleniyor..." -ForegroundColor Cyan
$PIN_TEMP = "$env:TEMP\geo_infografik_2x3.png"
Copy-Item -LiteralPath $IMAGE_PIN -Destination $PIN_TEMP -Force

$pinUpload = curl.exe --ssl-no-revoke -s `
    -X POST "https://api.omnisocials.com/v1/media/upload" `
    -H "Authorization: Bearer $API_KEY" `
    -F "file=@`"$PIN_TEMP`";type=image/png"

$pinResult = $pinUpload | ConvertFrom-Json
$PIN_MEDIA_ID = $pinResult.data.id
Write-Host "Pinterest Media ID: $PIN_MEDIA_ID" -ForegroundColor Green
Remove-Item $PIN_TEMP -Force

# Post yayinla (X + IG + FB)
$postFile = "$env:TEMP\geo_post.json"
@"
{
  "content": {
    "default": "$CAPTION_DEFAULT",
    "x": "$CAPTION_X"
  },
  "accounts": ["881407_x","881407_instagram","881407_facebook"],
  "media_ids": ["$IMG_MEDIA_ID"],
  "type": "post"
}
"@ | Out-File -FilePath $postFile -Encoding utf8

$postResult = curl.exe --ssl-no-revoke -s `
    -X POST "https://api.omnisocials.com/v1/posts/create-and-publish" `
    -H "Authorization: Bearer $API_KEY" `
    -H "Content-Type: application/json" `
    --data-binary "@$postFile"

Write-Host "Post sonucu: $postResult" -ForegroundColor Green
Remove-Item $postFile -Force
$postPostId = ($postResult | ConvertFrom-Json).data.id
Save-ToSupabase -PostId $postPostId -Caption $CAPTION_DEFAULT -Platforms @("instagram","facebook","x") -PostType "post"
Write-Host "Supabase kaydi: Gorsel Post" -ForegroundColor DarkGreen

# Pinterest ayri yayinla
$pinPostFile = "$env:TEMP\geo_pinterest.json"
@"
{
  "content": {
    "default": "$CAPTION_PINTEREST"
  },
  "accounts": ["881407_pinterest"],
  "media_ids": ["$PIN_MEDIA_ID"],
  "type": "post",
  "pinterest_board_id": "1091067515915706441"
}
"@ | Out-File -FilePath $pinPostFile -Encoding utf8

$pinPostResult = curl.exe --ssl-no-revoke -s `
    -X POST "https://api.omnisocials.com/v1/posts/create-and-publish" `
    -H "Authorization: Bearer $API_KEY" `
    -H "Content-Type: application/json" `
    --data-binary "@$pinPostFile"

Write-Host "Pinterest sonucu: $pinPostResult" -ForegroundColor Green
Remove-Item $pinPostFile -Force
$pinPostId = ($pinPostResult | ConvertFrom-Json).data.id
Save-ToSupabase -PostId $pinPostId -Caption $CAPTION_PINTEREST -Platforms @("pinterest") -PostType "post"
Write-Host "Supabase kaydi: Pinterest" -ForegroundColor DarkGreen

Write-Host ""
Write-Host "=== TUM YAYINLAR TAMAMLANDI ===" -ForegroundColor Green
Write-Host "Cagri A: Video -> Instagram + Facebook + YouTube + TikTok (Reel)"
Write-Host "Cagri B: Infografik -> X + Instagram + Facebook (Post) + Pinterest"
Write-Host "Supabase: 3 kayit eklendi -> CMO Dashboard'da gorunur" -ForegroundColor Cyan
