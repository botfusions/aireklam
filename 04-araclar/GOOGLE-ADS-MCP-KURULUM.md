# Google Ads MCP Kurulum Raporu

**Tarih:** 4 Nisan 2026
**Hesap:** Botfusions — Customer ID: 3646875139
**MCP:** google-marketing-solutions/google_ads_mcp (Python, resmi Google MCP)

---

## 1. MCP Nedir?

MCP (Model Context Protocol), Claude gibi AI araçlarının harici API'lere bağlanmasını sağlayan bir protokoldür. Google Ads MCP sayesinde Claude doğrudan Google Ads hesabınızı yönetebilir.

---

## 2. Google Ads MCP Klasöre Kurulum — Çalışır mı?

### Claude Code (VS Code Extension) — EVET

```
AI Reklam Ajansı/
├── .mcp.json          ← Bu dosya klasör açıldığında otomatik yüklenir
└── 04-araclar/
    └── google_ads_mcp/   ← MCP sunucu kodu burada
```

- `.mcp.json` dosyası proje klasöründe olduğu için **klasör açıldığında otomatik çalışır**
- Ayar yapmanıza gerek yok, `uv` ve Python bilgisayarınızda kurulu olduğu sürece çalışır
- **Mevcut durum:** `.mcp.json` zaten hazır ve doğru yapılandırılmış

### Claude Desktop (Masaüstü Uygulama) — HAYIR ( proje bazlı değil)

- Claude Desktop **global config** kullanır, proje klasörüne bakmaz
- Config dosyası her yerde aynı olmalıdır
- Klasör açma kavramı yoktur, her zaman aynı config'i okur

---

## 3. Neden Çalışmadı? — Sorunun Kökü

### Sorun 1: İki Farklı Claude Desktop Sürümü, İki Farklı Config

Windows'ta Claude Desktop **iki farklı şekilde** kurulabiliyor ve her biri **farklı klasörden** config okuyor:

| Sürüm | Config Konumu |
|-------|--------------|
| **Web'den indirme** (exe) | `AppData\Roaming\Claude\claude_desktop_config.json` |
| **Microsoft Store** | `AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude_desktop_config.json` |

**Ne oldu?**
- Biz `AppData\Roaming\Claude\` altındaki config'i güncelledik (Google'ın resmi MCP)
- Ama kullanıcı **Microsoft Store sürümünü** kullanıyordu
- Store sürümü `Packages` klasöründeki config'i okuyordu — orada eski TrueClicks hala duruyordu
- Sonuç: Her yeniden başlatmada TrueClicks geri geliyordu

**Çözüm:** Her iki config dosyasını da güncelledik.

### Sorun 2: TrueClicks MCP vs Google Resmi MCP

| Özellik | TrueClicks (`@trueclicks/google-ads-mcp-js`) | Google Resmi (`google_ads_mcp`) |
|---------|----------------------------------------------|----------------------------------|
| Dil | Node.js / JavaScript | Python |
| Kimlik Doğrulama | Base64 token (sınırlı) | OAuth2 + Developer Token (tam erişim) |
| Araç Sayısı | ~5-10 araç | 25+ araç |
| Bakım | Topluluk (3. parti) | Google'ın kendi ekibi |
| Paket | npx ile çalışır, cache sorunu | uv ile çalışır, kararlı |
| Kurulum | Basit ama sınırlı | Daha adımlı ama güçlü |

**Geçiş nedeni:** TrueClicks yetersiz kaldı, Google'ın resmi MCP'si daha fazla araç ve tam API erişimi sunuyor.

---

## 4. Yapılan İşlemler (Kronolojik)

| # | İşlem | Durum |
|---|-------|-------|
| 1 | Google Ads MCP repo klonlandı (`04-araclar/google_ads_mcp/`) | Tamam |
| 2 | `uv sync` ile bağımlılıklar kuruldu (110 paket, Python 3.12) | Tamam |
| 3 | Developer Token alındı (ads.google.com/aw/apicenter) | Tamam |
| 4 | OAuth Client ID + Secret alındı (Google Cloud Console) | Tamam |
| 5 | OAuth akışı ile Refresh Token oluşturuldu (cenk@botfusions.com) | Tamam |
| 6 | `google-ads.yaml` oluşturuldu (tüm kimlik bilgileri) | Tamam |
| 7 | YAML dosyası home dizinine kopyalandı (`C:\Users\user\google-ads.yaml`) | Tamam |
| 8 | `.mcp.json` oluşturuldu (Claude Code / VS Code) | Tamam |
| 9 | `claude_desktop_config.json` güncellendi (Web indirme sürümü) | Tamam |
| 10 | `claude_desktop_config.json` güncellendi (Microsoft Store sürümü) | Tamam |
| 11 | Eski TrueClicks config ve npm cache temizlendi | Tamam |

---

## 5. Dosya Konumları

```
Kimlik Bilgileri:
  C:\Users\user\google-ads.yaml                          ← Ana credential dosyası
  ...\04-araclar\google_ads_mcp\google-ads.yaml           ← Kopya (uv bu klasörde çalışır)

