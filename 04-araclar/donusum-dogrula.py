# -*- coding: utf-8 -*-
"""Donusum takibi dogrulama — Google Ads REST API (gRPC SSL bypass).

Kullanim: python 04-araclar/donusum-dogrula.py
Conversion action listesi + son 30 gun donusum verisi raporlar.
"""
import json
import sys
from pathlib import Path

import httpx
import yaml
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

ROOT = Path(__file__).resolve().parent.parent
YAML_PATH = ROOT / "04-araclar" / "google_ads_mcp" / "google-ads.yaml"
CID = "3646875139"


def get_token():
    cfg = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8"))
    creds = Credentials(
        token=None,
        refresh_token=cfg["refresh_token"],
        client_id=cfg["client_id"],
        client_secret=cfg["client_secret"],
        token_uri="https://oauth2.googleapis.com/token",
    )
    creds.refresh(Request())
    return creds.token, cfg["developer_token"], str(cfg.get("login_customer_id", CID))


def search(query, token, dev_token, login_cid):
    url = f"https://googleads.googleapis.com/v24/customers/{CID}/googleAds:searchStream"
    headers = {
        "Authorization": f"Bearer {token}",
        "developer-token": dev_token,
        "login-customer-id": login_cid,
        "Content-Type": "application/json",
    }
    resp = httpx.post(url, headers=headers, json={"query": query}, timeout=60)
    if resp.status_code != 200:
        raise RuntimeError(f"API hata {resp.status_code}: {resp.text[:400]}")
    rows = []
    for batch in resp.json():
        rows.extend(batch.get("results", []))
    return rows


def main():
    token, dev, login_cid = get_token()
    print("=== 1. CONVERSION ACTION TANIMLARI ===")
    rows = search("""
        SELECT conversion_action.id, conversion_action.name,
               conversion_action.status, conversion_action.type,
               conversion_action.primary_for_goal,
               conversion_action.include_in_conversions_metric
        FROM conversion_action
        WHERE conversion_action.status = 'ENABLED'
    """, token, dev, login_cid)
    for r in rows:
        ca = r.get("conversionAction", {})
        print(f"- {ca.get('name')} | tip: {ca.get('type')} | "
              f"primary: {ca.get('primaryForGoal')} | "
              f"conversions metriginde: {ca.get('includeInConversionsMetric')}")

    print("\n=== 2. SON 30 GUN — CONVERSION ACTION BAZLI ===")
    rows = search("""
        SELECT segments.conversion_action_name,
               metrics.all_conversions
        FROM customer
        WHERE segments.date DURING LAST_30_DAYS
    """, token, dev, login_cid)
    if not rows:
        print("(veri yok — son 30 gunde hic donusum kaydi olusmamis)")
    for r in rows:
        seg = r.get("segments", {})
        m = r.get("metrics", {})
        print(f"- {seg.get('conversionActionName')}: {m.get('allConversions')}")

    print("\n=== 3. SON 30 GUN — GENEL METRIKLER ===")
    rows = search("""
        SELECT metrics.cost_micros, metrics.clicks, metrics.impressions,
               metrics.conversions, metrics.all_conversions
        FROM customer
        WHERE segments.date DURING LAST_30_DAYS
    """, token, dev, login_cid)
    for r in rows:
        m = r.get("metrics", {})
        cost = int(m.get("costMicros", 0)) / 1e6
        print(f"Harcama: ${cost:.2f} | Tiklama: {m.get('clicks', 0)} | "
              f"Gosterim: {m.get('impressions', 0)} | "
              f"Donusum: {m.get('conversions', 0)} | Tum donusumler: {m.get('allConversions', 0)}")

    print("\n=== 4. KAMPANYA DURUMLARI ===")
    rows = search("""
        SELECT campaign.name, campaign.status, campaign_budget.amount_micros
        FROM campaign
        WHERE campaign.status != 'REMOVED'
    """, token, dev, login_cid)
    for r in rows:
        c = r.get("campaign", {})
        b = r.get("campaignBudget", {})
        budget = int(b.get("amountMicros", 0)) / 1e6
        print(f"- {c.get('name')} | {c.get('status')} | gunluk butce: ${budget:.2f}")


if __name__ == "__main__":
    main()
