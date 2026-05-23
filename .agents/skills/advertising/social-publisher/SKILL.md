# Social Publisher Skill — OmniSocials Entegrasyonu

**Versiyon:** 1.0.0  
**Kategori:** advertising  
**Model:** Haiku 4 (API çağrıları mekanik işlem)  
**Bağımlılık:** OmniSocials API (`API-INTEGRATIONS.md` → Bölüm 9)

---

## Görev

`content-repurposer` skill'i veya başka bir içerik üretim adımından gelen metni ve görselleri alarak **OmniSocials API** üzerinden tek çağrıyla tüm sosyal medya platformlarına yayınlar veya zamanlar.

---

## Tetikleyiciler

Bu skill şu durumlarda çalıştırılır:

- "Şimdi yayınla" / "Tüm platformlara gönder"
- "Zamanla — [tarih/saat]"
- `content-repurposer` sonrası kullanıcı onayı geldiğinde
- Otomatik içerik takvimi akışında

---

## Adım Adım Çalışma

### 1. Girdi Kontrolü

Yayın öncesi şu bilgilerin hazır olduğunu doğrula:

```
☐ Platform bazlı metinler (default + her platform için)
☐ Görsel URL'leri (varsa — canvas-design / HyperFrames çıktısı)
☐ Hedef platformlar (hangi kanallar?)
☐ Zamanlama (hemen mi, zamanlanmış mı?)
☐ Account ID'leri (GET /accounts ile al)
```

### 2. Bağlı Hesapları Listele

```python
import requests

API_KEY = "{{OMNISOCIALS_API_KEY}}"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def get_accounts():
    r = requests.get("https://api.omnisocials.com/v1/accounts", headers=HEADERS)
    return r.json()  # accounts listesi → her birinin 'id' ve 'platform' alanı var
```

### 3. Gönderi Oluştur ve Yayınla

#### Hemen Yayınla
```python
def publish_now(content_dict, account_ids, media_urls=None):
    payload = {
        "content": content_dict,
        "accounts": account_ids
    }
    if media_urls:
        payload["media_urls"] = media_urls
    
    r = requests.post(
        "https://api.omnisocials.com/v1/posts/create-and-publish",
        headers={**HEADERS, "Content-Type": "application/json"},
        json=payload
    )
    return r.json()
```

#### Zamanla
```python
def schedule_post(content_dict, account_ids, scheduled_at, media_urls=None):
    # scheduled_at → ISO 8601 UTC: "2026-05-15T10:00:00Z"
    payload = {
        "content": content_dict,
        "accounts": account_ids,
        "scheduled_at": scheduled_at
    }
    if media_urls:
        payload["media_urls"] = media_urls
    
    r = requests.post(
        "https://api.omnisocials.com/v1/posts/create",
        headers={**HEADERS, "Content-Type": "application/json"},
        json=payload
    )
    return r.json()
```

### 4. Platform Bazlı İçerik Şablonu

`content-repurposer` skill çıktısını bu formata dönüştür:

```python
content = {
    "default": "...",          # Instagram, Facebook, Threads için
    "x": "...",                # Max 280 karakter
    "linkedin": "...",         # Kişisel profil — profesyonel ton
    "linkedin_page": "...",    # Şirket sayfası — kurumsal ton
    "tiktok": "...",           # Max 4000 karakter
    "pinterest": "..."         # Max 500 karakter
}
```

### 5. Medya URL Formatı

```python
# Tüm platformlara aynı görsel
media_urls = ["https://cdn.example.com/gorsel.jpg"]

# Platform bazlı farklı görseller (farklı crop/format)
media_urls = {
    "default": ["https://cdn.example.com/gorsel-16x9.jpg"],   # Facebook
    "instagram": ["https://cdn.example.com/gorsel-1x1.jpg"],  # Kare
    "pinterest": ["https://cdn.example.com/gorsel-2x3.jpg"],  # Uzun
    "x": []  # Twitter'a görsel gönderme
}
```

### 6. Sonuç Kontrolü ve Hata Yönetimi

```python
def handle_result(result):
    status = result.get("status")
    
    if status == "published":
        print("✅ Tüm platformlara başarıyla yayınlandı")
        print("URLs:", result.get("urls", {}))
        
    elif status == "partially_posted":
        print("⚠️ Kısmi başarı:")
        print("  Başarılı:", result.get("posted_platforms"))
        print("  Başarısız:", result.get("failed_platforms"))
        # Başarısızları retry et:
        # POST /posts/:id/retry-failed-platforms
        
    elif status == "scheduled":
        print("🕐 Zamanlandı:", result.get("scheduled_at"))
        
    else:
        print("❌ Hata:", result)
```

---

## Botfusions Hesap Notları

- **X Premium hesabı** → 25.000 karakter limiti (standart 280 değil) — uzun thread yazılabilir
- **YouTube** → sadece Reel/Short destekliyor, normal video yok
- **Pinterest** → GEO içerikleri için `AI-Botfusions-GEO` board'u kullan (`1091067515915706441`)
- **Facebook** → Kişisel hesap (Ömer Tokgöz) — şirket sayfası değil, buna göre ton ayarla

---

## Karakter Limitleri (Kritik!)