MCP Sunucu Kodu:
  ...\04-araclar\google_ads_mcp\                          ← Google'ın resmi MCP (git clone)
  ...\04-araclar\google_ads_mcp\get-refresh-token.py      ← OAuth yardımcı script

Config Dosyaları:
  ...\AI Reklam Ajansı\.mcp.json                          ← Claude Code (VS Code) otomatik okur
  AppData\Roaming\Claude\claude_desktop_config.json       ← Claude Desktop (exe sürümü)
  AppData\Local\Packages\...\claude_desktop_config.json   ← Claude Desktop (Store sürümü)
```

---

## 6. Test Etmek İçin

### Claude Code (VS Code)
1. VS Code'da `AI Reklam Ajansı` klasörünü açın
2. Claude Code panelini açın
3. `/mcp` yazarak MCP durumunu kontrol edin → `google-ads` running olmalı
4. Test: "Google Ads kampanyalarımı listele"

### Claude Desktop
1. Claude Desktop'ı **tamamen kapatın** (taskbar'dan değil, sistem tepsisinden)
2. Yeniden açın
3. MCP durumunu kontrol edin → `google-ads` running olmalı
4. Test: "Google Ads hesabımı analiz et"

---

## 7. Bilinen Sorunlar

| Sorun | Çözüm |
|-------|--------|
| `uv` bulunamadı | Python ve uv kurulmuş olmalı: `pip install uv` |
| OAuth token süresi doldu | `get-refresh-token.py` ile yeniden alın |
| "Customer ID not found" hatası | `login_customer_id: 3646875139` YAML'da olmalı |
| MCP connecting ama yanıt yok | Google Ads API erişimi onaylanmamış olabilir — API Center'da kontrol |

---

## 8. Sonraki Adımlar

1. **Test** — MCP'nin gerçekten veri çektiğini doğrula
2. **Dönüşüm takibi** — `analytics-tracking` skill ile botfusions.com/geo-hizmet form tracking
3. **Kampanya optimizasyonu** — %99,4 tek kelimede bütçe sorunu
4. **Günlük rapor** — Otomatik spend + dönüşüm + anomali raporu

---

## 9. Sorun 3: `.mcp.json` Formatı VS Code ile Uyuşmuyor

### Sorun

`.mcp.json` dosyasını proje klasörüne `"mcpServers"` formatıyla oluşturduk ama VS Code bu formatı tanımadı. Sadece Pencil MCP göründü, Google Ads görünmedi.

**Neden?**

VS Code'un global MCP config'i (`AppData\Roaming\Code\User\mcp.json`) farklı bir format kullanıyor:

| Ortam | Dosya | Format Key |
|-------|-------|-----------|
| Claude Desktop | `claude_desktop_config.json` | `"mcpServers"` |
| VS Code (global) | `AppData\...\Code\User\mcp.json` | `"servers"` |
| VS Code (proje) | `.mcp.json` | `"mcpServers"` (teori) ama çalışmadı |

### Çözüm

Google Ads MCP'yi VS Code'un **global `mcp.json`** dosyasına `"servers"` formatıyla ekledik (Pencil gibi):

```json
// AppData\Roaming\Code\User\mcp.json
{
  "servers": {
    "pencil": { ... },
    "google-ads": {
      "command": "C:\\Users\\user\\.local\\bin\\uv.exe",
      "args": [
        "run",
        "--directory",
        "C:\\Users\\user\\Downloads\\Z.ai_claude code\\AI  Reklam  Ajansı\\04-araclar\\google_ads_mcp",
        "-m",
        "ads_mcp.server"
      ],
      "env": {
        "GOOGLE_ADS_CREDENTIALS": "C:\\Users\\user\\google-ads.yaml"
      },
      "type": "stdio"
    }
  }
}
```

**Not:** `uv` için tam path (`C:\\Users\\user\\.local\\bin\\uv.exe`) kullanıldı çünkü VS Code shell'i PATH'i farklı okuyabilir.

### Sonuç

| # | İşlem | Durum |
|---|-------|-------|
| 12 | `.mcp.json` proje dosyası oluşturuldu (`mcpServers` formatı) | Tamam ama çalışmadı |
| 13 | VS Code global `mcp.json` güncellendi (`servers` formatı) | Tamam |
| 14 | `uv` tam path olarak yazıldı | Tamam |

---

## 10. Config Dosyalarının Final Durumu

```
Aktif Config Dosyaları:

  VS Code (Claude Code):
    AppData\Roaming\Code\User\mcp.json         ← google-ads + pencil (AKTİF)

  Claude Desktop (exe sürümü):
    AppData\Roaming\Claude\claude_desktop_config.json   ← google-ads + lemma

  Claude Desktop (Microsoft Store):
    AppData\Local\Packages\...\claude_desktop_config.json ← google-ads + composio-canva

  Proje bazlı (şu an çalışmıyor):
    AI Reklam Ajansı\.mcp.json                 ← mcpServers formatı, tanınmadı
