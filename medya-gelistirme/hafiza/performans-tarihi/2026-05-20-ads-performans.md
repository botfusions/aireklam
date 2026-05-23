---
date: 2026-05-20
tags: [ads-performans, google-ads, botfusions]
kaynak: gunluk-agent
customer_id: "3646875139"
---

# Google Ads Performans — 2026-05-20

## ⚠️ Veri alınamadı

Google Ads MCP bu oturumda doğrudan erişilebilir durumda değil.  
Lokal kurulum (`04-araclar/google_ads_mcp/`) Claude Desktop oturumu gerektirir.

**Sebep:** Scheduled task ortamında Google Ads MCP tool'u aktif bağlantı listesinde yer almıyor.

---

## 📋 Manuel Kontrol Notları

Bir sonraki manuel oturumda şunlar kontrol edilmeli:

- [ ] Dünkü toplam harcama (TL) — `advertising/ads-google` skill ile
- [ ] Kampanya bazlı CTR değerleri
- [ ] En yüksek harcamalı keyword (GEO keyword bütçe dağılımı %99.4 sorunu devam ediyor mu?)
- [ ] Dönüşüm sayısı (geo-hizmet form submit)

## 🚨 Bilinen Anomali (Önceki Oturumlardan)

> Bütçenin **%99.4'ü tek keyword'de** harcanıyor — bütçe dağıtımı yapılmamışsa hâlâ kritik risk

**Aksiyon:** Bir sonraki manuel oturumda Google Ads MCP üzerinden keyword bütçe dağılımı kontrol edilmeli ve gerekirse `advertising/ads-budget` skill çalıştırılmalı.

---

## 🔧 Teknik Not

Google Ads MCP'yi scheduled task ortamında çalıştırmak için `.mcp.json` konfigürasyonunun Cowork oturumuna da tanıtılması gerekiyor.  
İlgili skill: `advertising/ads-google` · API dosyası: `04-araclar/google_ads_mcp/google-ads.yaml`
