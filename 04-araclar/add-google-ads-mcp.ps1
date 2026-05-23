# Google Ads MCP - Claude Desktop Config Güncelleyici
# Botfusions - cenk@botfusions.com
# Çalıştır: PowerShell olarak sağ tıkla > Run with PowerShell

$configPath = "$env:APPDATA\Claude\claude_desktop_config.json"
$token = "ZW1haWwtbG9naW46UlVkR1F4a2VBbjhIUjFVdEUxSmZWenBIUHlZemNpSXpQakVmT2lBUVpsa2tYR2tWT0FrQVBWVjJSVE1xSEIwYU9tTkhLenMxTVZzOU9Gb0VVeHdpY0ZGcUNpMC9Td0lqRkZnNU9RdDFERWN4QXhZZ0lVcERHVEkzRkIwdUpSNGNWbEpCQ0JjVEFnPT0="

Write-Host "Google Ads MCP kurulumu basliyor..." -ForegroundColor Cyan

# Config dosyasını kontrol et
if (-not (Test-Path $configPath)) {
    Write-Host "Config dosyasi bulunamadi: $configPath" -ForegroundColor Red
    Write-Host "Claude Desktop yuklu mu? Kontrol edin." -ForegroundColor Yellow
    pause
    exit
}

# Mevcut config'i oku
$configContent = Get-Content $configPath -Raw -Encoding UTF8
$config = $configContent | ConvertFrom-Json

# mcpServers yoksa oluştur
if (-not $config.mcpServers) {
    $config | Add-Member -MemberType NoteProperty -Name "mcpServers" -Value ([PSCustomObject]@{})
}

# Google Ads MCP ekle
$gadsConfig = [PSCustomObject]@{
    command = "npx"
    args = @("-y", "@trueclicks/google-ads-mcp-js", "--token=$token")
}

$config.mcpServers | Add-Member -MemberType NoteProperty -Name "gads" -Value $gadsConfig -Force

# Dosyayı kaydet
$config | ConvertTo-Json -Depth 10 | Set-Content $configPath -Encoding UTF8

Write-Host ""
Write-Host "BASARILI! Google Ads MCP eklendi." -ForegroundColor Green
Write-Host "Musteri ID: 3646875139 (Botfusions)" -ForegroundColor White
Write-Host ""
Write-Host "Simdi CLAUDE DESKTOP'I YENIDEN BASLATIN" -ForegroundColor Yellow
Write-Host "(Completely quit and reopen)" -ForegroundColor Yellow
Write-Host ""

# Doğrulama
$verifyContent = Get-Content $configPath -Raw | ConvertFrom-Json
if ($verifyContent.mcpServers.gads) {
    Write-Host "Dogrulama: gads MCP config'de mevcut." -ForegroundColor Green
} else {
    Write-Host "UYARI: Dogrulama basarisiz, config'i manuel kontrol edin." -ForegroundColor Red
}

pause
