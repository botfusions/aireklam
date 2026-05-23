"""
HATA-002 — RARELY_SERVED Keywords Duraklatma
Botfusions - Website traffic-Search-1 kampanyası
Çalıştır: uv run python pause_rarely_served_keywords.py
"""
import warnings
warnings.filterwarnings("ignore")

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.api_core import protobuf_helpers
import os

# Config
YAML_PATH = os.path.expanduser("~/google-ads.yaml")
CUSTOMER_ID = "3646875139"
AD_GROUP_ID = "194542382375"

# Duraklatılacak keywordler (criterion_id: isim)
CRITERIA = {
    2471707131033: "KOBİ dijital görünürlük (Geniş)",
    2471707132313: "marka AI görünürlüğü (Geniş)",
    2471707319513: "AI aramalarda görünme (Geniş)",
    2471707323833: "AI görünürlük artırma (Geniş)",
    2471707323993: "ChatGPT'de görünürlük (Geniş)",
    2471707324273: "Perplexity görünürlük (Geniş)",
    2472938243885: "KOBİ dijital görünürlük (Sıralı)",
}

print("=" * 50)
print("HATA-002 — Pasif Keyword Duraklatma")
print("=" * 50)
print(f"Hesap: {CUSTOMER_ID}")
print(f"Reklam Grubu: {AD_GROUP_ID}")
print(f"Duraklatılacak keyword sayısı: {len(CRITERIA)}")
print()

client = GoogleAdsClient.load_from_storage(YAML_PATH)
svc = client.get_service("AdGroupCriterionService")

operations = []
for criterion_id in CRITERIA:
    op = client.get_type("AdGroupCriterionOperation")
    c = op.update
    c.resource_name = svc.ad_group_criterion_path(CUSTOMER_ID, AD_GROUP_ID, criterion_id)
    c.status = client.enums.AdGroupCriterionStatusEnum.PAUSED
    client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, c._pb))
    operations.append(op)

try:
    response = svc.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=operations)
    print(f"✅ {len(response.results)} keyword başarıyla duraklatıldı:\n")
    for result in response.results:
        cid = int(result.resource_name.split("~")[1])
        print(f"  ⏸️  {CRITERIA.get(cid, cid)}")
    print("\n✅ HATA-002 tamamlandı!")
except GoogleAdsException as ex:
    print("❌ Google Ads API hatası:")
    for error in ex.failure.errors:
        print(f"  {error.message}")
except Exception as e:
    print(f"❌ Hata: {e}")
