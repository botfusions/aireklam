# =====================================================
# Botfusions -- GEO SEO Video Yayin Scripti
# 26 Mayis 2026
# Cagri A: Video (IG + FB + YT + TikTok Reel)
# Cagri B: Gorsel (X + IG + FB + Pinterest Post)
# =====================================================

if ($PSScriptRoot) { $ROOT = $PSScriptRoot } else { $ROOT = (Get-Item "C:\Users\user\Downloads\Z.ai_claude code\AI *Ajans*").FullName }

# secrets.env otomatik yukle
$secretsFile = Join-Path $ROOT "secrets.env"
if (Test-Path $secretsFile) {
    Get-Content $secretsFile | ForEach-Object {
        if ($_ -match "^\s*([^#][^=]+)=(.+)$") {
            [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), "Process")
        }
    }
    Write-Host "secrets.env yuklendi." -ForegroundColor DarkGray
}

$API_KEY  = $env:OMNISOCIALS_API_KEY
$SUPA_URL = if ($env:SUPABASE_URL) { $env:SUPABASE_URL } else { "https://supabase.turklawai.com" }
$SUPA_KEY = $env:SUPABASE_ANON_KEY

if (-not $API_KEY) {
    Write-Host "HATA: OMNISOCIALS_API_KEY bulunamadi." -ForegroundColor Red
    exit 1
}

$VIDEO_SRC   = Join-Path $ROOT "04-araclar\_arsiv-remotion-kaynak\out\geo-seo-45s.mp4"
$CANVA_URL = $env:CANVA_EXPORT_URL  # Canva signed export URL (AKIA dahil credential barindirir) - secrets.env'den yuklenir
$IMAGE_LOCAL = "$env:TEMP\geo_seo_gorsel.png"

$CAPTION_DEFAULT = "SEO yapiyorsun. Peki AI da var misin? Musterilerin artik satin almadan once ChatGPT ye soruyor: Bu sektorde en guvenilir firma hangisi? Ve sen o listede yok musun? Botfusions ile 90 gunde %527 organik trafik artisi yasayan musterimiz gibi -- hem Google da hem ChatGPT de ust siralara cikabilirsin. GEO + SEO = Cift Kanal Gorunurluk. Ucretsiz analiz: botfusions.com/geo-hizmet #GEO #SEO #AIMarketing #Botfusions #ChatGPT"

$CAPTION_X = "SEO yapiyorsun. Peki AI da var misin? ChatGPT seni onermiyor olabilir. GEO ile hem Google hem AI gorunurlugunu kazan. 90 gunde %527 trafik artisi gercek. botfusions.com/geo-hizmet #GEO #AIMarketing"

$CAPTION_PINTEREST = "GEO Nedir? Generative Engine Optimization ile ChatGPT ve Yapay Zeka Motorlarinda Gorunun. SEO + GEO = Cift Kanal Strateji. 90 gunde %527 organik trafik artisi. Botfusions ile AI gorunurluk analizi alin. botfusions.com/geo-hizmet"

$YOUTUBE_TITLE = "SEO Yapiyorsun Ama AI da Yok Musun? GEO ile Cift Kanal Gorunurluk | Botfusions"

function Save-ToSupabase {
    param($PostId, $Caption, $Platforms, $PostType)
    if (-not $SUPA_KEY) { return }
    $body = "$env:TEMP\supa_log.json"
    $platformsJson = ($Platforms | ForEach-Object { "`"$_`"" }) -join ","
    [System.IO.File]::WriteAllText($body, "{`"omnisocials_post_id`":`"$PostId`",`"caption`":`"geo-seo-video`",`"platforms`":[$platformsJson],`"post_type`":`"$PostType`",`"status`":`"posting`",`"campaign`":`"GEO-SEO-$(Get-Date -Format 'yyyy-MM-dd')`",`"published_at`":`"$(Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ')`"}")
    curl.exe --ssl-no-revoke -s -X POST "$SUPA_URL/rest/v1/social_posts" -H "Authorization: Bearer $SUPA_KEY" -H "apikey: $SUPA_KEY" -H "Content-Type: application/json" -H "Prefer: return=minimal" --data-binary "@$body" | Out-Null
    Remove-Item $body -Force -ErrorAction SilentlyContinue
    Write-Host "  Supabase: OK" -ForegroundColor DarkGray
}

# =====================================================
# CAGRI A — VIDEO REEL
# =====================================================
Write-Host ""
Write-Host "=== CAGRI A: VIDEO REEL ===" -ForegroundColor Magenta

if (-not (Test-Path $VIDEO_SRC)) {
    Write-Host "HATA: Video bulunamadi: $VIDEO_SRC" -ForegroundColor Red
    Write-Host "Once render yapin: cd '04-araclar\_arsiv-remotion-kaynak' ve npm run build:geoseo" -ForegroundColor Yellow
    exit 1
}

Write-Host "[1/5] Video yukleniyor..." -ForegroundColor Cyan
$VIDEO_TEMP = "$env:TEMP\geo_seo_video.mp4"
Copy-Item -LiteralPath $VIDEO_SRC -Destination $VIDEO_TEMP -Force

$videoUpload = curl.exe --ssl-no-revoke -s -X POST "https://api.omnisocials.com/v1/media/upload" -H "Authorization: Bearer $API_KEY" -F "file=@`"$VIDEO_TEMP`";type=video/mp4"
Write-Host "Yanit: $videoUpload"
$VIDEO_MEDIA_ID = ($videoUpload | ConvertFrom-Json).data.id

if (-not $VIDEO_MEDIA_ID) {
    Write-Host "HATA: Video Media ID alinamadi!" -ForegroundColor Red
    exit 1
}
Write-Host "Video Media ID: $VIDEO_MEDIA_ID" -ForegroundColor Green
Remove-Item $VIDEO_TEMP -Force

Write-Host "[2/5] Reel yayinlaniyor (IG + FB + YT + TikTok)..." -ForegroundColor Cyan
$reelFile = "$env:TEMP\geo_seo_reel.json"
[System.IO.File]::WriteAllText($reelFile, "{`"content`":{`"default`":`"$CAPTION_DEFAULT`",`"youtube`":`"$CAPTION_DEFAULT`"},`"accounts`":[`"881407_instagram`",`"881407_facebook`",`"881407_youtube`",`"881407_tiktok`"],`"media_ids`":[`"$VIDEO_MEDIA_ID`"],`"type`":`"reel`",`"youtube`":{`"title`":`"$YOUTUBE_TITLE`",`"privacy_status`":`"public`"},`"tiktok`":{`"privacy_level`":`"PUBLIC_TO_EVERYONE`"}}")

