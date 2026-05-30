# Botfusions -- GEO vs SEO Video + Infografik Yayini
# 2026-05-31

param()
$ErrorActionPreference = "Stop"

$BASE = $PSScriptRoot

# API Key
$envContent = Get-Content "$BASE\secrets.env"
$OMNI_KEY = ($envContent | Where-Object { $_ -match "^OMNISOCIALS_API_KEY=" }) -replace "OMNISOCIALS_API_KEY=",""

# Dosya yollari
$VIDEO_SRC = "$BASE\04-araclar\hyperframes\geo-seo-45s\renders\geo-seo-45s_2026-05-30_02-31-53.mp4"
$IMG_1X1   = "$BASE\02-gorseller\geo-gorseller\geo-seo-infografik-1x1.png"
$IMG_2X3   = "$BASE\02-gorseller\geo-gorseller\geo-seo-infografik-2x3.png"

$API_BASE = "https://api.omnisocials.com"

Write-Host "========================================"
Write-Host "BOTFUSIONS -- GEO vs SEO YAYIN"
Write-Host "========================================"

# ── ADIM 1: Video yukle ────────────────────────────────────────────────────────
Write-Host "[1/5] Video yukleniyor..."
$vtmp = "$env:TEMP\bf_geo_video.mp4"
Copy-Item -LiteralPath $VIDEO_SRC -Destination $vtmp -Force

$vUp = curl.exe --ssl-no-revoke -s `
    -X POST "$API_BASE/v1/media/upload" `
    -H "Authorization: Bearer $OMNI_KEY" `
    -F "file=@`"$vtmp`";type=video/mp4" | ConvertFrom-Json

Remove-Item $vtmp -Force -ErrorAction SilentlyContinue
$VIDEO_ID = $vUp.data.id
if (-not $VIDEO_ID) { Write-Host "HATA: Video upload"; Write-Host ($vUp | ConvertTo-Json); exit 1 }
Write-Host "   Video ID: $VIDEO_ID"

# ── ADIM 2: Reel yayinla ──────────────────────────────────────────────────────
Write-Host "[2/5] Reel yayinlaniyor (IG+FB+YT+TikTok)..."

$ytTitle = "SEO vs GEO Farki Ne? Rakibin ChatGPT'de Cikiyor, Sen Cikmiyor Musun? | Botfusions"
$captionDefault = "SEO yapiyorsun ama ChatGPT'de cikmiyorsun. Rakibin cikiyor.`n`nBuyuk fark:`n- SEO: Google icin optimize edersin`n- GEO: ChatGPT, Claude, Gemini icin optimize edersin`n`nSatinalma kararlarinin %67'si AI aramalarindan basliyor.`n`n90 gunde %527 organik trafik artisi gordugumuz musteri vakamiz var.`n`nUcretsiz GEO + SEO analizi icin bio linkine tikla.`n`n#GEO #SEO #YapayZeka #AIMarketing #Botfusions"

$reelJson = [ordered]@{
    content    = [ordered]@{
        default = $captionDefault
        youtube = $captionDefault
    }
    accounts   = @("881407_instagram","881407_facebook","881407_youtube","881407_tiktok")
    media_ids  = @($VIDEO_ID)
    type       = "reel"
    youtube    = [ordered]@{
        title          = $ytTitle
        privacy_status = "public"
    }
    tiktok     = [ordered]@{ privacy_level = "PUBLIC_TO_EVERYONE" }
}
$reelFile = "$env:TEMP\bf_reel.json"
$reelJson | ConvertTo-Json -Depth 5 | Out-File $reelFile -Encoding utf8

$reelResult = curl.exe --ssl-no-revoke -s `
    -X POST "$API_BASE/v1/posts/create-and-publish" `
    -H "Authorization: Bearer $OMNI_KEY" `
    -H "Content-Type: application/json" `
    --data-binary "@$reelFile" | ConvertFrom-Json

Remove-Item $reelFile -Force -ErrorAction SilentlyContinue
Write-Host "   Reel sonucu: $($reelResult | ConvertTo-Json -Compress)"

# ── ADIM 3: 1:1 gorsel yukle ──────────────────────────────────────────────────
Write-Host "[3/5] 1:1 infografik yukleniyor..."
$itmp = "$env:TEMP\bf_1x1.png"
Copy-Item -LiteralPath $IMG_1X1 -Destination $itmp -Force

