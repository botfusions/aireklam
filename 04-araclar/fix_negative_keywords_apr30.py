# /// script
# requires-python = ">=3.10"
# dependencies = ["google-ads>=24.0.0"]
# ///
"""
30 Nisan 2026 — Boşa Giden Bütçe Düzeltmesi
Botfusions - Website traffic-Search-1 kampanyası

Sorun: Aşağıdaki terimler son 10 günde ~556 TL harcadı.
  - seo bot     → 285 TL (eski script'te "seobotx" vardı, "seo bot" EKSİKTİ!)
  - chat cpt    → 28 TL  (ChatGPT yazım hatası, alakasız)
  - website chatbot → 14 TL (yanlış intent)
  - Diğer araç/bilgi arayan terimler

Çalıştır: uv run python fix_negative_keywords_apr30.py
"""
import warnings
warnings.filterwarnings("ignore")

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
import os

YAML_PATH = os.path.expanduser("~/google-ads.yaml")
CUSTOMER_ID = "3646875139"
CAMPAIGN_ID = "23657484697"  # Website traffic-Search-1

# ─── EKLENECEKLİSTİ ──────────────────────────────────────────────────────────
# Kural: SADECE gerçek search terms raporundan gelen, 0 dönüşüm + alakasız terimler
# Şüphelileri buraya ekleme — yanlış negatif daha büyük zarar verir

NEGATIVE_KEYWORDS = [

    # ── Büyük kayıplar (son 10 gün) ──────────────────────────────────────────
    "seo bot",              # 285 TL — eski scriptte eksikti!
    "chat cpt",             # 28 TL  — ChatGPT yazım hatası
    # "website chatbot" → KALDIRILDI — bu hizmeti sunabiliyoruz, ana sayfaya yönlendiriliyor

    # ── Araç arayanlar (tool intent) ─────────────────────────────────────────
    "ahrefs",               # ahrefs competitors, ahrefs traffic checker vb.
    "a b test tool",        # test aracı arıyor
    "amplitude",            # analytics aracı
    "adjust",               # attribution aracı
    "seo web sitesi",       # araç arıyor (eski scriptte var mı kontrol)

    # ── Tamamen alakasız ─────────────────────────────────────────────────────
    "agencia seo ia",       # İspanyolca — Türkiye'yi hedeflemiyoruz
    "artificial intelligence in organizations",  # akademik/kurumsal
    "artificial intelligence operations",        # IT operasyon terimi

]

# ─── DOKUNMA — alakalı terimler (hata yapma) ─────────────────────────────────
# answer engine optimization   → MÜŞTERİ ADEYİ, ekleme
# agentic engine optimization  → MÜŞTERİ ADEYİ, ekleme
# agentic seo skill            → alakalı
# arama motoru optimizasyonu   → Türkçe SEO, alakalı
# geo search optimization      → alakalı
# generative engine optimization → zaten ADDED
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 60)
print("30 Nisan 2026 — Negatif Keyword Güncelleme")
print("=" * 60)
print(f"Kampanya    : Website traffic-Search-1 ({CAMPAIGN_ID})")
print(f"Müşteri ID  : {CUSTOMER_ID}")
print(f"Eklenecek   : {len(NEGATIVE_KEYWORDS)} keyword (Exact Match)")
print()
print("Eklenecekler:")
for kw in NEGATIVE_KEYWORDS:
    print(f"  🚫 [{kw}]")
print()

client = GoogleAdsClient.load_from_storage(YAML_PATH)
svc    = client.get_service("CampaignCriterionService")
c_svc  = client.get_service("CampaignService")

operations = []
for kw in NEGATIVE_KEYWORDS:
    op = client.get_type("CampaignCriterionOperation")
    c  = op.create
    c.campaign      = c_svc.campaign_path(CUSTOMER_ID, CAMPAIGN_ID)
    c.negative      = True
    c.keyword.text  = kw
    c.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
    operations.append(op)

try:
    response = svc.mutate_campaign_criteria(
        customer_id=CUSTOMER_ID,
        operations=operations,
    )
    print(f"✅ {len(response.results)} negatif keyword eklendi!\n")
    for i, result in enumerate(response.results):
        print(f"  ✓ [{NEGATIVE_KEYWORDS[i]}]")
    print()
    print("=" * 60)
    print("Tahmini aylık kurtarılan bütçe: ~1.600 TL")
    print("(Son 10 gün 556 TL × 3 = aylık projeksiyon)")
    print("=" * 60)

except GoogleAdsException as ex:
    print("❌ Google Ads API hatası:")
    for error in ex.failure.errors:
        print(f"   Kod    : {error.error_code}")
        print(f"   Mesaj  : {error.message}")
        if error.location:
            for fv in error.location.field_path_elements:
                print(f"   Alan   : {fv.field_name}")
    print()
    print("İPUCU: Keyword zaten ekli olabilir → duplicate hatası normaldir.")

except Exception as e:
    print(f"❌ Beklenmeyen hata: {e}")