```

---

## 11. Sorun 4: YAML `use_proto_plus` Eksik

### Sorun

MCP sunucusu başlatılırken crash oldu:

```
ValueError: The client library configuration is missing the required "use_proto_plus" key.
```

Google Ads Python istemci kütüphanesi `use_proto_plus` alanını zorunlu kılıyor ama YAML dosyamızda yoktu.

### Çözüm

Her iki YAML dosyasına eklendi:

```yaml
# google-ads.yaml son satır
use_proto_plus: True
```

| # | İşlem | Durum |
|---|-------|-------|
| 15 | `use_proto_plus: True` home dizini YAML'a eklendi | Tamam |
| 16 | `use_proto_plus: True` proje klasörü YAML'a eklendi | Tamam |

---

## 12. Sorun 5: Transport Uyuşmazlığı (HTTP vs stdio)

### Sorun

MCP sunucusu `streamable-http` transport ile başlıyordu (`http://127.0.0.1:8000`), VS Code ise `stdio` transport bekliyordu. Sunucu başlıyor ama VS Code bağlanamıyordu — 15+ dakika "connecting" durumunda kaldı.

**Neden?** Google'ın `server.py` dosyasında transport sabit kodlanmıştı:

```python
# Orijinal (04-araclar/google_ads_mcp/ads_mcp/server.py)
mcp_server.run(
    transport="streamable-http",  # ← Sabit kodlanmış
    show_banner=False,
)
```

### Çözüm

Transport'ı ortam değişkeni ile kontrol edilebilir hale getirdik:

```python
# Düzeltilmiş
mcp_server.run(
    transport=os.getenv("MCP_TRANSPORT", "stdio"),  # ← Varsayılan: stdio
    show_banner=False,
)
```

- Varsayılan artık `stdio` — VS Code ile uyumlu
- HTTP transport gerekirse `MCP_TRANSPORT=streamable-http` ortam değişkeni ile kullanılabilir

| # | İşlem | Durum |
|---|-------|-------|
| 17 | `server.py` transport ortam değişkeni ile kontrol edilebilir yapıldı | Tamam |

---

## 13. Bağlantı Test Sonucu (4 Nisan 2026)

MCP bağlantısı başarılı:

```
list_accessible_accounts → ["3646875139", "5131327019"]
```

| Hesap ID | Açıklama |
|----------|----------|
| 3646875139 | Botfusions (ana hesap) |
| 5131327019 | İkinci hesap |

