---
name: ads-report
description: PDF rapor uretimi ve musteri sunum formatinda reklam denetim raporu hazirlama. Ads audit ciktisini Health Score, bulgular, grafikler ve aksiyon planina donusturur.
version: 1.0.0
author: Botfusions AI Reklam Ajansi
category: advertising
---

# ads-report — PDF Audit Report Generator

**Komut:** `/ads report`  
**Amaç:** Tüm platform denetim verilerini profesyonel, müşteriye sunulabilir PDF raporuna dönüştür.  
**Bağımlılık:** `reportlab` Python paketi (opsiyonel, PDF için), aksi halde Markdown çıktı.

---

## Görev Tanımı

Bu skill, `/ads audit` veya tekil platform denetimlerinden üretilen verileri alır ve:
1. **Ads Health Score (0-100)** — Ağırlıklı platform puanı + harf notu (A-F)
2. **Platform karşılaştırma grafiği** — Radar/bar chart
3. **Öncelikli bulgular özeti** — Kritik → Yüksek → Orta
4. **Aksiyon planı** — 30/60/90 gün yol haritası
5. **Müşteri sunum formatında PDF** — Logo, renk paleti, sayfa düzeni

formatlarında çıktı üretir.

---

## Çalışma Akışı

```
1. Veri Toplama
   ├── /ads audit çıktısı (varsa) → otomatik parse
   ├── /ads google, /ads meta, vb. individual çıktılar → birleştir
   └── Manuel veri → kullanıcıdan platform scoreları iste

2. Skor Hesaplama
   ├── Platform ağırlıkları uygula (bkz. Scoring Matrix)
   ├── Severity multiplier hesapla
   └── Toplam Health Score → Harf Notu belirle

3. Rapor Üretimi
   ├── PDF mevcut → reportlab ile üret
   └── PDF yok → Markdown çıktı (copy-paste hazır)

4. Dosya Kaydet
   └── ads-report-[musteri]-[YYYY-MM-DD].pdf / .md
```

---

## Scoring Matrix

| Platform | Ağırlık | Max Puan |
|----------|---------|----------|
| Google Ads | %30 | 30 |
| Meta Ads | %25 | 25 |
| Tracking/Dönüşüm | %20 | 20 |
| Creative Kalite | %15 | 15 |
| Budget/Bidding | %10 | 10 |
| **TOPLAM** | **%100** | **100** |

### Harf Notu Eşiği

| Puan | Not | Mesaj |
|------|-----|-------|
| 90-100 | A | Mükemmel — İnce ayar yeterli |
| 80-89 | B | İyi — 2-3 kritik düzeltme |
| 70-79 | C | Orta — Sistematik iyileştirme gerekli |
| 60-69 | D | Zayıf — Acil müdahale |
| 0-59 | F | Kritik — Yeniden yapılandırma |

### Severity Multiplier

```
CRITICAL → x2.0  (bütçe yanıyor, dönüşüm sıfır, ROAS negatif)
HIGH     → x1.5  (önemli fırsatlar kaçıyor)
MEDIUM   → x1.0  (standart iyileştirme)
LOW      → x0.5  (kozmetik düzeltme)
```

---

## PDF Rapor Yapısı

### Sayfa 1 — Executive Summary
```
┌─────────────────────────────────────────┐
│  [MÜŞTERİ LOGO]        [TARİH]          │
│                                         │
│  ADS HEALTH SCORE                       │
│  ┌──────────────────┐                   │
│  │   [GAUGE: 0-100] │  NOT: B (82/100)  │
│  └──────────────────┘                   │
│                                         │
│  Platform Özeti:                        │
│  Google Ads ████████░░ 76/100           │
│  Meta Ads   ██████████ 91/100           │
│  Tracking   ████░░░░░░ 45/100  ⚠️        │
│  Creative   ███████░░░ 70/100           │
│  Budget     ████████░░ 80/100           │
└─────────────────────────────────────────┘
```

### Sayfa 2 — Kritik Bulgular (Top 10)
- Her bulgu: Platform | Başlık | Etkisi | Önerilen Aksiyon
- Severity renk kodu: 🔴 Kritik | 🟠 Yüksek | 🟡 Orta | 🟢 Düşük

### Sayfa 3 — Platform Detayları
- Google Ads: Kampanya türü analizi, Quality Score, PMax segmentleri
- Meta Ads: Advantage+ durumu, Creative fatigue, Audience overlap
- Tracking: Dönüşüm aksiyonları, Attribution, Privacy sandbox

### Sayfa 4 — Aksiyon Planı
```
30 GÜN (Hızlı Kazanımlar)
□ Dönüşüm takibini kur → Beklenen etki: +%40 görünürlük
□ Broad Match kaldır → Beklenen tasarruf: ₺X/ay
□ Negatif keyword listesi → Beklenen: -15% wasted spend

60 GÜN (Optimizasyon)
□ Smart Bidding geçişi → Target CPA: ₺X
□ Creative refresh → 5 yeni varyasyon
□ Audience segmentasyonu

90 GÜN (Büyüme)
□ Yeni kampanya türleri
□ A/B test sonuçları değerlendir
□ Ölçek büyütme planı
```