| Platform | Limit |
|----------|-------|
| X (Twitter) | **280** karakter |
| Bluesky | 300 |
| Threads | 500 |
| Pinterest | 500 |
| LinkedIn | 3.000 |
| TikTok | 4.000 |
| Instagram | 2.200 |
| Facebook | 63.206 |

> ⚠️ OmniSocials en katı limiti aşarsa tüm postu reddeder. X ile birlikte post atılıyorsa `x` anahtarında 280 karakter versiyonu **zorunludur**.

---

## Botfusions İçin Tipik Senaryo

### Kampanya Görseli + Metin → Tüm Platformlar

```python
# content-repurposer çıktısından gelen metinler
content = {
    "default": "GEO hizmetimizle markanız yapay zeka aramalarda öne çıksın. Detaylar için link'e tıklayın.",
    "x": "AI aramalarında görünür olun 🎯 GEO hizmetimiz aktif! botfusions.com/geo-hizmet",
    "linkedin": "Yapay zeka destekli arama motorları artık SEO'yu değiştiriyor. Botfusions olarak...",
    "linkedin_page": "[Botfusions] GEO (Generative Engine Optimization) hizmetimiz yayında..."
}

# HyperFrames/canvas-design çıktısı URL'leri
media = {
    "default": "https://cdn.botfusions.com/geo-16x9.jpg",
    "instagram": "https://cdn.botfusions.com/geo-1x1.jpg"
}

# Hesap ID'leri — Botfusions Workspace (881407)
ACCOUNTS = {
    "instagram":  "881407_instagram",   # @botfusions — post, story, reel
    "facebook":   "881407_facebook",    # Ömer Tokgöz — post, story, reel
    "youtube":    "881407_youtube",     # @botfusionss — yalnızca reel
    "tiktok":     "881407_tiktok",      # @botfusions — post, reel
    "pinterest":  "881407_pinterest",   # cenk0342 — post
    "x":          "881407_x",           # @botfusionss — post (X Premium ✅)
}

# Pinterest Board ID'leri
PINTEREST_BOARDS = {
    "AI-Botfusions-GEO": "1091067515915706441",
    "Profil":            "1091067515915706431",
}
```

---

## Platform-Specific Parametreler (Kritik!)

OmniSocials bazı platformlar için **top-level anahtar** gerektirir. Bu parametreler `content` veya `accounts` ile aynı seviyede olmalıdır.

### YouTube Reel/Short

```json
{
  "content": {"default": "..."},
  "accounts": ["881407_youtube"],
  "type": "reel"
}
```

`type` top-level anahtar olarak `"reel"` olmalıdır. `post_type` veya içeride bir alan olarak **çalışmaz**.

### Pinterest (Board Seçimi Zorunlu)

```json
{
  "content": {"pinterest": "..."},
  "accounts": ["881407_pinterest"],
  "media_ids": ["26219"],
  "pinterest": {
    "board_id": "1091067515915706441",
    "title": "GEO ile AI Aramalarda One Cikarin",
    "link": "https://botfusions.com/geo-hizmet"
  }
}
```

`pinterest` **top-level anahtar** olmalıdır. `pinterest_board_id`, `board_id` (tek başına), `options.pinterest.board_id` gibi varyasyonlar **çalışmaz**. Board seçilmezse OmniSocials "Please select a Pinterest board" hatası verir.

### Doğrulanmış Board ID'leri

| Board Adı | ID |
|-----------|-----|
| AI-Botfusions-GEO | `1091067515915706441` |
| Profil | `1091067515915706431` |

---

## Medya Yükleme (Video)

Video yüklemek için explicit MIME type ve media_type parametreleri gerekir:

```bash
curl --ssl-no-revoke -X POST "https://api.omnisocials.com/v1/media" \
  -H "Authorization: Bearer $OMNISOCIALS_API_KEY" \
  -F "file=@video.mp4;type=video/mp4" \
  -F "media_type=video"
```

**Windows Notu:** `curl` SSL revocation check'te `CRYPT_E_NO_REVOCATION_CHECK` hatası verir → `--ssl-no-revoke` flag'i **zorunludur**.

---

## OmniSocials Auth Formatı

API key iki şekilde gönderilebilir:
- Header: `Authorization: Bearer <api_key>`
- Header: `X-API-Key: <api_key>`

---

## Önemli Notlar

1. **Hesap bağlantısı:** `app.omnisocials.com → Settings → Channels` üzerinden OAuth yapılmalı (tek seferlik, manuel)
2. **Account ID'leri:** `GET /accounts` ile alınan ID'ler sabit kalır — bir kere alınıp saklanabilir
3. **Rate limit:** 100 istek/dakika
4. **Test modu:** API key'i `omsk_test_` ile başlayan bir key ile gerçek yayın yapılmadan test edilebilir

---

## Dashboard Erişimi

- **URL:** https://app.omnisocials.com
- **API Key Yönetimi:** Settings → API
- **Kanal Bağlantısı:** Settings → Channels
- **Post Geçmişi:** Posts sekmesi

---

*Botfusions AI Reklam Ajansı | OmniSocials Social Publisher Skill v1.0.0 | Mayıs 2026*
