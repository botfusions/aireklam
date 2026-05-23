"""
HATA-003 — Alakasız Arama Terimlerine Negatif Keyword Ekleme
Botfusions - Website traffic-Search-1 kampanyası
Çalıştır: uv run python add_negative_keywords.py
"""
import warnings
warnings.filterwarnings("ignore")

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
import os

YAML_PATH = os.path.expanduser("~/google-ads.yaml")
CUSTOMER_ID = "3646875139"
CAMPAIGN_ID = "23657484697"  # Website traffic-Search-1

# Negatif keyword listesi (Exact Match)
NEGATIVE_KEYWORDS = [
    # Önceki liste
    "chatbot",
    "funnel",
    "gpt",
    "seo nedir",
    "seo analyzer",
    "answer the public",
    "social media ads strategy",
    "way to advertise a product",
    "noxtools",
    "seobotx",
    "website ranking checker",
    "seo web sitesi",
    "ücretsiz seo",
    "seo değerlendirme",
    "aiseo",
    # Son 14 gün analizinden eklenenler (Mayıs 2026)
    "moz",
    "chat gbt",
    "chatgbt",
    "dropgpt",
    "dextergpt",
    "trysoro",
    "seo vs geo",
    "chat gpt",
    "chatgpt",
]

print("=" * 55)
print("HATA-003 — Negatif Keyword Ekleme")
print("=" * 55)
print(f"Kampanya ID : {CAMPAIGN_ID}")
print(f"Eklenecek negatif keyword sayısı: {len(NEGATIVE_KEYWORDS)}")
print()

client = GoogleAdsClient.load_from_storage(YAML_PATH)
svc = client.get_service("CampaignCriterionService")
campaign_svc = client.get_service("CampaignService")

operations = []
for kw in NEGATIVE_KEYWORDS:
    op = client.get_type("CampaignCriterionOperation")
    criterion = op.create
    criterion.campaign = campaign_svc.campaign_path(CUSTOMER_ID, CAMPAIGN_ID)
    criterion.negative = True
    criterion.keyword.text = kw
    criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
    operations.append(op)

try:
    response = svc.mutate_campaign_criteria(
        customer_id=CUSTOMER_ID,
        operations=operations,
    )
    print(f"✅ {len(response.results)} negatif keyword eklendi:\n")
    for i, result in enumerate(response.results):
        print(f"  🚫 [{NEGATIVE_KEYWORDS[i]}]")
    print("\n✅ HATA-003 adım 1 tamamlandı!")
    print("   Bütçeyi yiyen alakasız terimler artık reklam görmeyecek.")
except GoogleAdsException as ex:
    print("❌ Google Ads API hatası:")
    for error in ex.failure.errors:
        print(f"  {error.message}")
except Exception as e:
    print(f"❌ Hata: {e}")
