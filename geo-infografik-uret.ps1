# ============================================================
# Botfusions — GEO İnfografik Üretici (WaveSpeed gpt-image-2)
# Çalıştır: sağ tık → "PowerShell ile çalıştır"
# ============================================================

$API_KEY    = "755272d9e7c821ecc8bbbc9c8588f89d0dd45b747af68c9fc30d4452e709840a"
$MODEL      = "openai/gpt-image-2/text-to-image"
$ENDPOINT   = "https://api.wavespeed.ai/api/v2/$MODEL"
$OUTPUT_DIR = "$PSScriptRoot\02-gorseller\geo-gorseller"

# Çıktı klasörünü oluştur
if (-not (Test-Path $OUTPUT_DIR)) {
    New-Item -ItemType Directory -Path $OUTPUT_DIR -Force | Out-Null
    Write-Host "📁 Klasör oluşturuldu: $OUTPUT_DIR" -ForegroundColor Cyan
}

# ============================================================
# GÖRSELLER — 2 format: kare (feed) + dikey (story/reel)
# ============================================================

$INFOGRAFIKLER = @(
    @{
        name   = "geo-neden-kare-feed"
        size   = "1024x1024"
        format = "Instagram/Facebook Feed (1:1)"
        prompt = @"
Professional dark-themed infographic design about GEO (Generative Engine Optimization) for Turkish AI marketing agency Botfusions. Square 1:1 format.

BACKGROUND: Deep black #0A0A0A with very subtle glowing purple hexagonal grid pattern in background.

TOP AREA: Clean white bold headline text: "Rakibin ChatGPT'de Görünüyor. Sen Görünmüyorsun." — large impactful typography.

MIDDLE SECTION — Side by side comparison cards with rounded dark borders:
LEFT CARD labeled "Rakibin": AI chat interface mockup showing competitor business appearing as bright glowing result with green checkmark ✓, vibrant, neon purple glow around card border.
RIGHT CARD labeled "Sen": Same AI chat interface showing empty dark void, faded gray question mark "?" in center, dim card border, shadowed.

CENTER: Large glowing "GEO" text badge between cards, purple-to-violet gradient #A855F7.

STATS ROW — two glowing metric cards:
LEFT STAT: Huge bold white text "%67" with subtitle text "satın alma kararları AI araştırmasıyla başlıyor"
RIGHT STAT: Huge bold orange text "%527" with subtitle text "90 günde organik trafik artışı"

BOTTOM BAR: Solid orange #F97316 strip with white text "Ücretsiz GEO Analizi → botfusions.com/geo-hizmet"

STYLE: Ultra-modern tech infographic, brand colors purple #A855F7 orange #F97316 white on black, neon glow effects, professional digital marketing, pixel-perfect clean layout.
"@
    },
    @{
        name   = "geo-neden-dikey-story"
        size   = "1024x1792"
        format = "Instagram Story / TikTok (9:16)"
        prompt = @"
Professional dark-themed vertical infographic (9:16 ratio, Instagram Story format) about GEO for Botfusions Turkish AI marketing agency.

BACKGROUND: Pure black #0A0A0A with subtle purple neural network dot pattern, glowing purple edge lighting.

TOP SECTION (branding): Small centered "Botfusions" wordmark in purple #A855F7 with small AI icon. Thin purple divider line.

HOOK SECTION (large):
Line 1 bold white: "Müşteri ChatGPT'ye soruyor."
Line 2 bold orange glow #F97316: "Rakibin çıkıyor."
Line 3 fading gray dim: "Sen çıkmıyorsun."

AI COMPARISON VISUAL:
Two side-by-side AI chat interface bubbles with phone frame:
- Left bubble bright: competitor name glowing green with checkmark ✓ — vibrant, lit
- Right bubble dark: empty void, gray faded "?" — invisible, shadowed

Three STAT CARDS stacked vertically, each full-width with dark card background and glowing border:
Card 1: Large "%67" in white, text "satın alma kararları AI asistan araştırmasıyla başlıyor"
Card 2: Large "%527" in bright orange, text "90 günde organik trafik artışı — gerçek müşteri vakası"
Card 3: "Türkiye'de GEO'yu uygulayan öncü ajanslardan biriyiz" italic white

SOLUTION ROW: Three feature pill badges: "ChatGPT Görünürlük" | "İçerik Optimizasyonu" | "Aylık Rapor" — purple gradient backgrounds.

BOTTOM CTA BUTTON: Full-width orange #F97316 rounded button: "Ücretsiz GEO Analizi Al →" white bold text. Below: "botfusions.com/geo-hizmet" in light gray.

STYLE: Instagram Story / TikTok vertical, bold scroll-stopping layout, Botfusions brand colors, neon glow tech aesthetic, clean professional infographic.
"@
    }
)

