"""
GSC OAuth2 Refresh Token Üretici
==================================
Mevcut Google Cloud client_id ve client_secret ile
Google Search Console için refresh token alır.

Kullanım:
    python get_gsc_token.py

Adımlar:
    1. Script çalışır, terminalde bir URL gösterir
    2. URL'yi tarayıcıda aç
    3. Google hesabınla giriş yap ve izin ver
    4. Sayfadaki kodu buraya yapıştır
    5. Refresh token .env dosyasına otomatik yazılır
"""

import os
import webbrowser
from pathlib import Path

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    print("Bağımlılık eksik. Yükleniyor...")
    os.system("pip install google-auth-oauthlib --break-system-packages -q")
    from google_auth_oauthlib.flow import InstalledAppFlow

# OAuth bilgileri — secrets.env'den okunur
CLIENT_ID     = os.getenv("GOOGLE_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")

if not CLIENT_ID or not CLIENT_SECRET:
    print("HATA: GOOGLE_CLIENT_ID ve GOOGLE_CLIENT_SECRET secrets.env'de bulunamadi.")
    exit(1)

# GSC için gereken scope
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

CLIENT_CONFIG = {
    "installed": {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
}

def main():
    print("\n" + "="*55)
    print("GSC OAuth2 Refresh Token Üretici")
    print("="*55)
    print("\nGoogle Cloud Console'da Search Console API aktif")
    print("Client ID mevcut — şimdi token alınıyor...\n")

    flow = InstalledAppFlow.from_client_config(CLIENT_CONFIG, scopes=SCOPES)

    # Önce local server dene, olmazsa manuel kod ile devam et
    try:
        creds = flow.run_local_server(port=8085, open_browser=True)
        print("\n✅ Otomatik olarak alındı!")
    except Exception:
        # Tarayıcı açılamazsa URL'yi göster
        auth_url, _ = flow.authorization_url(prompt="consent")
        print("Tarayıcı açılamadı. Aşağıdaki URL'yi kopyalayıp tarayıcında aç:\n")
        print(f"  {auth_url}\n")
        code = input("Sayfadaki kodu buraya yapıştır: ").strip()
        flow.fetch_token(code=code)
        creds = flow.credentials

    refresh_token = creds.refresh_token
    print(f"\n🔑 Refresh Token:\n   {refresh_token}")

    # .env dosyasını güncelle
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        content = env_path.read_text(encoding="utf-8")
        if "GSC_REFRESH_TOKEN" in content:
            lines = content.splitlines()
            new_lines = []
            for line in lines:
                if line.startswith("GSC_REFRESH_TOKEN"):
                    new_lines.append(f"GSC_REFRESH_TOKEN={refresh_token}")
                else:
                    new_lines.append(line)
            env_path.write_text("\n".join(new_lines), encoding="utf-8")
        else:
            with open(env_path, "a") as f:
                f.write(f"\nGSC_REFRESH_TOKEN={refresh_token}\n")
        print(f"\n✅ .env dosyasına yazıldı: {env_path}")
    else:
        print(f"\n⚠️  .env bulunamadı. Token'ı manuel ekle:")
        print(f"   GSC_REFRESH_TOKEN={refresh_token}")

    print("\n🎉 Kurulum tamamlandı! Artık pipeline çalıştırabilirsin:")
    print("   python agent.py --client botfusions --days 30")
    print("="*55 + "\n")


if __name__ == "__main__":
    main()