### Sayfa 5 — PPC Finansal Özet
- Mevcut spend/dönüşüm durumu
- Hedef CPA ve ROAS
- Break-even analizi
- Bütçe önerisi

---

## Kullanım Örnekleri

### Örnek 1: Tam Audit Sonrası Rapor
```
/ads report
```
→ En son çalıştırılan audit çıktısını kullan

### Örnek 2: Spesifik Veri ile Rapor
```
/ads report
[Google: 76/100, Meta: 91/100, Tracking: 45/100, Creative: 70/100, Budget: 80/100]
Müşteri: Botfusions | Dönem: Nisan 2026
```

### Örnek 3: Müşteri Adı ve Logo ile
```
/ads report --musteri "ABC Şirketi" --logo "/path/logo.png" --donem "Q1 2026"
```

---

## PDF Üretim Kodu (reportlab)

```python
# Kurulum: pip install reportlab
# Çalıştır: python ads_report.py

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.graphics.shapes import Drawing, Wedge
from reportlab.graphics import renderPDF
from datetime import datetime
import sys

def create_ads_report(data: dict, output_path: str):
    """
    data = {
        "musteri": "Şirket Adı",
        "donem": "Nisan 2026",
        "skorlar": {
            "google": 76,
            "meta": 91,
            "tracking": 45,
            "creative": 70,
            "budget": 80
        },
        "bulgular": [
            {"platform": "Tracking", "baslik": "Dönüşüm takibi eksik", 
             "severity": "CRITICAL", "aksiyon": "GA4 + Google Tag kurulumu"},
        ],
        "aksiyon_plani": {
            "30_gun": ["Dönüşüm takibini kur", "Broad Match kaldır"],
            "60_gun": ["Smart Bidding geçişi"],
            "90_gun": ["Ölçek büyütme"]
        }
    }
    """
    
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Ağırlıklı skor hesapla
    s = data["skorlar"]
    toplam = (s["google"] * 0.30 + s["meta"] * 0.25 + 
              s["tracking"] * 0.20 + s["creative"] * 0.15 + 
              s["budget"] * 0.10)
    
    not_map = {90: "A", 80: "B", 70: "C", 60: "D", 0: "F"}
    harf_not = next(v for k, v in sorted(not_map.items(), reverse=True) if toplam >= k)
    
    # Başlık
    story.append(Paragraph(f"<b>ADS HEALTH REPORT</b>", styles["Title"]))
    story.append(Paragraph(f"{data['musteri']} | {data['donem']}", styles["Normal"]))
    story.append(Spacer(1, 20))
    
    # Health Score
    story.append(Paragraph(f"<b>HEALTH SCORE: {toplam:.0f}/100 — Not: {harf_not}</b>", styles["Heading1"]))
    story.append(Spacer(1, 10))
    
    # Platform tablosu
    platform_data = [
        ["Platform", "Puan", "Ağırlık", "Katkı"],
        ["Google Ads", f"{s['google']}/100", "%30", f"{s['google']*0.30:.1f}"],
        ["Meta Ads", f"{s['meta']}/100", "%25", f"{s['meta']*0.25:.1f}"],
        ["Tracking", f"{s['tracking']}/100", "%20", f"{s['tracking']*0.20:.1f}"],
        ["Creative", f"{s['creative']}/100", "%15", f"{s['creative']*0.15:.1f}"],
        ["Budget/Bidding", f"{s['budget']}/100", "%10", f"{s['budget']*0.10:.1f}"],
        ["TOPLAM", f"{toplam:.0f}/100", "%100", f"{toplam:.1f}"],
    ]
    
    t = Table(platform_data, colWidths=[150, 80, 80, 80])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a2e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#A855F7')),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f8f0ff')]),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))
    
    # Bulgular
    if data.get("bulgular"):
        story.append(Paragraph("<b>KRİTİK BULGULAR</b>", styles["Heading2"]))
        severity_colors = {
            "CRITICAL": "#dc2626", "HIGH": "#ea580c",
            "MEDIUM": "#d97706", "LOW": "#16a34a"
        }
        for b in sorted(data["bulgular"], key=lambda x: ["CRITICAL","HIGH","MEDIUM","LOW"].index(x["severity"])):
            renk = severity_colors.get(b["severity"], "#666")
            story.append(Paragraph(
                f'<font color="{renk}">●</font> <b>[{b["platform"]}]</b> {b["baslik"]}<br/>'
                f'<i>Aksiyon: {b["aksiyon"]}</i>',
                styles["Normal"]
            ))
            story.append(Spacer(1, 5))
    
    # Aksiyon planı
    if data.get("aksiyon_plani"):
        story.append(Spacer(1, 10))
        story.append(Paragraph("<b>AKSİYON PLANI</b>", styles["Heading2"]))
        for donem, aksiyonlar in data["aksiyon_plani"].items():
            story.append(Paragraph(f"<b>{donem.replace('_', ' ').upper()}</b>", styles["Heading3"]))
            for a in aksiyonlar:
                story.append(Paragraph(f"□ {a}", styles["Normal"]))
    
    # Footer
    story.append(Spacer(1, 30))
    story.append(Paragraph(
        f"<i>Botfusions AI Reklam Ajansı | info@botfusions.com | +90 850 302 74 60 | {datetime.now().strftime('%d.%m.%Y')}</i>",
        styles["Normal"]
    ))
    
    doc.build(story)
    print(f"✅ Rapor üretildi: {output_path}")

if __name__ == "__main__":
    # Test verisi
    ornek_veri = {
        "musteri": "Botfusions",
        "donem": "Nisan 2026",
        "skorlar": {"google": 76, "meta": 91, "tracking": 45, "creative": 70, "budget": 80},
        "bulgular": [
            {"platform": "Tracking", "baslik": "Dönüşüm takibi kurulmamış", 
             "severity": "CRITICAL", "aksiyon": "GA4 dönüşüm aksiyonu + Google Tag kurulumu"},
            {"platform": "Google Ads", "baslik": "Tek keyword'e %99 bütçe akışı", 
             "severity": "HIGH", "aksiyon": "Keyword genişletme + negatif liste"},
        ],
        "aksiyon_plani": {
            "30_gun": ["Dönüşüm takibini kur", "Keyword çeşitlendir"],
            "60_gun": ["Smart Bidding geçişi", "Creative A/B testi"],
            "90_gun": ["Yeni kampanya türleri", "Ölçek büyütme"]
        }
    }
    output = sys.argv[1] if len(sys.argv) > 1 else "ads-report-test.pdf"
    create_ads_report(ornek_veri, output)
```

