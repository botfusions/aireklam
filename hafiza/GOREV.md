# Hafıza Katmanı

Tüm modüllerin ortak deposu. Hiçbir şey kaybolmaz.

## Alt Klasörler (otomatik oluşacak)

| Klasör | İçerik |
|--------|--------|
| `rakip-arsivi/` | Günlük rakip post snapshot'ları |
| `trend-log/` | Haftalık trend özetleri |
| `hook-kutuphanesi/` | Denenmiş tüm hook'lar + performans skoru |
| `icerik-arsivi/` | Yayınlanan tüm içerikler + metrikler |
| `performans-tarihi/` | Uzun dönem kanal bazlı performans |

## Kural
Her içerik paketi yayınlandıktan 7 gün sonra performans notu ile arşivlenir.  
Hook kütüphanesi aylık güncellenir → en iyi 20 hook listesi tutulur.
