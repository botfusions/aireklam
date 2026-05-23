"""
5 Mayıs 2026 — Arama Terimi Analizinden Yeni Negatif Keywordler
Botfusions - Website traffic-Search-1 kampanyası

Bu script SADECE daha önce eklenmemiş yeni terimleri ekler.
Çalıştır: uv run python add_negative_keywords_mayo5.py
"""
import warnings
warnings.filterwarnings("ignore")

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
import os

YAML_PATH = os.path.expanduser("~/google-ads.yaml")
CUSTOMER_ID = "3646875139"
CAMPAIGN_ID = "23657484697"  # Website traffic-Search-1

# (keyword_text, match_type)
# BROAD = genel türevleri de keser | EXACT = sadece tam eşleşme
NEW_NEGATIVE_KEYWORDS = [
    # Genel pazarlama arayanlar (bugünkü analiz - EXACT)
    ("marketing my product",              "EXACT"),
    ("marketing strategy for new product","EXACT"),
    ("promote your business",             "EXACT"),
    ("online marketing specialists",      "EXACT"),

    # Yanlış yazım / araç arayanlar (EXACT)
    ("chat cpt",                          "EXACT"),
    ("keywords",                          "EXACT"),

    # Genel yapay zeka arayanlar (BROAD — türevleri de keser)
    ("llm",                               "BROAD"),

    # Genel AI (dikkatli - PHRASE olarak ekliyoruz, "AI GEO" gibi şeyleri kesmez)
    ("ai tools",                          "EXACT"),
    ("ai platform",                       "EXACT"),
]

print("=" * 60)
print("5 Mayıs 2026 — Yeni Negatif Keyword Ekleme")
print("=" * 60)
print(f"Kampanya ID : {CAMPAIGN_ID}")
print(f"Eklenecek keyword sayısı: {len(NEW_NEGATIVE_KEYWORDS)}")
print()

client = GoogleAdsClient.load_from_storage(YAML_PATH)
svc = client.get_service("CampaignCriterionService")
campaign_svc = client.get_service("CampaignService")

match_type_map = {
    "EXACT": client.enums.KeywordMatchTypeEnum.EXACT,
    "PHRASE": client.enums.KeywordMatchTypeEnum.PHRASE,
    "BROAD": client.enums.KeywordMatchTypeEnum.BROAD,
}

operations = []
for kw_text, match_type in NEW_NEGATIVE_KEYWORDS:
    op = client.get_type("CampaignCriterionOperation")
    criterion = op.create
    criterion.campaign = campaign_svc.campaign_path(CUSTOMER_ID, CAMPAIGN_ID)
    criterion.negative = True
    criterion.keyword.text = kw_text
    criterion.keyword.match_type = match_type_map[match_type]
    operations.append(op)

try:
    response = svc.mutate_campaign_criteria(
        customer_id=CUSTOMER_ID,
        operations=operations,
    )
    print(f"✅ {len(response.results)} negatif keyword başarıyla eklendi:\n")
    for i, result in enumerate(response.results):
        kw, mt = NEW_NEGATIVE_KEYWORDS[i]
        print(f"  🚫 [{mt}] {kw}")
    print()
    print("✅ Tamamlandı! Toplam negatif keyword sayısı: ~33")
    print("   Bu terimlerden gelen bütçe israfı durduruldu.")
except GoogleAdsException as ex:
    print("❌ Google Ads API hatası:")
    for error in ex.failure.errors:
        print(f"  Hata: {error.message}")
        if error.location:
            for fv in error.location.field_path_elements:
                print(f"  Alan: {fv.field_name} (index: {fv.index})")
except Exception as e:
    print(f"❌ Beklenmedik hata: {e}")
