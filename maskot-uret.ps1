# Botfusions Maskot Üretici — WaveSpeed API (openai/gpt-image-2)
# Çalıştır: sağ tık → "PowerShell ile çalıştır"

$API_KEY    = "755272d9e7c821ecc8bbbc9c8588f89d0dd45b747af68c9fc30d4452e709840a"
$MODEL      = "openai/gpt-image-2/text-to-image"
$ENDPOINT   = "https://api.wavespeed.ai/api/v2/$MODEL"
$OUTPUT_DIR = "$PSScriptRoot\02-gorseller\maskotlar"

$BASE_PROMPT = "3D rendered cute robot mascot character, Botfusions brand identity, round smooth body, big expressive circular eyes, primary color vibrant purple #A855F7 body panels, accent color bright orange #F97316 glowing joints eye rings chest badge fingertip lights, small white B letter on chest badge, dark purple #7C3AED shadow areas and depth shading, ultra-clean photorealistic 3D render, studio lighting, pure white background, Pixar-quality character design, professional product mascot, no text no watermark, 1:1 square format"

$POSES = @(
    @{ name = "C1-selamlama"; pose = "greeting pose, one hand raised waving hello, friendly smile, welcoming gesture" },
    @{ name = "C2-dusunuyor"; pose = "thinking pose, one hand on chin, looking up thoughtfully, curious expression" },
    @{ name = "C3-sunum";     pose = "presenting pose, one arm extended pointing to the right, confident stance" },
    @{ name = "C4-kutluyor";  pose = "celebrating pose, both arms raised in victory, colorful confetti around, joyful expression" },
    @{ name = "C5-ucuyor";    pose = "flying pose, rocket boost with bright orange flames from feet, dynamic upward movement" },
    @{ name = "C6-oturuyor";  pose = "sitting pose, legs crossed, relaxed friendly posture, slight smile" }
)

# Çıktı klasörünü oluştur
if (-not (Test-Path $OUTPUT_DIR)) {
    New-Item -ItemType Directory -Path $OUTPUT_DIR -Force | Out-Null
    Write-Host "📁 Klasör oluşturuldu: $OUTPUT_DIR" -ForegroundColor Cyan
}

Write-Host "`n🤖 Botfusions Maskot Üretici Başlıyor..." -ForegroundColor Magenta
Write-Host "🔧 Model  : $MODEL" -ForegroundColor Cyan
Write-Host "🌐 Endpoint: $ENDPOINT" -ForegroundColor Cyan
Write-Host "📁 Çıktı  : $OUTPUT_DIR`n" -ForegroundColor Cyan

foreach ($item in $POSES) {
    $fullPrompt = "$BASE_PROMPT, $($item.pose)"
    $outFile    = "$OUTPUT_DIR\botfusions-maskot-$($item.name).png"

    Write-Host "⏳ Üretiliyor: $($item.name)..." -ForegroundColor Yellow

    # gpt-image-2 parametreleri (output_format desteklenmiyor, n kullanılmıyor)
    $body = @{
        prompt  = $fullPrompt
        size    = "1024x1024"
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

        Write-Host "   ✔ İstek gönderildi, 60 sn üretim bekleniyor..." -ForegroundColor Gray
        Start-Sleep -Seconds 60

        # --- URL çekme: farklı yanıt yapılarını dene ---
        $imgUrl = $null

        # Tip 1: data.outputs[]
        if ($response.data.outputs -and $response.data.outputs.Count -gt 0) {
            $imgUrl = $response.data.outputs[0]
        }
        # Tip 2: data.images[].url
        elseif ($response.data.images -and $response.data.images.Count -gt 0) {
            $imgUrl = $response.data.images[0].url
        }
        # Tip 3: outputs[]
        elseif ($response.outputs -and $response.outputs.Count -gt 0) {
            $imgUrl = $response.outputs[0]
        }
        # Tip 4: data.url
        elseif ($response.data.url) {
            $imgUrl = $response.data.url
        }
        # Tip 5: url
        elseif ($response.url) {
            $imgUrl = $response.url
        }

        # Yoksa asenkron polling
        if (-not $imgUrl) {
            $predId = if ($response.data.id) { $response.data.id } else { $response.id }
            if ($predId) {
                Write-Host "   🔄 Polling ID: $predId" -ForegroundColor Gray
                $maxWait = 120; $waited = 0
                do {
                    Start-Sleep -Seconds 5; $waited += 5
                    $poll   = Invoke-RestMethod `
                        -Uri "https://api.wavespeed.ai/api/v2/predictions/$predId" `
                        -Headers @{ "Authorization" = "Bearer $API_KEY" } `
                        -TimeoutSec 30
                    $status = if ($poll.data.status) { $poll.data.status } else { $poll.status }
                    Write-Host "   [$waited sn] $status" -ForegroundColor Gray
                } while ($status -notin @("succeeded","completed","failed") -and $waited -lt $maxWait)

                if ($poll.data.outputs)    { $imgUrl = $poll.data.outputs[0] }
                elseif ($poll.data.images) { $imgUrl = $poll.data.images[0].url }
                elseif ($poll.outputs)     { $imgUrl = $poll.outputs[0] }
                elseif ($poll.data.url)    { $imgUrl = $poll.data.url }
            } else {
                Write-Host "   ⚠ Ham yanıt (URL veya ID bulunamadı):" -ForegroundColor DarkYellow
                Write-Host ($response | ConvertTo-Json -Depth 6) -ForegroundColor DarkGray
            }
        }

        if ($imgUrl) {
            Invoke-WebRequest -Uri $imgUrl -OutFile $outFile -TimeoutSec 60
            Write-Host "   ✅ Kaydedildi: botfusions-maskot-$($item.name).png" -ForegroundColor Green
        } else {
            Write-Host "   ❌ Görsel URL bulunamadı." -ForegroundColor Red
        }

    } catch {
        $errBody = $_.ErrorDetails.Message
        Write-Host "   ❌ Hata: $errBody" -ForegroundColor Red
        Write-Host "   Detay: $($_.Exception.Message)" -ForegroundColor DarkRed
    }

    Write-Host "" # boş satır
}


Write-Host "🎉 Tamamlandı! Görseller: $OUTPUT_DIR" -ForegroundColor Green
Write-Host "`nDevam etmek için bir tuşa basın..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
