### 2. Mühendislik Yaklaşımıyla Yeniden Yapılandırılmış Prompt Sistemi

Yapay zekanın gerçekten sizin için bir SEO asistanı gibi çalışması için aşağıdaki adımları ve düzeltilmiş promptları kullanmalısınız.

*(Not: Aşağıdaki promptları Claude'a kopyalarken köşeli parantez içindeki `[...]` alanları kendi verilerinizle doldurun. Dosya yüklemeniz gereken yerleri belirttim.)*

#### ADIM 0: Sistem Bağlamı (System Prompt)
*Bu promptu her yeni sohbette (chat) en başta verin ki Claude ne yapacağını bilsin.*

```text
Sen uzman bir Yerel SEO ve Dijital Pazarlama stratejistisin. Görevin, aşağıda bilgilerini verdiğim yerel işletmemin arama motorlarındaki sıralamasını, trafiğini ve gelirini artırmaktır.

Bana tavsiye verirken her zaman hızlı kazanımları (quick wins) önceliklendir. Her tavsiye için etki derecesini (Yüksek/Orta/Düşük) ve sonuç alma süresini belirt. Rakiplerle karşılaştırma yaparken sonuçları her zaman tablo formatında ver. Tahmin yürütme, emin olmadığın verilerde benden ek bilgi veya dosya iste.

İŞLETME BAĞLAMI:
İşletme Adı: [İşletme Adı]
Hizmet Alanları: [Şehir 1], [Şehir 2], [Şehir 3]
Ana Hizmetler: [Hizmet 1], [Hizmet 2], [Hizmet 3]
Hedef Müşteri ve Ortalama İş Değeri: [Kimdir] / [X TL/Dolar]
Hedeflenen Anahtar Kelimeler: [Kelime 1], [Kelime 2], [Kelime 3]
Mevcut En Büyük Sorun: [Sorunu tek cümleyle açıklayın]
Ana Rakipler: [Rakip 1], [Rakip 2], [Rakip 3]
```

---

#### BÖLÜM 1: Google İşletme Profili (GBP) Optimizasyonu

*Mühendis Notu: Claude rakiplerinizin haritasına giremez. Rakiplerin kategorilerini, niteliklerini ve yorumlarını sizin kopyalayıp promptun altına yapıştırmanız veya ekran görüntüsü/metin belgesi olarak yüklemeniz gerekir.*

**Prompt 1 & 2: Kategori ve Nitelik (Attribute) Analizi**
```text
Aşağıdaki metinde/dosyada benim işletmemin ve 3 ana rakibimin Google İşletme Profili bilgileri (kategoriler ve işletme nitelikleri) yer almaktadır.
[Buraya rakiplerin profillerinden kopyaladığınız metinleri yapıştırın]

Lütfen şu analizi yap:
1. Rakiplerimin sahip olduğu ama bende olmayan 'Ana Kategori' ve 'Alt Kategorileri' tablo olarak listele.
2. Rakiplerimin kullandığı "ücretsiz keşif, 7/24 açık, tecrübeli" gibi işletme niteliklerini (attributes) çıkar ve eksiklerimi göster.
3. Hangi kategorileri ve nitelikleri acilen eklemem gerektiğini öncelik sırasına göre yaz.
```

**Prompt 3 & 4: Yorum ve Yanıt Stratejisi**
```text
Ekte/Aşağıda 3 ana rakibimin aldığı son 50 yorumun metinleri bulunmaktadır. 
[Yorumları buraya yapıştırın veya CSV olarak yükleyin]

1. Rakiplerin yorumlarında en çok geçen olumlu anahtar kelimeleri ve hizmet/bölge isimlerini çıkar (Müşteriler neyi seviyor?).
2. En çok şikayet edilen 5 konuyu listele (Fırsat boşluklarımız neler?).
3. Benim işletmem için; 5 yıldızlı, 4 yıldızlı, 3 yıldızlı ve 1-2 yıldızlı yorumlara verilecek, içinde [Anahtar Kelimelerim] geçen, insansı ve profesyonel 3'er adet yanıt şablonu oluştur (her biri 40-80 kelime).
```

**Prompt 5: Harita Gönderileri (GBP Posts) Takvimi**
```text
Bana yerel işletmem için 8 haftalık bir Google İşletme Profili (GBP) gönderi takvimi hazırla. 
- Haftada 3 gönderi olacak.
- İçerik karması: Sezonluk teklifler, Öncesi/Sonrası proje tanıtımları, [Bölge 1] ve [Bölge 2] odaklı yerel mesajlar, müşteri yorumu öne çıkarmaları ve eğitici içerikler.
- Her gönderide [Hedef Anahtar Kelimeler] doğal bir şekilde geçmeli ve net bir Call-To-Action (Hemen Ara, Teklif Al vb.) bulunmalı.
- İlk 4 haftanın metinlerini doğrudan yayınlamaya hazır şekilde, görsellerde ne olması gerektiğiyle (Image Prompt) birlikte yaz.
```

**Prompt 6 & 7 & 8: GBP Açıklaması ve Hizmetler**
```text
Google İşletme profilim için 750 karakteri geçmeyecek 3 farklı işletme açıklaması yaz:
Versiyon 1: Anahtar kelime odaklı (Maksimum SEO sinyali)
Versiyon 2: Dönüşüm odaklı (Okuyanı hemen aramaya teşvik eden)
Versiyon 3: Güven odaklı (Deneyim, yerellik ve yorumlara odaklanan)
İçinde mutlaka [Hizmetler] ve [Bölgeler] geçsin. Robotik değil, samimi bir dil kullan.

Ayrıca [Hizmet 1, Hizmet 2, Hizmet 3] için haritamda kullanacağım, her biri 40-60 kelime arası olan, fayda ve problem çözme odaklı hizmet açıklamaları yaz.
```

---

#### BÖLÜM 2: Web Sitesi ve İçerik Üretimi

*Mühendis Notu: Bu aşamada SEMrush, Ahrefs veya Google Search Console'dan aldığınız verileri dışa aktarıp (Export CSV) Claude'a dosya olarak yüklemelisiniz.*

**Prompt 9, 10 & 12: Keyword Gap ve GSC Veri Analizi**
```text
Ekte, sitemin Google Search Console verileri ve SEMrush'tan aldığım rakip anahtar kelime boşluğu (Keyword Gap) verileri bulunmaktadır. [CSV dosyasını yükleyin]

Lütfen bu verileri analiz et ve şunları bul:
1. 2. Sayfa Fırsatları: Şu an 11. ve 20. sıralar arasında olduğum ve en çok gösterim (impression) alan 10 anahtar kelimeyi tespit et.
2. Kayıp Fırsatlar: Rakiplerimin trafik aldığı ama benim hiç sıralanamadığım yüksek aranma hacimli/düşük zorluk dereceli ilk 20 kelimeyi listele.
3. Bana 30 günlük bir aksiyon planı çıkar: Hangi sayfaların Başlık (Title) ve Meta Açıklamalarını değiştirmeliyim? Hangi kelimeler için sıfırdan sayfa açmalıyım?
```

**Prompt 11: Yerel Hizmet Sayfası Oluşturucu (Programatik SEO Mantığı)**
```text
Web sitem için şehre özel hizmet sayfaları oluşturmak istiyorum.
Hizmet: [Hizmet Adı]
Hedef Şehir: [Şehir Adı]

Bana bu sayfa için SEO uyumlu bir iskelet ve içerik yaz:
- SEO Title (Max 60 karakter) ve Meta Description (Max 155 karakter).
- İkna edici bir H1 başlığı.
- O şehirdeki müşterinin acil problemini çözen 100 kelimelik giriş.
- "Neden Bizi Seçmelisiniz?" bölümü (O şehre özgü yerel simgeler veya sokak adları kullanarak güven ver).
- Süreç ve Hizmet Detayları bölümü.
- Bu şehre özel sorulabilecek 3 adet SSS (Sıkça Sorulan Sorular) ve cevapları.
```

**Prompt 13 & 17: Duygu Analizi ve İçerik Boşluğu**
```text
Ekte rakiplerimin hizmet süreçleriyle ilgili hem iyi hem kötü müşteri yorumları/geri bildirimleri var. [Metni yapıştırın]

Bu verileri kullanarak "Duygu Analizi" yap:
1. İnsanların bu hizmeti almadan önceki en büyük korkuları ve hizmetten sonra yaşadıkları en büyük rahatlamalar neler?
2. Müşterilerin kullandığı kesin ve duygusal ifadeleri (örn: "her yeri batıracaklar sanıyordum ama tertemiz bıraktılar") tespit et.
3. Web sitemin Ana Sayfa Başlığını (Hero Headline) ve Alt Başlığını, müşterilerin bu duygusal dilini kullanarak, güven verecek şekilde yeniden yaz.
```

---

#### BÖLÜM 3: Backlink, Otorite ve Teknik Analiz

**Prompt 14 & 15: Backlink ve Citation (Yerel Dizin) Analizi**
```text
Ekte rakiplerimin Ahrefs/SEMrush backlink profili CSV dosyası bulunmaktadır. [Dosyayı Yükleyin]

1. En az 2 rakibimin link aldığı ama benim link almadığım siteleri (Domainler) bul.
2. Bu linklerin türünü (Dizin, Haber sitesi, Blog, Sponsorluk) kategorize et.
3. Bu sitelerden link alabilmem için bana gerçekçi bir 90 günlük erişim (outreach) stratejisi ve webmasterlara göndereceğim 1 adet profesyonel e-posta şablonu hazırla.
```

**Prompt 18: Varlık (Entity) Optimizasyonu ve Schema**
```text
İşletmemin Google'ın Bilgi Grafiğinde (Knowledge Graph) güçlü bir varlık (Entity) olmasını istiyorum.
İşletme Bilgileri: [Ad, Adres, Telefon, Web Sitesi, Kurucusu, Sektör]

Bana web sitemin ana sayfasına eklemek üzere hatasız, eksiksiz ve güncel bir "LocalBusiness JSON-LD Schema Markup" kodu yaz. Kodun içine [Sosyal Medya Linklerim] ve [Hizmet Bölgelerim] dahil olsun. Sadece kodu ver, doğrudan kopyalayıp siteme ekleyebileyim.
```

---

### Özet ve Uygulama Planı (Nasıl Çalışmalısınız?)

Makale yazarı, promptların "sihirli" olduğuna inanıyor ancak mühendislikte sihir yoktur, **doğru veri girdisi** vardır. 

Bu sistemi kullanırken:
1. **Araçları Kendiniz Kullanın:** Ahrefs, SEMrush, GSC veya Google Haritalar'a girip rakiplerinizin verilerini dışa aktarın (CSV olarak indirin).
2. **Claude'a Veri Verin:** Orijinal metindeki "Git şunu araştır" komutları yerine, benim yukarıda revize ettiğim **"Ekteki veriyi analiz et"** komutlarını kullanın.
3. **Parçala ve Yönet:** Her adımı (Bölüm 1, Bölüm 2 vb.) ayrı bir mesajda (promptta) yapın. LLM'den tek mesajda tüm SEO stratejisini yapmasını isterseniz sığ ve genelleştirilmiş, işe yaramaz sonuçlar alırsınız.