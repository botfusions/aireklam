@echo off
title Botfusions CMO Dashboard
color 0B
echo.
echo  ╔══════════════════════════════════════════════════╗
echo  ║   Botfusions AI CMO Dashboard - Başlatılıyor    ║
echo  ╚══════════════════════════════════════════════════╝
echo.
echo  [1/2] GSC API Sunucusu başlatılıyor...
echo.

cd /d "%~dp0"

REM Flask bağımlılıklarını yükle (ilk çalıştırmada)
pip install flask python-dotenv google-api-python-client google-auth google-auth-httplib2 --quiet --break-system-packages 2>nul

REM GSC API sunucusunu arka planda başlat
start "Botfusions GSC API" /min python gsc_api_server.py

REM 2 saniye bekle sunucu başlasın
timeout /t 2 /nobreak >nul

echo  [2/2] Dashboard açılıyor...
echo.
echo  GSC API : http://localhost:8765/api/health
echo  Dashboard: cmo-dashboard.html
echo.

REM Dashboard'ı varsayılan tarayıcıda aç
start "" "%~dp0cmo-dashboard.html"

echo  ✓ CMO Dashboard aktif!
echo  ✓ GSC API arka planda çalışıyor
echo.
echo  Kapatmak için bu pencereyi kapatın ve
echo  Görev Yöneticisi'nden "Botfusions GSC API" penceresini sonlandırın.
echo.
pause
