"""
GA4 OAuth Refresh Token Alıcı
Bir kerelik çalıştır — cenk@botfusions.com ile authorize et
Token'ı .env dosyasına kaydeder
"""
import os
import json
import urllib.parse
import http.server
import threading
from pathlib import Path

ROOT = Path(__file__).parent

# secrets.env'den OAuth client credentials oku
try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / "secrets.env")
except ImportError:
    pass

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")

if not CLIENT_ID or not CLIENT_SECRET:
    print("HATA: GOOGLE_CLIENT_ID ve GOOGLE_CLIENT_SECRET secrets.env'de bulunamadi.")
    print("Cozum: secrets.env dosyasini olusturun (.env.template referans alin)")
    exit(1)
REDIRECT_URI = "http://localhost:8090"
SCOPES = "https://www.googleapis.com/auth/analytics.readonly"

# Step 1: Auth URL
auth_url = (
    f"https://accounts.google.com/o/oauth2/v2/auth?"
    f"client_id={CLIENT_ID}&"
    f"redirect_uri={urllib.parse.quote(REDIRECT_URI)}&"
    f"response_type=code&"
    f"scope={urllib.parse.quote(SCOPES)}&"
    f"access_type=offline&"
    f"prompt=consent"
)

print("=" * 55)
print("  GA4 OAUTH REFRESH TOKEN ALICI")
print("=" * 55)
print(f"\n1. Bu URL'yi tarayıcıda açın:\n")
print(f"  {auth_url}\n")
print("2. cenk@botfusions.com hesabıyla giriş yapın")
print("3. 'Allow' deyin")
print("4. Yönlendirilen URL'deki 'code' parametresini kopyalayın")
print()

code = input("Authorization code'u yapıştırın: ").strip()

# Step 2: Token exchange
import requests
r = requests.post("https://oauth2.googleapis.com/token", data={
    "code": code,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "grant_type": "authorization_code",
})

if r.status_code != 200:
    print(f"HATA: {r.status_code} — {r.text}")
    exit(1)

token_data = r.json()
refresh_token = token_data.get("refresh_token")

if not refresh_token:
    print("HATA: refresh_token alınamadı. Token response:")
    print(json.dumps(token_data, indent=2))
    exit(1)

print(f"\n✅ Refresh Token alındı: {refresh_token[:30]}...")

# .env'e kaydet
env_path = "05-gsc-nocodb/.env"
with open(env_path, "r", encoding="utf-8") as f:
    content = f.read()

if "GA4_REFRESH_TOKEN=" in content:
    # Mevcut satırı güncelle
    lines = content.split("\n")
    new_lines = []
    for line in lines:
        if line.startswith("GA4_REFRESH_TOKEN="):
            new_lines.append(f"GA4_REFRESH_TOKEN={refresh_token}")
        else:
            new_lines.append(line)
    content = "\n".join(new_lines)
else:
    content += f"\nGA4_REFRESH_TOKEN={refresh_token}\n"

with open(env_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\n✅ {env_path} dosyasına kaydedildi")
print("Şimdi gsc_api_server.py'yi yeniden başlatın — GA4 çalışacak!")