$reelResult = curl.exe --ssl-no-revoke -s -X POST "https://api.omnisocials.com/v1/posts/create-and-publish" -H "Authorization: Bearer $API_KEY" -H "Content-Type: application/json" --data-binary "@$reelFile"
Write-Host "Reel sonucu: $reelResult" -ForegroundColor Green
Remove-Item $reelFile -Force
$reelPostId = ($reelResult | ConvertFrom-Json).data.id
Save-ToSupabase -PostId $reelPostId -Caption $CAPTION_DEFAULT -Platforms @("instagram","facebook","youtube","tiktok") -PostType "reel"

# =====================================================
# CAGRI B — GORSEL POST (X + IG + FB)
# =====================================================
Write-Host ""
Write-Host "=== CAGRI B: GORSEL POST ===" -ForegroundColor Magenta

Write-Host "[3/5] Canva gorseli indiriliyor..." -ForegroundColor Cyan
curl.exe --ssl-no-revoke -s -L -o "$IMAGE_LOCAL" "$CANVA_URL"
if (-not (Test-Path $IMAGE_LOCAL)) {
    Write-Host "HATA: Gorsel indirilemedi!" -ForegroundColor Red
    exit 1
}
Write-Host "Gorsel indirildi: $IMAGE_LOCAL" -ForegroundColor Green

Write-Host "[4/5] Gorsel yukleniyor..." -ForegroundColor Cyan
$imgUpload = curl.exe --ssl-no-revoke -s -X POST "https://api.omnisocials.com/v1/media/upload" -H "Authorization: Bearer $API_KEY" -F "file=@`"$IMAGE_LOCAL`";type=image/png"
Write-Host "Yanit: $imgUpload"
$IMG_MEDIA_ID = ($imgUpload | ConvertFrom-Json).data.id

if (-not $IMG_MEDIA_ID) {
    Write-Host "HATA: Gorsel Media ID alinamadi!" -ForegroundColor Red
    exit 1
}
Write-Host "Gorsel Media ID: $IMG_MEDIA_ID" -ForegroundColor Green

$postFile = "$env:TEMP\geo_seo_post.json"
[System.IO.File]::WriteAllText($postFile, "{`"content`":{`"default`":`"$CAPTION_DEFAULT`",`"x`":`"$CAPTION_X`"},`"accounts`":[`"881407_x`",`"881407_instagram`",`"881407_facebook`"],`"media_ids`":[`"$IMG_MEDIA_ID`"],`"type`":`"post`"}")

$postResult = curl.exe --ssl-no-revoke -s -X POST "https://api.omnisocials.com/v1/posts/create-and-publish" -H "Authorization: Bearer $API_KEY" -H "Content-Type: application/json" --data-binary "@$postFile"
Write-Host "Post sonucu: $postResult" -ForegroundColor Green
Remove-Item $postFile -Force
$postId = ($postResult | ConvertFrom-Json).data.id
Save-ToSupabase -PostId $postId -Caption $CAPTION_DEFAULT -Platforms @("instagram","facebook","x") -PostType "post"

# =====================================================
# CAGRI C — PINTEREST (ayri cagri)
# =====================================================
Write-Host ""
Write-Host "=== CAGRI C: PINTEREST ===" -ForegroundColor Magenta
Write-Host "[5/5] Pinterest yayinlaniyor..." -ForegroundColor Cyan

$pinFile = "$env:TEMP\geo_seo_pinterest.json"
[System.IO.File]::WriteAllText($pinFile, "{`"content`":{`"default`":`"$CAPTION_PINTEREST`"},`"accounts`":[`"881407_pinterest`"],`"media_ids`":[`"$IMG_MEDIA_ID`"],`"type`":`"post`",`"pinterest_board_id`":`"1091067515915706441`"}")

$pinResult = curl.exe --ssl-no-revoke -s -X POST "https://api.omnisocials.com/v1/posts/create-and-publish" -H "Authorization: Bearer $API_KEY" -H "Content-Type: application/json" --data-binary "@$pinFile"
Write-Host "Pinterest sonucu: $pinResult" -ForegroundColor Green
Remove-Item $pinFile -Force
Remove-Item $IMAGE_LOCAL -Force -ErrorAction SilentlyContinue
$pinId = ($pinResult | ConvertFrom-Json).data.id
Save-ToSupabase -PostId $pinId -Caption $CAPTION_PINTEREST -Platforms @("pinterest") -PostType "post"

Write-Host ""
Write-Host "=== TUM YAYINLAR TAMAMLANDI ===" -ForegroundColor Green
Write-Host "A: Video  -> Instagram + Facebook + YouTube + TikTok (Reel)"
Write-Host "B: Gorsel -> X + Instagram + Facebook (Post)"
Write-Host "C: Gorsel -> Pinterest / AI-Botfusions-GEO board"
