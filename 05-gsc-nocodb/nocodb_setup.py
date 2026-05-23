"""
NocoDB Setup Script
===================
GSC pipeline için NocoDB base ve tablolarını ilk kez oluşturur.
Tek seferlik çalıştır.

Kullanım:
    python nocodb_setup.py --base "Botfusions SEO"
    python nocodb_setup.py --base "HorecaMark SEO"
    python nocodb_setup.py --list          # mevcut base'leri göster
"""

import os
import sys
import argparse
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

BASE_URL   = os.getenv("NOCODB_BASE_URL", "https://nocodb.turklawai.com").rstrip("/")
API_TOKEN  = os.getenv("NOCODB_API_TOKEN", "")
HEADERS    = {"xc-token": API_TOKEN, "Content-Type": "application/json"}


SCHEMAS = {
    "gsc_keywords": [
        {"title": "client",            "uidt": "SingleLineText"},
        {"title": "date_fetched",      "uidt": "Date"},
        {"title": "period_days",       "uidt": "Number"},
        {"title": "keyword",           "uidt": "SingleLineText"},
        {"title": "clicks",            "uidt": "Number"},
        {"title": "impressions",       "uidt": "Number"},
        {"title": "ctr",               "uidt": "Decimal"},
        {"title": "position",          "uidt": "Decimal"},
        {"title": "intent",            "uidt": "SingleLineText"},
        {"title": "opportunity_score", "uidt": "Decimal"},
        {"title": "priority",          "uidt": "SingleLineText"},
    ],
    "gsc_pages": [
        {"title": "client",       "uidt": "SingleLineText"},
        {"title": "date_fetched", "uidt": "Date"},
        {"title": "period_days",  "uidt": "Number"},
        {"title": "url",          "uidt": "URL"},
        {"title": "clicks",       "uidt": "Number"},
        {"title": "impressions",  "uidt": "Number"},
        {"title": "ctr",          "uidt": "Decimal"},
        {"title": "avg_position", "uidt": "Decimal"},
        {"title": "missed_clicks","uidt": "Number"},
        {"title": "priority",     "uidt": "SingleLineText"},
    ],
    "gsc_trends": [
        {"title": "client",             "uidt": "SingleLineText"},
        {"title": "date_fetched",       "uidt": "Date"},
        {"title": "query",              "uidt": "SingleLineText"},
        {"title": "recent_impressions", "uidt": "Number"},
        {"title": "prev_impressions",   "uidt": "Number"},
        {"title": "change_pct",         "uidt": "Decimal"},
        {"title": "clicks",             "uidt": "Number"},
        {"title": "position",           "uidt": "Decimal"},
    ],
    "gsc_summary": [
        {"title": "client",            "uidt": "SingleLineText"},
        {"title": "date_fetched",      "uidt": "Date"},
        {"title": "period_days",       "uidt": "Number"},
        {"title": "total_clicks",      "uidt": "Number"},
        {"title": "total_impressions", "uidt": "Number"},
        {"title": "avg_ctr",           "uidt": "Decimal"},
        {"title": "avg_position",      "uidt": "Decimal"},
        {"title": "quick_wins",        "uidt": "Number"},
        {"title": "low_ctr_pages",     "uidt": "Number"},
        {"title": "trending_queries",  "uidt": "Number"},
        {"title": "notes",             "uidt": "LongText"},
    ],
}


def list_bases():
    r = requests.get(f"{BASE_URL}/api/v1/db/meta/projects/", headers=HEADERS)
    r.raise_for_status()
    bases = r.json().get("list", [])
    if not bases:
        print("Henüz base yok.")
        return
    print(f"\n{'Base Adı':<30} {'ID'}")
    print("─" * 55)
    for b in bases:
        print(f"{b['title']:<30} {b['id']}")


def create_base(name: str) -> str:
    """Base oluştur, ID döndür"""
    r = requests.post(
        f"{BASE_URL}/api/v1/db/meta/projects/",
        headers=HEADERS,
        json={"title": name}
    )
    r.raise_for_status()
    base_id = r.json()["id"]
    print(f"✓ Base oluşturuldu: {name} (ID: {base_id})")
    return base_id


def get_base_id(name: str):
    r = requests.get(f"{BASE_URL}/api/v1/db/meta/projects/", headers=HEADERS)
    r.raise_for_status()
    for b in r.json().get("list", []):
        if b["title"] == name:
            return b["id"]
    return None


def setup_tables(base_id: str):
    """4 tabloyu oluştur"""
    r = requests.get(f"{BASE_URL}/api/v1/db/meta/projects/{base_id}/tables", headers=HEADERS)
    r.raise_for_status()
    existing = {t["title"] for t in r.json().get("list", [])}

    for table_name, columns in SCHEMAS.items():
        if table_name in existing:
            print(f"  · Zaten mevcut: {table_name}")
            continue
        payload = {"title": table_name, "columns": columns}
        cr = requests.post(
            f"{BASE_URL}/api/v1/db/meta/projects/{base_id}/tables",
            headers=HEADERS,
            json=payload
        )
        cr.raise_for_status()
        print(f"  ✓ Oluşturuldu: {table_name}")


def main():
    parser = argparse.ArgumentParser(description="NocoDB GSC Setup")
    parser.add_argument("--base",   help="Base adı (ör: 'Botfusions SEO')")
    parser.add_argument("--list",   action="store_true", help="Mevcut base'leri listele")
    parser.add_argument("--create", action="store_true", help="Base yoksa oluştur")
    args = parser.parse_args()

    if not API_TOKEN:
        print("❌ NOCODB_API_TOKEN bulunamadı. .env dosyasını kontrol et.")
        sys.exit(1)

    if args.list:
        list_bases()
        return

    if not args.base:
        parser.print_help()
        return

    print(f"\n🔧 NocoDB Setup: {args.base}")
    print(f"   URL: {BASE_URL}")

    base_id = get_base_id(args.base)

    if not base_id:
        if args.create:
            base_id = create_base(args.base)
        else:
            print(f"❌ Base bulunamadı: '{args.base}'")
            print("   --create flag'i ile otomatik oluştur.")
            sys.exit(1)
    else:
        print(f"✓ Base bulundu: {args.base} (ID: {base_id})")

    print(f"\n📋 Tablolar oluşturuluyor...")
    setup_tables(base_id)

    print(f"\n✅ Setup tamamlandı!")
    print(f"\nArtık pipeline'ı çalıştırabilirsin:")
    print(f"  python gsc_nocodb_pipeline.py --client botfusions --days 30 --report")


if __name__ == "__main__":
    main()
