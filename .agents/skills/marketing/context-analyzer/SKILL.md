---
name: context-analyzer
description: "URL verildiginde web sitesini analiz eder, yapilandirilmis context markdown dosyasi olusturur. Marka sesi, rakipler, anahtar kelimeler, ozellikler, hedef kitle gibi bilgileri cikarir."
argument-hint: "analyze <url>"
version: 1.0.0
license: MIT
---

# Context Analyzer — URL'den Context Olusturucu

Bir URL verildiginde, web sitesini derinlemesine analiz ederek yapilandirilmis bir context markdown dosyasi olusturur.

## When to Activate

TRIGGER when the user:
- Bir URL verip analiz istediginde
- "Bu siteyi analiz et", "context olustur", "site incele" dediginde
- Yeni bir musteri/urun/sitesi eklendiginde
- "Rakip analiz et" + URL verdiginde
- "Marka profili cikar" dediginde
- Context klasoru bos oldugunda ve doldurilmasi gerektiginde

## Pipeline Architecture

```
URL
 ↓
[1. WEB SCRAPE]
  Web Search + Web Reader → ham icerik
 ↓
[2. ANALYZE]
  Marka sesi, ton, hedef kitle, urunler, rakipler, anahtar kelimeler cikar
 ↓
[3. STRUCTURE]
  Yapilandirilmis markdown dosyasi olustur
 ↓
[4. SAVE]
  context/{domain}.md dosyasina kaydet
 ↓
[5. CROSS-REFERENCE]
  Diger context dosyalariyla iliskilendir
```

## Cikti Formatı

Her URL icin `context/{domain}.md` dosyasi olusturulur:

```markdown
# {Marka Adi} — Context Analizi

> Analiz Tarihi: {tarih}
> URL: {url}
> Domain: {domain}

## 1. Marka Ozeti
- Marka adi:
- Slogan/motto:
- Kurulus yili:
- Lokasyon:
- Sektör:
- Calisan sayisi (tahmin):
- Hedef pazar:

## 2. Urun/Hizmet Ozellikleri
### Ana Hizmetler
| Hizmet | Aciklama | Fiyat Araligi |
|--------|----------|---------------|
| ...    | ...      | ...           |

### Fark Yaratan Ozellikler (USP)
1.
2.
3.

## 3. Hedef Kitle
### Birincil
- Demografi:
- Sektör:
- Sirket buyuklugu:
- Pain points:
- Awareness seviyesi:

### Ikincil
- ...

## 4. Marka Sesi ve Ton
### Ton Ozellikleri
- Genel ton: (profesyonel/samimi/otiritk/egitici)
- Dil: (resmi/gunluk/teknik)
- Yaklasim: (data-driven/hikaye odakli/duygusal)

### Ornek Ifadeler
- "..." → [ton analizi]
- "..." → [ton analizi]

### Kullanilan Anahtar Kelimeler
- Sik kullanilan terimler:
- Jargon:
- Cagri ifadeleri:

## 5. Rakipler
| Rakip | URL | Ortak Noktalar | Farklari |
|-------|-----|----------------|----------|
| ...   | ... | ...            | ...      |

## 6. Anahtar Kelimeler
### Marka Kelimeleri
- ...

### Urun/Hizmet Kelimeleri
- ...

### Long-tail Firsatlar
- ...

## 7. Gorsel Kimlik
### Renk Paleti
- Ana renk: #{hex}
- Ikincil: #{hex}
- Vurgu: #{hex}

### Tipografi
- Baslik fontu:
- Govde fontu:

### Gorsel Stil
- (minimal/karmasik, fotocekitik/illüstratif, modern/klasik)

## 8. Teknik Altyapi
### Platform
- CMS:
- Hosting:
- Analytics:

### SEO Durumu
- Meta title:
- Meta description:
- H1:
- Schema markup:

## 9. Icerik Stratejisi Gozlemi
### Blog/Icerik
- Sıklık:
- Konular:
- Kalite:

### Sosyal Medya
- Aktif platformlar:
- Gonderi sikligi:
- Takipci sayisi (tahmin):

## 10. Dijital Pazarlama Gozlemi
### Reklam Varligi
- Google Ads:
- Meta Ads:
- LinkedIn:

### E-posta
- Newsletter:
- Lead magnet:

## 11. Guclu Yonler
1.
2.
3.

## 12. Zayif Yonler / Firsatlar
1.
2.
3.

---
*Bu dosya context-analyzer skill'i tarafından otomatik olarak oluşturuldu.*
```

## Uygulama Adimlari

### Adim 1: Web Icerigini Topla
```
1. Web Search → "{marka}" "{urun}" site:domain.com
2. Web Reader → https://domain.com (ana sayfa)
3. Web Reader → https://domain.com/hakkimizda (varsa)
4. Web Reader → https://domain.com/hizmetler (varsa)
5. Web Reader → https://domain.com/blog (varsa)
```

### Adim 2: Analiz Et
Her sayfadan sunlari cikar:
- Marka pozisyonu ve deger teklifi
- Hizmet/urun listesi ve aciklamalari
- Hedef kitle ipuclari (dil, ton, ornekler)
- Rakip bahsetmeleri
- Anahtar kelimeler (dogal dil, SEO)
- Gorsel kimlik (renkler, fontlar, stil)
- Teknik isaretler (CMS, tracking kodlari)

### Adim 3: Dosyayi Olustur
- Domain adindan dosya adi olustur: `context/{domain}.md`
- Yukaridaki sablonu doldur
- Kaydet

### Adim 4: Cross-Reference
- Diger context dosyalarinda ayni rakipler var mi kontrol et
- Anahtar kelime ortaklari tespit et
- Not ekle

## Kullanim Ornekleri

### Yeni Musteri Ekleme
```
Kullanici: "https://orneksite.com analiz et"
→ context-analyzer calisir
→ context/orneksite-com.md olusturulur
→ MANIFEST'e eklenir
```

### Rakip Analizi
```
Kullanici: "https://rakip1.com ve https://rakip2.com analiz et"
→ 2 dosya olusturulur
→ context/rakip1-com.md
→ context/rakip2-com.md
→ Karsilastirma raporu sunulur
```

### Botfusions Context Doldurma
```
Kullanici: "Botfusions context'lerini doldur"
→ product-marketing-context.md'den veri al
→ context/botfusions-com.md olustur
→ context/brand-voice.md doldur
→ context/features.md doldur
→ context/target-keywords.md doldur
→ context/competitor-analysis.md doldur
```

## Error Handling

- Site ulasilamaz → Web Search ile cache/alternatif sayfa dene
- Yetersiz icerik → Kullaniciya detay sor
- Domain zaten analiz edilmis → Ustuine guncelle, sifirdan olusturma
- Dil algilanamadi → Varsayilan Turkce, kullanicidan onay iste
- Rate limit → 30s bekle, tekrar dene

## Best Practices

### DO
- Her URL icin ayri dosya olustur
- Tarih ve kaynak URL'yi mutlaka ekle
- Anahtar kelimeleri Google arama dilinde yaz (Turkce)
- Rakip bilgilerini diger context dosyalariyla capraz kontrol et
- Gorsel kimlik bilgilerini hex kodlariyla kaydet

### DON'T
- Tek bir sayfayla yetinme (en az 3 sayfa tara)
- Varsayimlarla doldurma (belirsizse "tahmin" yaz)
- Context dosyasini 500 satiri gecirme (ozet tut)
- Eski dosyalari uzerine yazma (guncelle)
