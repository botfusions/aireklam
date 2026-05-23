# GSC → NocoDB Agentic Pipeline

Google Search Console verilerini otomatik olarak çekip NocoDB'ye aktaran, anomali tespit eden ve rapor üreten agentic workflow sistemi.

---

## Ne Yapar?

```
GSC API → gsc_nocodb_pipeline.py → NocoDB → Rapor / Anomali Alarmı
```

Her çalıştırmada şunları yapar:

- Keyword pozisyonlarını ve quick win fırsatlarını çeker
- Düşük CTR sayfaları tespit eder
- Yükselen sorgu trendlerini bulur
- Tüm veriyi NocoDB'ye kaydeder (4 tablo)
- Önceki dönemle karşılaştırarak anomali tespiti yapar
- `logs/` klasörüne metin raporu bırakır

---

## Dosya Yapısı

```
05-gsc-nocodb/
├── agent.py                  ← Otonom ajan — buradan çalıştır
├── gsc_nocodb_pipeline.py    ← Pipeline motoru (GSC → NocoDB)
├── nocodb_setup.py           ← İlk kurulum (tablo oluşturma)
├── requirements.txt          ← Python bağımlılıkları
├── .env.example              ← Ortam değişkenleri şablonu
├── .env                      ← (Git'e commit etme!)
├── clients/                  ← Müşteri bazlı config dosyaları
├── reports/                  ← Üretilen PDF/HTML raporlar
├── logs/                     ← Agent çalışma logları (tarihli .txt)
└── schemas/                  ← Tablo şema yedekleri
```

---

## Kurulum (İlk Kez)

### 1. Bağımlılıkları yükle

```bash
cd 05-gsc-nocodb
pip install -r requirements.txt
```

### 2. Ortam değişkenlerini ayarla

```bash
cp .env.example .env
```

`.env` dosyasını aç ve şu değerleri doldur:

```env
GSC_CREDENTIALS_PATH=/path/to/gsc-service-account.json
NOCODB_BASE_URL=https://nocodb.turklawai.com
NOCODB_API_TOKEN=your_nocodb_token_here
```

> **GSC Service Account nasıl alınır?**
> Google Cloud Console → IAM → Service Accounts → JSON key indir.
> GSC'de bu hesabı site sahibi olarak ekle.

> **NocoDB API Token nerede?**
> NocoDB → Team & Auth → API Token sekmesi.

### 3. NocoDB base ve tabloları oluştur

```bash
# Mevcut base'leri listele
python nocodb_setup.py --list

# Base oluştur ve tabloları kur
python nocodb_setup.py --base "Botfusions SEO" --create
```

Otomatik oluşturulan 4 tablo:

| Tablo | İçerik |
|-------|--------|
| `gsc_keywords`  | Keyword pozisyonları, quick win fırsatları, ticari niyet skoru |
| `gsc_pages`     | Düşük CTR sayfalar, kaçırılan tıklama hesabı |
| `gsc_trends`    | Son 7 günde yükselen sorgular |
| `gsc_summary`   | Günlük özet — toplam tıklama, CTR, pozisyon |

---

## Kullanım

### Tek müşteri çalıştır

```bash
python agent.py --client botfusions
python agent.py --client botfusions --days 7
python agent.py --client horecamark --days 30
```

### Tüm müşterileri çalıştır

```bash
python agent.py --all
python agent.py --all --days 14 --alert-threshold 15
```

### Parametreler

| Parametre | Varsayılan | Açıklama |
|-----------|------------|----------|
| `--client` | — | Müşteri ID (zorunlu, `--all` yoksa) |
| `--all` | false | Tüm müşteriler |
| `--days` | 30 | Kaç günlük GSC verisi |
| `--alert-threshold` | 20 | Anomali eşiği (% değişim) |

### Sadece pipeline (ajan olmadan)

```bash
python gsc_nocodb_pipeline.py --client botfusions --days 30 --report
```

---

## Yeni Müşteri Ekleme

`gsc_nocodb_pipeline.py` dosyasındaki `CLIENT_PROFILES` dict'ine ekle:

```python
"yeni-musteri": {
    "client_id": "yeni-musteri",
    "site_url": "https://yeni-musteri.com",
    "nocodb_base": "Yeni Müşteri SEO",   # NocoDB'deki base adı
},
```

Ardından NocoDB'de base oluştur:

```bash
python nocodb_setup.py --base "Yeni Müşteri SEO" --create
```

---

## Zamanlanmış Çalıştırma (Cron)

Her sabah 08:00'de tüm müşteriler için çalıştır:

```bash
# crontab -e
0 8 * * * cd /path/to/AI\ Reklam\ Ajansı/05-gsc-nocodb && python agent.py --all >> logs/cron.log 2>&1
```

---

## Anomali Tespiti

Agent şu metriklerde önceki dönemle karşılaştırma yapar:

- **Tıklama** — %20+ düşüş → 🔴 alarm
- **Görüntüleme** — %20+ düşüş → 🔴 alarm
- **CTR** — %20+ düşüş → 🔴 alarm
- **Ortalama Pozisyon** — %20+ kötüleşme → 🔴 alarm
- Herhangi birinde %20+ iyileşme → 🟢 bilgi

Eşiği `--alert-threshold` parametresiyle değiştirebilirsin.

---

## Bağlantılı Sistemler

| Sistem | Konum | Açıklama |
|--------|-------|----------|
| GSC Modül | `04-araclar/seo-machine-modules/modules/google_search_console.py` | Temel veri çekme sınıfı |
| NocoDB | VPS 1 — https://nocodb.turklawai.com | Veri deposu |
| AI SEO Skill | `.agents/skills/marketing/ai-seo/SKILL.md` | GSC verilerini kullanan skill |
| API Entegrasyon Dok. | `.agents/API-INTEGRATIONS.md` | Tüm API kurulum rehberi |

---

*Botfusions AI Reklam Ajansı | 05-gsc-nocodb | Nisan 2026*