---

## Claude Yürütme Talimatları

Kullanıcı `/ads report` yazdığında:

1. **Veri kontrol et:** Mevcut konuşmada audit çıktısı var mı?
   - Varsa → otomatik parse et
   - Yoksa → "Hangi platformların audit verisi var? Puan/skor bilgisi ver" diye sor

2. **Skor hesapla:** Yukarıdaki Scoring Matrix'i uygula

3. **PDF dene:**
   ```bash
   pip install reportlab --quiet && python ads_report.py output.pdf
   ```
   - Başarılı → PDF dosya linki ver
   - Başarısız → Markdown rapor üret (aynı içerik, kopyala-yapıştır hazır)

4. **Müşteri bilgisi sor** (rapor için):
   - Müşteri adı?
   - Dönem?
   - Logo dosyası? (opsiyonel)

5. **Dosya adı:** `ads-report-[musteri-adi]-[YYYY-MM-DD].pdf`

6. **Çıktıyı kaydet:** Kullanıcının çalışma dizinine

---

## Markdown Fallback Formatı (PDF yoksa)

PDF üretilemezse şu formatı kullan:

```markdown
# 📊 ADS HEALTH REPORT
**Müşteri:** [Ad] | **Dönem:** [Dönem] | **Tarih:** [Tarih]

---

## 🎯 HEALTH SCORE: 82/100 — B

| Platform | Puan | Ağırlık |
|----------|------|---------|
| Google Ads | 76/100 | %30 |
| Meta Ads | 91/100 | %25 |
| Tracking | 45/100 | %20 |
| Creative | 70/100 | %15 |
| Budget | 80/100 | %10 |
| **TOPLAM** | **82/100** | - |

---

## 🚨 KRİTİK BULGULAR

🔴 **[CRITICAL] Tracking — Dönüşüm takibi eksik**
→ Aksiyon: GA4 + Google Tag kurulumu

🟠 **[HIGH] Google Ads — Tek keyword'e %99 bütçe**
→ Aksiyon: Keyword çeşitlendir, negatif liste ekle

---

## 📅 AKSİYON PLANI

**30 Gün (Hızlı Kazanımlar)**
- [ ] Dönüşüm takibini kur
- [ ] Keyword çeşitlendir

**60 Gün (Optimizasyon)**
- [ ] Smart Bidding geçişi
- [ ] Creative A/B testi

**90 Gün (Büyüme)**
- [ ] Yeni kampanya türleri
- [ ] Ölçek büyütme

---

*Botfusions AI Reklam Ajansı | info@botfusions.com | +90 850 302 74 60*
```

---

## Notlar

- **Dil:** Rapor varsayılan olarak Türkçe üretilir. `--lang en` ile İngilizce.
- **Renk:** Botfusions paleti kullanılır (`#A855F7` mor, `#1a1a2e` koyu)
- **Bağımlılık:** `reportlab` opsiyoneldir; yoksa Markdown fallback otomatik devreye girer
- **Entegrasyon:** `/ads audit` çıktısını doğrudan okuyabilir; ayrı veri girişi gerekmez

---

*Botfusions AI Reklam Ajansı | ads-report v1.0 | Nisan 2026*