---

## 14. Sorun 6: Developer Token Sadece Test Erişimi

### Sorun

MCP bağlandı ama kampanya sorgusu hata verdi:

```
error_code: DEVELOPER_TOKEN_NOT_APPROVED
message: "The developer token is only approved for use with test accounts.
         To access non-test accounts, apply for Basic or Standard access."
```

**Neden:** Developer Token varsayılan olarak sadece test hesaplarıyla çalışır. Gerçek reklam hesaplarına erişmek için **Basic Access** başvurusu gerekli.

### Durum

- **Basvuru durumu:** Yapildi (4 Nisan 2026)
- **Beklenen onay suresi:** 1-3 gun
- **Basvuru yeri:** ads.google.com/aw/apicenter → Basic Access for Developer Token

### Onay Sonrasi Yapilacaklar

1. MCP ile kampanya verilerini cekme testi
2. Kampanya optimizasyonu (%99,4 tek kelime sorunu)
3. Donusum takibi kurulumu
4. Gunluk rapor otomasyonu

| # | Islem | Durum |
|---|-------|--------|
| 18 | Developer Token Basic Access basvurusu yapildi | **Beklemede** (1-3 gun) |

---

## 15. Tum Yapilan Isler — Ozet

| # | Islem | Durum |
|---|-------|--------|
| 1 | Google Ads MCP repo klonlandi | Tamam |
| 2 | `uv sync` ile bagimliliklar kuruldu | Tamam |
| 3 | Developer Token alindi | Tamam |
| 4 | OAuth Client ID + Secret alindi | Tamam |
| 5 | OAuth akisi ile Refresh Token olusturuldu (cenk@botfusions.com) | Tamam |
| 6 | `google-ads.yaml` olusturuldu | Tamam |
| 7 | YAML home dizinine kopyalandi | Tamam |
| 8 | `.mcp.json` proje dosyasi olusturuldu | Tamam |
| 9 | Claude Desktop config (exe surumu) guncellendi | Tamam |
| 10 | Claude Desktop config (Store surumu) guncellendi | Tamam |
| 11 | TrueClicks config ve npm cache temizlendi | Tamam |
| 12 | `.mcp.json` proje bazli denendi (calismadi) | Tamam |
| 13 | VS Code global `mcp.json` guncellendi | Tamam |
| 14 | `uv` tam path olarak yazildi | Tamam |
| 15 | `use_proto_plus: True` YAML'a eklendi | Tamam |
| 16 | `use_proto_plus: True` proje YAML'ina eklendi | Tamam |
| 17 | `server.py` transport stdio yapildi | Tamam |
| 18 | Developer Token Basic Access basvurusu | **Beklemede** |

---

## 16. YAPILACAKLAR — Bağımsız Google Ads Rapor Programı

**Hedef:** Claude Code / Claude Desktop olmadan çalışan, başkasına verilebilen bağımsız Python programı.

### Neden?

- Claude olmayan bilgisayarlarda da çalışsın
- Müşteriye veya çalışana verilebilsin
- Her sabah otomatik rapor üretsin
- Google Ads API'ye doğrudan bağlansın

### Program Yapısı

```
04-araclar/google-ads-rapor/
├── main.py              ← Tek dosya: çalıştır, raporu al
├── config.yaml          ← Kimlik bilgileri (developer_token vb.)
├── requirements.txt     ← pip install -r requirements.txt
├── templates/
│   └── rapor.html       ← HTML rapor şablonu
└── README.md            ← Kurulum ve kullanım talimatı
```

### Özellikler

| Özellik | Açıklama |
|---------|----------|
| Günlük rapor | Spend, CTR, tıklama, gösterim, dönüşüm |
| Kampanya özeti | Aktif kampanyalar, bütçe durumu |
| Anomali tespiti | Harcama ani artış, dönüşüm düşüş uyarısı |
| Keyword analizi | Düşük kalite skoru kelimeler |
| HTML çıktı | Tarayıcıda açılabilir rapor |
| E-posta (opsiyonel) | Gmail ile otomatik rapor gönderme |
| Zamanlama | Windows Task Scheduler ile her sabah çalıştırma |

