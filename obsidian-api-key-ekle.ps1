# Obsidian API Key — Claude Desktop Config Güncelleyici
# Çalıştır: Sağ tık → PowerShell ile çalıştır

$configPath = "$env:APPDATA\Claude\claude_desktop_config.json"
$apiKey = "f534907dd9fa04179f59cbd41ecf26779f77b7e6e0e8949c90e5abc1ce9ccea7"

Write-Host "Config dosyası okunuyor: $configPath" -ForegroundColor Cyan

if (-not (Test-Path $configPath)) {
    Write-Host "HATA: Config dosyası bulunamadı!" -ForegroundColor Red
    exit
}

# Yedek al
$backup = $configPath + ".backup_" + (Get-Date -Format "yyyyMMdd_HHmmss")
Copy-Item $configPath $backup
Write-Host "Yedek alındı: $backup" -ForegroundColor Green

# JSON oku
$config = Get-Content $configPath -Raw | ConvertFrom-Json

# mcpServers içinde obsidian entry'yi bul
$obsidianKey = $null
foreach ($key in $config.mcpServers.PSObject.Properties.Name) {
    if ($key -like "*obsidian*") {
        $obsidianKey = $key
        break
    }
}

if ($null -eq $obsidianKey) {
    Write-Host "HATA: Config'de obsidian MCP bulunamadı!" -ForegroundColor Red
    Write-Host "Mevcut MCP'ler:" -ForegroundColor Yellow
    $config.mcpServers.PSObject.Properties.Name | ForEach-Object { Write-Host "  - $_" }
    exit
}

Write-Host "Obsidian MCP bulundu: $obsidianKey" -ForegroundColor Green

# env objesi yoksa oluştur
if (-not $config.mcpServers.$obsidianKey.env) {
    $config.mcpServers.$obsidianKey | Add-Member -NotePropertyName "env" -NotePropertyValue ([PSCustomObject]@{})
}

# API key ekle (hangi env variable adını kullanıyorsa)
$envObj = $config.mcpServers.$obsidianKey.env

# OBSIDIAN_API_KEY dene
if ($envObj.PSObject.Properties.Name -contains "OBSIDIAN_API_KEY") {
    $envObj.OBSIDIAN_API_KEY = $apiKey
} else {
    $envObj | Add-Member -NotePropertyName "OBSIDIAN_API_KEY" -NotePropertyValue $apiKey -Force
}

# Kaydet
$config | ConvertTo-Json -Depth 20 | Set-Content $configPath -Encoding UTF8
Write-Host "API key eklendi!" -ForegroundColor Green
Write-Host ""
Write-Host "Simdi Claude Desktop'i tamamen kapat ve yeniden ac." -ForegroundColor Yellow
Write-Host "Sonra tekrar dene - Obsidian baglanacak." -ForegroundColor Yellow
Read-Host "Devam etmek icin Enter'a bas"
