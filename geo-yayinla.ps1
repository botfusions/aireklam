# GEO Infografik Yayin - Terminale paste edilebilir versiyon

$API_KEY = $env:OMNISOCIALS_API_KEY
if (-not $API_KEY) {
    Write-Host "HATA: OMNISOCIALS_API_KEY ortam degiskeni bulunamadi." -ForegroundColor Red
    Write-Host "Cozum: secrets.env dosyasini olusturun veya asagidaki komutu calistirin:"
    Write-Host '  $env:OMNISOCIALS_API_KEY = "omsk_live_xxxxx"'
    exit 1
}

# Turkce karakter sorunu: path'i hardcode etme, wildcard ile bul
if ($PSScriptRoot) {
    $ROOT = $PSScriptRoot
} else {
    $ROOT = (Get-Item "C:\Users\user\Downloads\Z.ai_claude code\AI *Ajans*").FullName
}
Write-Host "ROOT: $ROOT"

$IMAGE_SRC = Join-Path $ROOT "02-gorseller\geo-gorseller\geo-infografik-kare-feed.png"
Write-Host "Gorsel: $IMAGE_SRC"

if (-not (Test-Path -LiteralPath $IMAGE_SRC)) {
    Write-Host "HATA: Gorsel bulunamadi!" -ForegroundColor Red
    Write-Host "Klasordeki dosyalar:" -ForegroundColor Yellow
    Get-ChildItem (Join-Path $ROOT "02-gorseller\geo-gorseller") -ErrorAction SilentlyContinue
    exit
}
Write-Host "Gorsel OK" -ForegroundColor Green

# Temp kopyala
$T = "$env:TEMP\geo_1x1.png"
Copy-Item -LiteralPath $IMAGE_SRC -Destination $T -Force
Write-Host "Temp: $T ($([math]::Round((Get-Item $T).Length/1KB)) KB)"

# ADIM 1: Upload
Write-Host "Uploading..." -ForegroundColor Cyan
$up = curl.exe --ssl-no-revoke -s -S -X POST "https://api.omnisocials.com/v1/media/upload" -H "Authorization: Bearer $API_KEY" -F "file=@`"$T`";type=image/png"
Write-Host "Upload yaniti: $up"
Remove-Item $T -Force

$mid = ($up | ConvertFrom-Json).data.id
if (-not $mid) { Write-Host "HATA: media_id alinamadi" -ForegroundColor Red; exit }
Write-Host "Media ID: $mid" -ForegroundColor Green

# ADIM 2: Post (IG + FB + TikTok + X)
Write-Host "Post yayinlaniyor..." -ForegroundColor Cyan
$pf = "$env:TEMP\gp.json"
[System.IO.File]::WriteAllText($pf, "{`"content`":{`"default`":`"Musteri ChatGPT'ye soruyor. Rakibin cikiyor. Sen cikmiyorsun. Satin alma kararlarinin %67'si artik AI arastirmasiyla basliyor. GEO ile ChatGPT, Claude ve Gemini'de gorunur ol. 90 gunde %527 organik trafik artisi sagladik. Ucretsiz analiz: botfusions.com/geo-hizmet #GEO #ChatGPT #AI #dijitalpazarlama #Botfusions`",`"x`":`"ChatGPT'ye soruluyor. Rakibin cikiyor. Sen cikmiyorsun. GEO ile AI aramalarda gorun - %527 trafik artisi 90 gunde - botfusions.com/geo-hizmet #GEO #AI #Botfusions`"},`"accounts`":[`"881407_instagram`",`"881407_facebook`",`"881407_tiktok`",`"881407_x`"],`"media_ids`":[`"$mid`"],`"type`":`"post`"}")
$pr = curl.exe --ssl-no-revoke -s -S -X POST "https://api.omnisocials.com/v1/posts/create-and-publish" -H "Authorization: Bearer $API_KEY" -H "Content-Type: application/json" --data-binary "@$pf"
Write-Host "Post sonucu: $pr" -ForegroundColor Green
Remove-Item $pf -Force

# ADIM 3: Pinterest
Write-Host "Pinterest yayinlaniyor..." -ForegroundColor Cyan
$pinf = "$env:TEMP\gpin.json"
[System.IO.File]::WriteAllText($pinf, "{`"content`":{`"default`":`"GEO ile ChatGPT, Claude ve Gemini'de gorunur ol. %67 satin alma karari AI arastirmasiyla basliyor. 90 gunde %527 organik trafik artisi. botfusions.com/geo-hizmet #GEO #AI #ChatGPT #Botfusions`"},`"accounts`":[`"881407_pinterest`"],`"media_ids`":[`"$mid`"],`"type`":`"post`",`"pinterest_board_id`":`"1091067515915706441`"}")
$pinr = curl.exe --ssl-no-revoke -s -S -X POST "https://api.omnisocials.com/v1/posts/create-and-publish" -H "Authorization: Bearer $API_KEY" -H "Content-Type: application/json" --data-binary "@$pinf"
Write-Host "Pinterest sonucu: $pinr" -ForegroundColor Green
Remove-Item $pinf -Force

Write-Host ""
Write-Host "TAMAMLANDI: IG + FB + TikTok + X + Pinterest" -ForegroundColor Green