### Kullanım Akışı

```bash
# 1. Kurulum
pip install -r requirements.txt

# 2. Config ayarla (tek seferlik)
# config.yaml içine credentials yaz

# 3. Rapor al
python main.py                    # Günlük rapor (HTML)
python main.py --rapor haftalik   # Haftalık rapor
python main.py --mail             # Raporu e-posta gönder
```

### Öncelik Tablosu

| # | Görev | Bağımlılık | Öncelik |
|---|-------|-----------|---------|
| 1 | Temel rapor scripti (main.py) | Basic Access onayı | Yüksek |
| 2 | config.yaml yapılandırması | Yok (şimdi yapılabilir) | Yüksek |
| 3 | HTML rapor şablonu | Yok (şimdi yapılabilir) | Orta |
| 4 | E-posta gönderimi | Gmail App Password | Orta |
| 5 | Anomali tespiti | Temel rapor scripti | Düşük |
| 6 | Windows Task Scheduler ayarı | Temel rapor scripti | Düşük |
| 7 | .exe paketleme (PyInstaller) | Tüm özellikler bittiğinde | Düşük |

### Alternatif: TrueClicks ile Şimdi Çalışan Versiyon

Basic Access beklenirken TrueClicks API kullanılarak hemen çalışan bir versiyon da yapılabilir. Ancak bu TrueClicks altyapısına bağımlı olur.

### Teknoloji

- **Python 3.11+**
- **google-ads** kütüphanesi (resmi Google Python istemcisi)
- **Jinja2** (HTML şablon)
- **smtplib** (e-posta, yerleşik)

---

## 17. YAPILACAKLAR — Pixa MCP (Görsel Üretim)

**Hedef:** Pixa AI görsel üretim MCP'sini projeye bağlamak.

### Nedir?

Pixa, AI tabanlı görsel üretim platformu. MCP endpoint'i üzerinden Claude ile entegre çalışabilir.

- **Endpoint:** `https://mcp.pixa.com/mcp`
- **Transport:** Streamable HTTP
- **Kullanım:** Reklam görselleri, sosyal medya içerikleri, kreatif üretimi

### Bağlantı Config

```json
// VS Code mcp.json veya .mcp.json'a eklenecek:
"pixa": {
  "url": "https://mcp.pixa.com/mcp",
  "type": "streamable-http"
}
```

### Bekleyenler

| # | Görev | Durum |
|---|-------|--------|
| 1 | Pixa hesabı / API key bilgisi alınması | **Beklemede** (kullanıcıdan) |
| 2 | VS Code mcp.json'a ekleme | API key sonrası |
| 3 | Test — görsel üretim denemesi | Config sonrası |
| 4 | Reklam görselleri için prompt şablonları oluşturma | MCP çalışır durumda olunca |

### Mevcut Görsel Pipeline ile İlişki

```
Şu anki:
  Gemini Nano Banana Pro (kie.ai) → URL → Google Sheets

Pixa eklentisi:
  Pixa MCP → Claude ile doğrudan görsel üretim → 02-gorseller/ klasörüne kayıt

İkisi birlikte çalışabilir — farklı formatlar için farklı araçlar:
  Pixa → Instagram 1:1, Facebook 16:9 kreatifler
  Gemini → Daha hızlı üretim, toplu iş
```

---

## 18. YAPILACAKLAR — Canva Entegrasyonu

**Hedef:** Canva ile reklam görseli tasarımı ve şablon yönetimi.

### Denenen Yöntemler

| # | Yöntem | Sonuç |
|---|--------|-------|
| 1 | Composio Canva MCP (`mcp-remote https://mcp.composio.dev/canva`) | **Başarısız** — Endpoint HTML döndürüyor, MCP protokolü çalışmıyor |
| 2 | `adoptai-mcp canva` npm paketi | **Belirsiz** — Çıktı vermedi |
| 3 | Canva Python SDK (`pip install canva`) | **Yok** — PyPI'da resmi SDK bulunamadı |

### Mevcut Canva Seçenekleri