$iUp = curl.exe --ssl-no-revoke -s `
    -X POST "$API_BASE/v1/media/upload" `
    -H "Authorization: Bearer $OMNI_KEY" `
    -F "file=@`"$itmp`";type=image/png" | ConvertFrom-Json

Remove-Item $itmp -Force -ErrorAction SilentlyContinue
$IMG_ID = $iUp.data.id
Write-Host "   Gorsel ID: $IMG_ID"

# ── ADIM 4: Post yayinla (IG+FB+X) ───────────────────────────────────────────
Write-Host "[4/5] Post yayinlaniyor (IG+FB+X)..."

$captionX = "SEO yapiyorsun ama ChatGPT'de cikiyor musun?`n`nRakibin cikiyor.`n`nGEO = Generative Engine Optimization`nChatGPT + Claude + Gemini icin optimize et.`n`n90 gunde %527 organik artis.`n`nbotfusions.com/geo-hizmet"

$postJson = [ordered]@{
    content   = [ordered]@{
        default = $captionDefault
        x       = $captionX
    }
    accounts  = @("881407_instagram","881407_facebook","881407_x")
    media_ids = @($IMG_ID)
    type      = "post"
}
$postFile = "$env:TEMP\bf_post.json"
$postJson | ConvertTo-Json -Depth 5 | Out-File $postFile -Encoding utf8

$postResult = curl.exe --ssl-no-revoke -s `
    -X POST "$API_BASE/v1/posts/create-and-publish" `
    -H "Authorization: Bearer $OMNI_KEY" `
    -H "Content-Type: application/json" `
    --data-binary "@$postFile" | ConvertFrom-Json

Remove-Item $postFile -Force -ErrorAction SilentlyContinue
Write-Host "   Post sonucu: $($postResult | ConvertTo-Json -Compress)"

# ── ADIM 5: Pinterest ─────────────────────────────────────────────────────────
Write-Host "[5/5] Pinterest yayini..."
$ptmp = "$env:TEMP\bf_2x3.png"
Copy-Item -LiteralPath $IMG_2X3 -Destination $ptmp -Force

$pUp = curl.exe --ssl-no-revoke -s `
    -X POST "$API_BASE/v1/media/upload" `
    -H "Authorization: Bearer $OMNI_KEY" `
    -F "file=@`"$ptmp`";type=image/png" | ConvertFrom-Json

Remove-Item $ptmp -Force -ErrorAction SilentlyContinue
$PIN_ID = $pUp.data.id

$captionPin = "SEO vs GEO Farki | Botfusions 2025 Rehberi`n`nSEO: Google, Bing arama motorlari icin optimizasyon.`nGEO: ChatGPT, Claude, Gemini, Perplexity AI motorlari icin gorunurluk.`n`n2025'te satinalma kararlarinin %67'si AI aramalarindan basliyor.`n`nBotfusions: 90 gunde %527 organik trafik artisi kaniti olan Turkiye'nin onde gelen GEO ajansi.`n`nUcretsiz analiz: botfusions.com/geo-hizmet`n`n#GEO #SEO #AIMarketing #YapayZekaSEO #Botfusions #ChatGPTSEO"

$pinJson = [ordered]@{
    content           = [ordered]@{ default = $captionPin }
    accounts          = @("881407_pinterest")
    media_ids         = @($PIN_ID)
    type              = "post"
    pinterest_board_id = "1091067515915706441"
}
$pinFile = "$env:TEMP\bf_pin.json"
$pinJson | ConvertTo-Json -Depth 5 | Out-File $pinFile -Encoding utf8

$pinResult = curl.exe --ssl-no-revoke -s `
    -X POST "$API_BASE/v1/posts/create-and-publish" `
    -H "Authorization: Bearer $OMNI_KEY" `
    -H "Content-Type: application/json" `
    --data-binary "@$pinFile" | ConvertFrom-Json

Remove-Item $pinFile -Force -ErrorAction SilentlyContinue
Write-Host "   Pinterest sonucu: $($pinResult | ConvertTo-Json -Compress)"

Write-Host ""
Write-Host "========================================"
Write-Host "YAYIN TAMAMLANDI"
Write-Host "========================================"