# ============================================================
# YARDIMCI FONKSİYON: URL çek
# ============================================================
function Get-ImageUrl($response) {
    if ($response.data.outputs -and $response.data.outputs.Count -gt 0) { return $response.data.outputs[0] }
    if ($response.data.images -and $response.data.images.Count -gt 0)   { return $response.data.images[0].url }
    if ($response.outputs -and $response.outputs.Count -gt 0)           { return $response.outputs[0] }
    if ($response.data.url)  { return $response.data.url }
    if ($response.url)       { return $response.url }
    return $null
}

# ============================================================
# ANA DÖNGÜ
# ============================================================
Write-Host "`n🎨 Botfusions GEO İnfografik Üretici" -ForegroundColor Magenta
Write-Host "═══════════════════════════════════════" -ForegroundColor DarkMagenta
Write-Host "🔧 Model   : $MODEL" -ForegroundColor Cyan
Write-Host "📁 Çıktı   : $OUTPUT_DIR" -ForegroundColor Cyan
Write-Host "🖼  Format  : Feed (1:1) + Story (9:16)`n" -ForegroundColor Cyan

$results = @()

foreach ($item in $INFOGRAFIKLER) {
    Write-Host "⏳ [$($item.format)] Üretiliyor: $($item.name)..." -ForegroundColor Yellow

    $body = @{
        prompt  = $item.prompt
        size    = $item.size
        quality = "low"
    } | ConvertTo-Json -Depth 3

    try {
        $response = Invoke-RestMethod `
            -Uri $ENDPOINT `
            -Method POST `
            -Headers @{
                "Authorization" = "Bearer $API_KEY"
                "Content-Type"  = "application/json"
            } `
            -Body $body `
            -TimeoutSec 120

        Write-Host "   ✔ İstek gönderildi. 60 sn üretim süresi bekleniyor..." -ForegroundColor Gray
        Start-Sleep -Seconds 60

        $imgUrl = Get-ImageUrl $response

        # Asenkron polling gerekirse
        if (-not $imgUrl) {
            $predId = if ($response.data.id) { $response.data.id } else { $response.id }

            if ($predId) {
                Write-Host "   🔄 Polling ID: $predId" -ForegroundColor Gray
                $maxWait = 120; $waited = 0

                do {
                    Start-Sleep -Seconds 10; $waited += 10
                    try {
                        $poll = Invoke-RestMethod `
                            -Uri "https://api.wavespeed.ai/api/v2/predictions/$predId" `
                            -Headers @{ "Authorization" = "Bearer $API_KEY" } `
                            -TimeoutSec 30
                        $status = if ($poll.data.status) { $poll.data.status } else { $poll.status }
                        Write-Host "   [$waited sn] Durum: $status" -ForegroundColor Gray
                        $imgUrl = Get-ImageUrl $poll
                    } catch {
                        Write-Host "   [$waited sn] Polling bekleniyor..." -ForegroundColor DarkGray
                    }
                } while (-not $imgUrl -and $waited -lt $maxWait)
            } else {
                Write-Host "   ⚠ Ham yanıt (ID/URL yok):" -ForegroundColor DarkYellow
                Write-Host ($response | ConvertTo-Json -Depth 5 | Select-String -Pattern "." | Select-Object -First 15) -ForegroundColor DarkGray
            }
        }

        if ($imgUrl) {
            $outFile = "$OUTPUT_DIR\$($item.name).png"
            Invoke-WebRequest -Uri $imgUrl -OutFile $outFile -TimeoutSec 60
            Write-Host "   ✅ Kaydedildi: $($item.name).png`n" -ForegroundColor Green
            $results += "✅ $($item.format): $outFile"
        } else {
            Write-Host "   ❌ Görsel URL alınamadı.`n" -ForegroundColor Red
            $results += "❌ $($item.format): BAŞARISIZ"
        }

    } catch {
        $errBody = $_.ErrorDetails.Message
        Write-Host "   ❌ API Hatası: $errBody" -ForegroundColor Red
        Write-Host "   Detay: $($_.Exception.Message)`n" -ForegroundColor DarkRed
        $results += "❌ $($item.format): HATA — $($_.Exception.Message)"
    }
}

# ============================================================
# ÖZET
# ============================================================
Write-Host "═══════════════════════════════════════" -ForegroundColor DarkMagenta
Write-Host "🎉 TAMAMLANDI — Sonuçlar:" -ForegroundColor Green
foreach ($r in $results) {
    Write-Host "   $r" -ForegroundColor White
}
Write-Host "`n📂 Klasör: $OUTPUT_DIR" -ForegroundColor Cyan
Write-Host "`nBir tuşa basın..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