| Seçenek | Açıklama | Durum |
|---------|----------|-------|
| **Canva Connect REST API** | developers.canva.com'dan OAuth ile erişim | Mümkün — hesap gerekli |
| **Canva Apps SDK** | Node.js tabanlı, Canva içinde çalışan uygulamalar | Farklı amaç |
| **3. parti MCP** | Composio, AdoptAI vb. | Şu an çalışmıyor |

### Önerilen Yol: Canva Connect REST API

Canva'nın resmi REST API'si ile Python `httpx` kullanarak:

```
04-araclar/canva-api/
├── main.py              ← Tasarım oluştur, export et
├── config.yaml          ← OAuth credentials
├── requirements.txt     ← httpx
└── README.md
```

**Ne gerekli:**
1. Canva Developer hesabı → developers.canva.com
2. OAuth Client ID + Secret
3. Access Token (OAuth akışı ile)

### Bekleyenler

| # | Görev | Durum |
|---|-------|--------|
| 1 | Canva Developer hesabı açma | **Beklemede** (kullanıcıdan) |
| 2 | OAuth credentials alma | Hesap sonrası |
| 3 | Python REST API istemcisi yazma | Credentials sonrası |
| 4 | VS Code MCP config'ine ekleme | Çalışan API sonrası |

---

## 19. CMO Stratejisi — 3 Fazlı Plan

### Faz 1: HEMEN (TrueClicks ile)

TrueClicks MCP, kendi onaylı Developer Token'ını kullandığı için Basic Access beklemeden çalışır.

**VS Code MCP Config'e eklendi:**

```json
"trueclicks-ads": {
  "command": "C:\\Program Files\\nodejs\\npx.cmd",
  "args": ["-y", "@trueclicks/google-ads-mcp-js", "--token=..."],
  "type": "stdio"
}
```

**Kullanılabilecek araçlar:**

| Komut | Açıklama |
|-------|----------|
| `/ads audit` | Tüm platformlarda tam denetim (225+ kontrol) |
| `/ads google` | Google Ads derin analiz (74 kontrol) |
| `/ads competitor` | Rakip reklam araştırması |
| `/ads creative` | Kreatif kalite denetimi |
| `/ads budget` | Bütçe optimizasyonu |
| `/ads plan saas` | SaaS reklam stratejisi |
| `/ads meta` | Meta/Facebook Ads analiz |

### Faz 2: Basic Access Gelince (Google Resmi API)

| Özellik | TrueClicks | Google Resmi API |
|---------|-----------|-----------------|
| Veri okuma | Var | Var |
| Kampanya oluşturma | Sınırlı | Tam |
| GAQL sorgusu | Sınırlı | 25+ araç |
| Otomatik teklif | Yok | Var |
| Toplu işlem | Yok | Var |

### Faz 3: Bağımsız Program

Claude olmadan çalışan Python script:
- Her sabah otomatik rapor (HTML + e-posta)
- Müşteriye/çalışana verilebilir
- .exe olarak paketlenebilir

---

## 20. Claude Ads Skill Kurulumu

**Kaynak:** https://github.com/AgriciDaniel/claude-ads

**Kurulum:** `04-araclar/claude-ads/install.ps1` çalıştırıldı.

**Yüklenenler:**
- 1 ana skill (ads orchestrator)
- 17 alt-skill (platform + fonksiyonel + kreatif)
- 10 agent (6 denetim + 4 kreatif)
- 23 referans dosyası
- 11 sektör şablonu

---

## 21. Mevcut MCP Durumu (10 Nisan 2026)

| MCP | VS Code | Claude Desktop | Durum |
|-----|---------|---------------|-------|
| `pencil` | Var | - | Çalışıyor |
| `google-ads` (resmi) | Var | Var | Bağlı, Basic Access bekliyor |
| `trueclicks-ads` | Var | Var (gads) | **Çalışıyor** |
| `composio-canva` | Kaldırıldı | - | Endpoint bozuk |
| `lemma` | - | Var | Çalışıyor |
| `mcp-obsidian` | - | Var | Çalışıyor |

---

*Botfusions AI Reklam Ajansi — Google Ads MCP Kurulum Raporu*
*Son guncelleme: 10 Nisan 2026 — CMO stratejisi, Claude Ads kurulumu, TrueClicks VS Code eklendi*
