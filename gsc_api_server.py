"""
Botfusions CMO Dashboard — GSC API Sunucusu
==========================================
Google Search Console verilerini dashboard'a sunan lokal REST API.

Çalıştır : python gsc_api_server.py
Port     : http://localhost:8765
Dashboard: cmo-dashboard.html

Endpoints:
  GET /api/health              → Sunucu sağlık kontrolü
  GET /api/gsc/summary         → Toplam tıklama, gösterim, CTR, pozisyon
  GET /api/gsc/keywords        → Üst keyword'lar (sıralama, tıklama, gösterim)
  GET /api/gsc/quickwins       → 11-20 arası fırsat keyword'ları
  GET /api/gsc/pages           → En çok trafik alan sayfalar
"""

import os
import sys
import json
import logging
import ipaddress
from urllib.parse import urlparse
from pathlib import Path
from datetime import datetime
from flask import Flask, jsonify, request

# ── Modül yollarını ayarla ──────────────────────────
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "04-araclar" / "seo-machine-modules" / "modules"))
sys.path.insert(0, str(ROOT / "05-gsc-nocodb"))

# .env dosyasını yükle
try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / "05-gsc-nocodb" / ".env")
    load_dotenv(ROOT / "secrets.env")      # Merkezi secret dosyasi
except ImportError:
    pass

# ── Config ─────────────────────────────────────────
SITE_URL = os.getenv("GSC_SITE_URL", "https://botfusions.com")
PORT     = int(os.getenv("CMO_SERVER_PORT", 8765))
HOST     = "127.0.0.1"

# ── Logging ────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [GSC] %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger(__name__)

# ── Flask App ──────────────────────────────────────
app = Flask(__name__)

# ── CORS — sadece bilinen originlere izin ver ──
ALLOWED_ORIGINS = [
    "http://localhost:8765",
    "http://127.0.0.1:8765",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "null",   # file:// ile acilan dashboard'lar icin
]

@app.after_request
def add_cors(response):
    origin = request.headers.get("Origin", "")
    if origin in ALLOWED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, X-CMO-Key"
    return response

# ── Auth — state-changing endpoint'ler icin API key zorunlu ──
CMO_API_KEY = os.getenv("CMO_API_KEY", "")

def require_auth():
    """POST endpoint'lerde CMO_API_KEY zorunlu. GET endpoint'ler serbest."""
    if request.method != "POST":
        return None
    if not CMO_API_KEY:
        return None   # Anahtar yoksa auth kapali (geri uyumlu)
    key = request.headers.get("X-CMO-Key") or (request.get_json() or {}).get("api_key")
    if key != CMO_API_KEY:
        return jsonify({"error": "Yetkisiz. X-CMO-Key header gerekli."}), 401
    return None

@app.before_request
def auth_check():
    if request.method == "OPTIONS":
        return "", 204
    return require_auth()

# ── SSRF Korumasi ──────────────────────────────────
def validate_url(url):
    """URL'nin guvenli oldugunu dogrula: scheme, private IP, allowlist."""
    try:
        parsed = urlparse(url)
    except Exception:
        return False, "Gecersiz URL formati"

    if parsed.scheme not in ("http", "https"):
        return False, "Yalnizca http/https scheme desteklenir"

    hostname = parsed.hostname
    if not hostname:
        return False, "Hostname bulunamadi"

    # Private IP engelleme
    try:
        import socket
        resolved = socket.gethostbyname(hostname)
        ip = ipaddress.ip_address(resolved)
        if ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_link_local:
            return False, f"Private/internal IP adresi engellendi: {resolved}"
    except (socket.gaierror, ValueError):
        pass  # Cozulemeyen hostname'ye izin ver (CDN, vb.)

    # Yasakli hostname'ler
    blocked = ("localhost", "127.0.0.1", "0.0.0.0", "::1", "metadata.google.internal")
    if hostname.lower() in blocked:
        return False, f"Yasakli hostname: {hostname}"

    return True, "OK"

# ── GSC Bağlantısı (lazy) ─────────────────────────
_gsc = None

def get_gsc():
    global _gsc
    if _gsc is None:
        from google_search_console import GoogleSearchConsole
        _gsc = GoogleSearchConsole(site_url=SITE_URL)
        log.info(f"GSC bağlandı → {SITE_URL}")
    return _gsc


# ────────────────────────────────────────────────────
#  ENDPOINTS
# ────────────────────────────────────────────────────

@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "site": SITE_URL,
        "server_time": datetime.now().isoformat(),
        "version": "1.0.0"
    })


@app.route("/api/gsc/summary")
def gsc_summary():
    """
    Toplam metrikler: tıklama, gösterim, ort. CTR, ort. pozisyon
    """
    days  = int(request.args.get("days", 28))
    try:
        gsc = get_gsc()
        keywords = gsc.get_keyword_positions(days=days, limit=1000)

        total_clicks      = sum(k["clicks"]      for k in keywords)
        total_impressions = sum(k["impressions"]  for k in keywords)
        avg_ctr           = (total_clicks / total_impressions * 100) if total_impressions else 0
        avg_position      = (sum(k["position"] for k in keywords) / len(keywords)) if keywords else 0

        return jsonify({
            "ok": True,
            "days": days,
            "site": SITE_URL,
            "fetched_at": datetime.now().isoformat(),
            "summary": {
                "total_clicks":      int(total_clicks),
                "total_impressions":  int(total_impressions),
                "avg_ctr":           round(avg_ctr, 2),
                "avg_position":       round(avg_position, 1),
                "total_keywords":     len(keywords),
            }
        })
    except Exception as e:
        log.error(f"summary hatası: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/gsc/keywords")
def gsc_keywords():
    """
    Üst keyword'lar — tıklama, gösterim, sıra
    """
    days  = int(request.args.get("days",  28))
    limit = int(request.args.get("limit", 20))

    try:
        gsc      = get_gsc()
        keywords = gsc.get_keyword_positions(days=days, limit=500)

        # Tıklamaya göre sırala, limit uygula
        top = sorted(keywords, key=lambda x: x["clicks"], reverse=True)[:limit]

        return jsonify({
            "ok":         True,
            "days":       days,
            "fetched_at": datetime.now().isoformat(),
            "count":      len(top),
            "keywords":   top
        })
    except Exception as e:
        log.error(f"keywords hatası: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/gsc/quickwins")
def gsc_quickwins():
    """
    Quick win fırsatları — pozisyon 11-20, yüksek gösterim
    """
    days = int(request.args.get("days", 28))

    try:
        gsc  = get_gsc()
        wins = gsc.get_quick_wins(
            days=days,
            position_min=11,
            position_max=20,
            min_impressions=30,
            prioritize_commercial=True
        )

        return jsonify({
            "ok":         True,
            "days":       days,
            "fetched_at": datetime.now().isoformat(),
            "count":      len(wins),
            "quickwins":  wins[:15]
        })
    except Exception as e:
        log.error(f"quickwins hatası: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/gsc/pages")
def gsc_pages():
    """
    En çok trafik alan sayfalar
    """
    days  = int(request.args.get("days",  28))
    limit = int(request.args.get("limit", 10))

    try:
        from datetime import timedelta
        from googleapiclient.discovery import build

        gsc = get_gsc()
        start = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        end   = datetime.now().strftime("%Y-%m-%d")

        resp = gsc.service.searchanalytics().query(
            siteUrl=SITE_URL,
            body={
                "startDate":  start,
                "endDate":    end,
                "dimensions": ["page"],
                "rowLimit":   limit,
            }
        ).execute()

        pages = []
        for row in resp.get("rows", []):
            pages.append({
                "page":        row["keys"][0],
                "clicks":      int(row["clicks"]),
                "impressions": int(row["impressions"]),
                "ctr":         round(row["ctr"] * 100, 2),
                "position":    round(row["position"], 1),
            })

        return jsonify({
            "ok":         True,
            "days":       days,
            "fetched_at": datetime.now().isoformat(),
            "count":      len(pages),
            "pages":      pages
        })
    except Exception as e:
        log.error(f"pages hatası: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/gsc/all")
def gsc_all():
    """
    Dashboard için tüm verileri tek sorguda döndür (network optimizasyonu)
    """
    days = int(request.args.get("days", 28))

    try:
        gsc      = get_gsc()
        keywords = gsc.get_keyword_positions(days=days, limit=500)
        wins     = gsc.get_quick_wins(days=days, min_impressions=30)

        total_clicks      = sum(k["clicks"]     for k in keywords)
        total_impressions = sum(k["impressions"] for k in keywords)
        avg_ctr           = (total_clicks / total_impressions * 100) if total_impressions else 0
        avg_position      = (sum(k["position"]  for k in keywords) / len(keywords)) if keywords else 0

        top_keywords = sorted(keywords, key=lambda x: x["clicks"], reverse=True)[:20]

        # Sayfalar
        from datetime import timedelta
        start = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        end   = datetime.now().strftime("%Y-%m-%d")
        page_resp = gsc.service.searchanalytics().query(
            siteUrl=SITE_URL,
            body={"startDate": start, "endDate": end, "dimensions": ["page"], "rowLimit": 10}
        ).execute()
        pages = [
            {
                "page":        r["keys"][0].replace(SITE_URL, ""),
                "clicks":      int(r["clicks"]),
                "impressions": int(r["impressions"]),
                "ctr":         round(r["ctr"] * 100, 2),
                "position":    round(r["position"], 1),
            }
            for r in page_resp.get("rows", [])
        ]

        return jsonify({
            "ok":         True,
            "days":       days,
            "fetched_at": datetime.now().isoformat(),
            "site":       SITE_URL,
            "summary": {
                "total_clicks":      int(total_clicks),
                "total_impressions": int(total_impressions),
                "avg_ctr":           round(avg_ctr, 2),
                "avg_position":      round(avg_position, 1),
                "total_keywords":    len(keywords),
            },
            "top_keywords": top_keywords,
            "quickwins":    wins[:10],
            "top_pages":    pages,
        })

    except Exception as e:
        log.error(f"all hatası: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


# ══════════════════════════════════════════════════
# OmniSocials + Supabase Proxy Endpoints
# Browser CORS sorununu aşmak için lokal proxy
#
# NOT: OmniSocials yalnızca yayın (publishing) API'sidir.
#      GET /posts endpoint'i YOKTUR — 403 verir.
#      Post listesi → Supabase'den çekilir.
#      Hesap listesi → OmniSocials GET /accounts (var).
#      Medya listesi → Supabase media_library tablosundan.
# ══════════════════════════════════════════════════
try:
    import requests as req_lib
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "--break-system-packages", "-q"])
    import requests as req_lib

OMNI_KEY  = os.getenv("OMNISOCIALS_API_KEY", "")
if not OMNI_KEY:
    log.warning("OMNISOCIALS_API_KEY bulunamadi. Sosyal medya endpoint'leri calismaz.")
OMNI_BASE = "https://api.omnisocials.com/v1"

SUPA_URL  = os.getenv("SUPABASE_URL", "https://supabase.turklawai.com")
SUPA_KEY  = os.getenv("SUPABASE_ANON_KEY", "")
if not SUPA_KEY:
    log.warning("SUPABASE_ANON_KEY bulunamadi. Supabase endpoint'leri calismaz.")

def omni_get(path):
    """OmniSocials API — yalnızca mevcut endpoint'ler için kullan."""
    url = f"{OMNI_BASE}{path}"
    r = req_lib.get(url, headers={"Authorization": f"Bearer {OMNI_KEY}"}, timeout=10)
    r.raise_for_status()
    return r.json()

def supabase_get(table, params=None):
    """Supabase REST API'den veri çek."""
    url = f"{SUPA_URL}/rest/v1/{table}"
    headers = {
        "Authorization": f"Bearer {SUPA_KEY}",
        "apikey": SUPA_KEY,
        "Accept": "application/json",
    }
    r = req_lib.get(url, headers=headers, params=params or {}, timeout=10)
    r.raise_for_status()
    return r.json()


@app.route("/api/omni/posts")
def omni_posts():
    """Post listesini Supabase social_posts tablosundan çeker.
    OmniSocials GET /posts endpoint'i yoktur (publishing-only API)."""
    try:
        limit = request.args.get("limit", "20")
        data = supabase_get("social_posts", {
            "order": "created_at.desc",
            "limit": limit,
            "select": "id,omnisocials_post_id,caption,platforms,post_type,status,published_at,campaign,created_at"
        })
        return jsonify({"posts": data, "source": "supabase"})
    except Exception as e:
        log.warning(f"Supabase post sorgusu başarısız: {e}")
        return jsonify({"posts": [], "source": "supabase", "error": str(e)})


@app.route("/api/omni/media")
def omni_media():
    """Medya listesini Supabase media_library tablosundan çeker."""
    try:
        limit = request.args.get("limit", "20")
        data = supabase_get("media_library", {
            "order": "created_at.desc",
            "limit": limit,
            "select": "id,filename,type,mime_type,size_bytes,public_url,omnisocials_id,campaign,created_at"
        })
        return jsonify({"media": data, "source": "supabase"})
    except Exception as e:
        log.warning(f"Supabase medya sorgusu başarısız: {e}")
        return jsonify({"media": [], "source": "supabase", "error": str(e)})


@app.route("/api/omni/accounts")
def omni_accounts():
    """Bağlı hesapları OmniSocials GET /accounts'tan çeker, hata olursa statik fallback."""
    try:
        data = omni_get("/accounts")
        return jsonify(data)
    except Exception as e:
        log.warning(f"OmniSocials accounts hatası: {e}")
        return jsonify({"accounts": [
            {"id": "881407_instagram", "platform": "instagram", "username": "@botfusions"},
            {"id": "881407_facebook",  "platform": "facebook",  "username": "Ömer Tokgöz"},
            {"id": "881407_youtube",   "platform": "youtube",   "username": "@botfusionss"},
            {"id": "881407_tiktok",    "platform": "tiktok",    "username": "@botfusions"},
            {"id": "881407_pinterest", "platform": "pinterest", "username": "cenk0342"},
            {"id": "881407_x",         "platform": "x",         "username": "@botfusionss"},
        ], "source": "static_fallback"})


# ══════════════════════════════════════════════════
# Yayın Endpoint'leri — 2 Çağrı Sistemi
# Grup A: Video → Instagram, Facebook, YouTube, TikTok
# Grup B: Görsel → X, LinkedIn, Pinterest, Instagram feed, Facebook feed
# ══════════════════════════════════════════════════

def omni_post(payload):
    """OmniSocials'a POST isteği gönder."""
    r = req_lib.post(
        f"{OMNI_BASE}/posts/create-and-publish",
        headers={"Authorization": f"Bearer {OMNI_KEY}", "Content-Type": "application/json"},
        json=payload,
        timeout=30
    )
    r.raise_for_status()
    return r.json()

def supabase_insert(table, data):
    """Supabase tablosuna kayıt ekle."""
    headers = {
        "Authorization": f"Bearer {SUPA_KEY}",
        "apikey": SUPA_KEY,
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    r = req_lib.post(f"{SUPA_URL}/rest/v1/{table}", headers=headers, json=data, timeout=10)
    r.raise_for_status()
    return {"ok": True}


@app.route("/api/publish/video", methods=["POST", "OPTIONS"])
def publish_video():
    """Grup A: Video → Instagram Reel + Facebook Reel + YouTube Shorts + TikTok"""
    if request.method == "OPTIONS":
        return jsonify({}), 200
    try:
        body = request.get_json()
        payload = {
            "content": {
                "default":  body.get("text_default", ""),
                "youtube":  body.get("text_youtube", body.get("text_default", "")),
            },
            "accounts": [
                "881407_instagram",
                "881407_facebook",
                "881407_youtube",
                "881407_tiktok",
            ],
            "media_urls": {"default": [body["video_url"]]},
        }
        if body.get("youtube_title"):
            payload["youtube_title"] = body["youtube_title"]
        if body.get("scheduled_at"):
            payload["schedule_at"] = body["scheduled_at"]

        result = omni_post(payload)
        post_id = result.get("data", {}).get("id") or result.get("id")

        # Supabase log
        try:
            supabase_insert("social_posts", {
                "omnisocials_post_id": str(post_id),
                "caption": body.get("text_default", ""),
                "platforms": ["instagram", "facebook", "youtube", "tiktok"],
                "post_type": "reel",
                "status": "posting",
                "campaign": body.get("campaign", ""),
                "youtube_title": body.get("youtube_title", ""),
            })
        except Exception as db_err:
            log.warning(f"Supabase log hatası: {db_err}")

        return jsonify({"ok": True, "post_id": post_id, "group": "video", "result": result})
    except Exception as e:
        log.error(f"Video yayın hatası: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/publish/image", methods=["POST", "OPTIONS"])
def publish_image():
    """Grup B: Görsel → X + LinkedIn + Pinterest + Instagram feed + Facebook feed"""
    if request.method == "OPTIONS":
        return jsonify({}), 200
    try:
        body = request.get_json()
        accounts = ["881407_x", "881407_instagram", "881407_facebook"]
        if body.get("include_linkedin", True):
            accounts.append("881407_linkedin")
        if body.get("include_pinterest", True):
            accounts.append("881407_pinterest")

        payload = {
            "content": {
                "default":   body.get("text_default", ""),
                "x":         body.get("text_x", "")[:280],
                "linkedin":  body.get("text_linkedin", body.get("text_default", "")),
                "pinterest": body.get("text_pinterest", body.get("text_default", ""))[:500],
            },
            "accounts": accounts,
            "media_urls": {"default": [body["image_url"]]},
        }
        if body.get("pinterest_board_id"):
            payload["pinterest_board_id"] = body["pinterest_board_id"]
        if body.get("image_url_pinterest"):
            payload["media_urls"]["pinterest"] = [body["image_url_pinterest"]]
        if body.get("scheduled_at"):
            payload["schedule_at"] = body["scheduled_at"]

        result = omni_post(payload)
        post_id = result.get("data", {}).get("id") or result.get("id")

        try:
            supabase_insert("social_posts", {
                "omnisocials_post_id": str(post_id),
                "caption": body.get("text_x") or body.get("text_default", ""),
                "platforms": accounts,
                "post_type": "post",
                "status": "posting",
                "campaign": body.get("campaign", ""),
            })
        except Exception as db_err:
            log.warning(f"Supabase log hatası: {db_err}")

        return jsonify({"ok": True, "post_id": post_id, "group": "image", "result": result})
    except Exception as e:
        log.error(f"Görsel yayın hatası: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/publish/full", methods=["POST", "OPTIONS"])
def publish_full():
    """Hem video hem görsel — iki çağrıyı birden tetikler."""
    if request.method == "OPTIONS":
        return jsonify({}), 200
    try:
        body = request.get_json()
        results = {}
        errors  = {}

        if body.get("video_url"):
            try:
                rv = req_lib.post(
                    "http://localhost:8765/api/publish/video",
                    json=body, timeout=35
                )
                results["video"] = rv.json()
            except Exception as e:
                errors["video"] = str(e)

        if body.get("image_url"):
            try:
                ri = req_lib.post(
                    "http://localhost:8765/api/publish/image",
                    json=body, timeout=35
                )
                results["image"] = ri.json()
            except Exception as e:
                errors["image"] = str(e)

        return jsonify({"ok": not errors, "results": results, "errors": errors})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ══════════════════════════════════════════════════
# GEO ANALİZ — bofusions_geo_mcp Entegrasyonu
# Lokal MCP paketi: GEO analiz_mcp/src/bofusions_geo_mcp
# ══════════════════════════════════════════════════
import asyncio as _asyncio
import sys as _sys
from pathlib import Path as _Path

# GEO MCP kaynak klasörünü sys.path'e ekle
_GEO_SRC = _Path(__file__).parent.parent / "GEO analiz_mcp" / "src"
if not _GEO_SRC.exists():
    _GEO_SRC = _Path(r"C:/Users/user/Downloads/Z.ai_claude code/GEO analiz_mcp/src")
if _GEO_SRC.exists() and str(_GEO_SRC) not in _sys.path:
    _sys.path.insert(0, str(_GEO_SRC))
    log.info(f"GEO MCP yüklendi -> {_GEO_SRC}")
else:
    log.warning(f"GEO MCP bulunamadi: {_GEO_SRC}")


async def _run_geo_scan(url: str, brand: str) -> dict:
    """bofusions_geo_mcp araçlarını çalıştır — tam GEO analizi."""
    from bofusions_geo_mcp.client import fetch_page, fetch_robots_txt, fetch_llms_txt
    from bofusions_geo_mcp.parser import extract_content_blocks
    from bofusions_geo_mcp.scoring import score_passage, calculate_geo_score
    from html import escape

    page   = await fetch_page(url)
    robots = await fetch_robots_txt(url)
    llms   = await fetch_llms_txt(url)

    # ── Citability skorla ──────────────────────
    citability_scores = []
    if page.get("text_content"):
        html_mock = (
            "".join(f"<h{h['level']}>{escape(h['text'])}</h{h['level']}>"
                    for h in page.get("heading_structure", []))
            + f"<p>{escape(page['text_content'][:8000])}</p>"
        )
        for block in extract_content_blocks(html_mock):
            if block["word_count"] >= 20:
                sc = score_passage(block["content"], block["heading"])
                citability_scores.append(sc["total_score"])

    citability_avg = (sum(citability_scores) / len(citability_scores)
                      if citability_scores else 0)

    # ── Diğer skorlar ─────────────────────────
    schema_count = len(page.get("structured_data", []))
    schema_score = min(schema_count * 25, 100)

    tech_ded = 0
    if not page.get("has_ssr_content"): tech_ded += 20
    if not page.get("canonical"):       tech_ded += 10
    if not page.get("description"):     tech_ded += 10
    if len(page.get("h1_tags", [])) != 1: tech_ded += 10
    if not robots.get("exists"):        tech_ded += 15
    tech_score = max(100 - tech_ded, 0)

    llms_score = (50 if llms["llms_txt"]["exists"] else 0) + \
                 (50 if llms["llms_full_txt"]["exists"] else 0)

    geo = calculate_geo_score(
        citability_avg, 0, citability_avg,
        tech_score, schema_score, llms_score
    )

    # ── Bulgular ──────────────────────────────
    findings = []
    if not page.get("description"):
        findings.append({"level": "HIGH", "text": "Meta description eksik — AI snippet seçimini etkiler"})
    if not page.get("structured_data"):
        findings.append({"level": "HIGH", "text": "JSON-LD schema markup yok — AI keşfedilebilirliği düşük"})
    if not llms["llms_txt"]["exists"]:
        findings.append({"level": "HIGH", "text": "llms.txt dosyası yok — AI crawler yapıyı göremez"})
    if not page.get("has_ssr_content"):
        findings.append({"level": "HIGH", "text": "SSR/Pre-render yok — AI crawlerlar boş sayfa görür"})
    if not page.get("canonical"):
        findings.append({"level": "MEDIUM", "text": "Canonical URL tag eksik"})
    if len(page.get("h1_tags", [])) != 1:
        h1 = len(page.get("h1_tags", []))
        findings.append({"level": "MEDIUM", "text": f"H1 tag sorunu: {h1} adet (tam 1 olmalı)"})
    if citability_avg < 50:
        findings.append({"level": "MEDIUM", "text": f"Düşük citability skoru ({citability_avg:.0f}/100) — içerik yapılandırma gerekli"})

    crawler_status = robots.get("ai_crawler_status", {})
    blocked = [c for c, s in crawler_status.items() if "BLOCKED" in s]
    if blocked:
        findings.append({"level": "HIGH", "text": f"Engellenmiş AI crawler: {', '.join(blocked[:3])}"})

    return {
        "url":       url,
        "brand":     brand,
        "geo_score": round(geo["total_score"], 1),
        "grade":     geo["grade"],
        "components": {k: {"weight": v["weight"], "score": round(v["score"], 1), "weighted": round(v["weighted"], 1)}
                       for k, v in geo["components"].items()},
        "page": {
            "title":          page.get("title"),
            "description":    page.get("description"),
            "word_count":     page.get("word_count", 0),
            "h1_count":       len(page.get("h1_tags", [])),
            "schema_count":   schema_count,
            "has_ssr":        page.get("has_ssr_content", True),
            "canonical":      page.get("canonical"),
            "image_count":    len(page.get("images", [])),
            "internal_links": len(page.get("internal_links", [])),
        },
        "robots": {
            "exists":      robots.get("exists", False),
            "ai_crawlers": crawler_status,
        },
        "llms": {
            "llms_txt":      llms["llms_txt"]["exists"],
            "llms_full_txt": llms["llms_full_txt"]["exists"],
        },
        "scores": {
            "citability": round(citability_avg, 1),
            "technical":  round(tech_score, 1),
            "schema":     round(schema_score, 1),
            "llms":       round(llms_score, 1),
        },
        "citability_block_count": len(citability_scores),
        "findings":   findings,
        "scanned_at": datetime.now().isoformat(),
    }


@app.route("/api/geo/scan", methods=["POST", "OPTIONS"])
def geo_scan():
    """GEO tam analiz — bofusions_geo_mcp ile site tarar, Supabase'e kaydeder."""
    if request.method == "OPTIONS":
        return jsonify({}), 200
    try:
        body  = request.get_json() or {}
        url   = body.get("url",   "https://botfusions.com/geo-hizmet")
        brand = body.get("brand", "Botfusions")

        # URL normalize
        if not url.startswith("http"):
            url = "https://" + url

        # SSRF korumasi
        safe, msg = validate_url(url)
        if not safe:
            return jsonify({"error": f"URL gecersiz: {msg}"}), 400

        result = _asyncio.run(_run_geo_scan(url, brand))

        # Supabase'e kaydet
        try:
            supabase_insert("geo_scans", {
                "url":            result["url"],
                "brand":          result["brand"],
                "geo_score":      result["geo_score"],
                "grade":          result["grade"],
                "components":     result["components"],
                "scores":         result["scores"],
                "page_meta":      result["page"],
                "llms_txt":       result["llms"]["llms_txt"],
                "llms_full_txt":  result["llms"]["llms_full_txt"],
                "robots_exists":  result["robots"]["exists"],
                "findings":       result["findings"],
            })
            result["saved"] = True
        except Exception as db_err:
            log.warning(f"GEO scan Supabase hatası: {db_err}")
            result["saved"] = False

        return jsonify({"ok": True, **result})
    except Exception as e:
        log.error(f"GEO scan hatası: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/geo/history")
def geo_history():
    """Geçmiş GEO taramalarını Supabase'den getirir."""
    try:
        limit = request.args.get("limit", "10")
        data  = supabase_get("geo_scans", {
            "order":  "created_at.desc",
            "limit":  limit,
            "select": "id,url,brand,geo_score,grade,created_at",
        })
        return jsonify({"ok": True, "scans": data})
    except Exception as e:
        log.warning(f"GEO history hatası: {e}")
        return jsonify({"ok": True, "scans": [], "error": str(e)})


@app.route("/api/geo/latest")
def geo_latest():
    """Belirli bir URL için en son GEO taramasını getirir."""
    try:
        url  = request.args.get("url", "https://botfusions.com/geo-hizmet")
        data = supabase_get("geo_scans", {
            "url":    f"eq.{url}",
            "order":  "created_at.desc",
            "limit":  "1",
        })
        return jsonify({"ok": True, "scan": data[0] if data else None})
    except Exception as e:
        return jsonify({"ok": False, "scan": None, "error": str(e)})


# ══════════════════════════════════════════════════
# Google Ads — Gerçek veri endpoint'leri
# google-ads.yaml credentials ile Google Ads API'ye bağlanır
# ══════════════════════════════════════════════════

_GOOGLE_ADS_CLIENT = None
_GOOGLE_ADS_CID = os.getenv("GOOGLE_ADS_CUSTOMER_ID", "3646875139")


# gRPC/BoringSSL Windows'ta sertifika dogrulayamiyor (CERTIFICATE_VERIFY_FAILED) —
# bu yuzden tum Google Ads sorgulari REST API uzerinden calisir (bkz. google_ads_mcp/tools/api.py)
_ADS_YAML_PATH = str(ROOT / "04-araclar" / "google_ads_mcp" / "google-ads.yaml")
_ADS_REST_TOKEN = None
_ADS_REST_TOKEN_EXP = 0.0


def _ads_rest_search(query):
    """GAQL sorgusunu Google Ads REST API ile calistir, ham JSON satirlari dondur."""
    global _ADS_REST_TOKEN, _ADS_REST_TOKEN_EXP
    import time as _time
    import yaml as _yaml
    with open(_ADS_YAML_PATH, encoding="utf-8") as f:
        cfg = _yaml.safe_load(f)
    if not _ADS_REST_TOKEN or _time.time() > _ADS_REST_TOKEN_EXP:
        from google.oauth2.credentials import Credentials as _OAuthCreds
        from google.auth.transport.requests import Request as _AuthReq
        creds = _OAuthCreds(
            token=None,
            refresh_token=cfg["refresh_token"],
            client_id=cfg["client_id"],
            client_secret=cfg["client_secret"],
            token_uri="https://oauth2.googleapis.com/token",
        )
        creds.refresh(_AuthReq())
        _ADS_REST_TOKEN = creds.token
        _ADS_REST_TOKEN_EXP = _time.time() + 3000
    headers = {
        "Authorization": f"Bearer {_ADS_REST_TOKEN}",
        "developer-token": cfg["developer_token"],
        "login-customer-id": str(cfg.get("login_customer_id", _GOOGLE_ADS_CID)),
        "Content-Type": "application/json",
    }
    url = f"https://googleads.googleapis.com/v24/customers/{_GOOGLE_ADS_CID}/googleAds:searchStream"
    r = req_lib.post(url, headers=headers, json={"query": query}, timeout=60)
    if r.status_code != 200:
        raise RuntimeError(f"Ads REST API {r.status_code}: {r.text[:300]}")
    rows = []
    for batch in r.json():
        rows.extend(batch.get("results", []))
    return rows


def _num(x):
    """REST JSON'da int64/money alanlari string gelir — guvenli sayiya cevir."""
    try:
        return float(x or 0)
    except (TypeError, ValueError):
        return 0.0


@app.route("/api/google-ads/summary")
def google_ads_summary():
    """Google Ads kampanya özeti — son N gün."""
    try:
        from datetime import timedelta
        days = int(request.args.get("days", "30"))
        end = datetime.now().strftime("%Y-%m-%d")
        start = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        # Kampanya metrikleri
        q = f"""
            SELECT campaign.name, campaign.status, campaign.advertising_channel_type,
                   metrics.clicks, metrics.impressions, metrics.cost_micros,
                   metrics.ctr, metrics.average_cpc, metrics.conversions,
                   metrics.average_cpm
            FROM campaign
            WHERE segments.date BETWEEN '{start}' AND '{end}'
              AND campaign.status != 'REMOVED'
            ORDER BY metrics.cost_micros DESC
        """
        campaigns = []
        totals = {"spend": 0.0, "clicks": 0, "impressions": 0, "conversions": 0.0, "ctr_sum": 0.0, "ctr_count": 0}
        for row in _ads_rest_search(q):
            c, m = row.get("campaign", {}), row.get("metrics", {})
            cost = _num(m.get("costMicros")) / 1e6
            clicks = int(_num(m.get("clicks")))
            imps = int(_num(m.get("impressions")))
            ctr = _num(m.get("ctr"))
            camp = {
                "name": c.get("name"),
                "status": c.get("status"),
                "type": c.get("advertisingChannelType"),
                "spend": round(cost, 2),
                "clicks": clicks,
                "impressions": imps,
                "ctr": round(ctr * 100, 2),
                "cpc": round(_num(m.get("averageCpc")) / 1e6, 2),
                "conversions": round(_num(m.get("conversions")), 0),
            }
            campaigns.append(camp)
            totals["spend"] += cost
            totals["clicks"] += clicks
            totals["impressions"] += imps
            totals["conversions"] += _num(m.get("conversions"))
            if imps > 0:
                totals["ctr_sum"] += ctr * 100
                totals["ctr_count"] += 1

        totals["spend"] = round(totals["spend"], 2)
        totals["ctr_avg"] = round(totals["ctr_sum"] / totals["ctr_count"], 2) if totals["ctr_count"] else 0
        totals["cpc_avg"] = round(totals["spend"] / totals["clicks"], 2) if totals["clicks"] else 0

        # Keyword metrikleri (top 15)
        q_kw = f"""
            SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
                   metrics.clicks, metrics.impressions, metrics.cost_micros,
                   metrics.ctr, metrics.average_cpc, metrics.conversions
            FROM keyword_view
            WHERE segments.date BETWEEN '{start}' AND '{end}'
              AND metrics.impressions > 0
            ORDER BY metrics.cost_micros DESC
            LIMIT 15
        """
        keywords = []
        for row in _ads_rest_search(q_kw):
            kw, m = row.get("adGroupCriterion", {}).get("keyword", {}), row.get("metrics", {})
            keywords.append({
                "keyword": kw.get("text"),
                "match_type": kw.get("matchType"),
                "spend": round(_num(m.get("costMicros")) / 1e6, 2),
                "clicks": int(_num(m.get("clicks"))),
                "impressions": int(_num(m.get("impressions"))),
                "ctr": round(_num(m.get("ctr")) * 100, 2),
                "cpc": round(_num(m.get("averageCpc")) / 1e6, 2),
                "conversions": round(_num(m.get("conversions")), 0),
            })

        # Günlük trend (son 30 gün)
        q_daily = f"""
            SELECT segments.date, metrics.clicks, metrics.impressions, metrics.cost_micros
            FROM campaign
            WHERE segments.date BETWEEN '{start}' AND '{end}'
            ORDER BY segments.date
        """
        daily_map = {}
        for row in _ads_rest_search(q_daily):
            m = row.get("metrics", {})
            d = row.get("segments", {}).get("date")
            entry = daily_map.setdefault(d, {"date": d, "spend": 0.0, "clicks": 0, "impressions": 0})
            entry["spend"] = round(entry["spend"] + _num(m.get("costMicros")) / 1e6, 2)
            entry["clicks"] += int(_num(m.get("clicks")))
            entry["impressions"] += int(_num(m.get("impressions")))
        daily = sorted(daily_map.values(), key=lambda x: x["date"])

        return jsonify({
            "ok": True,
            "period": {"start": start, "end": end, "days": days},
            "totals": totals,
            "campaigns": campaigns,
            "keywords": keywords,
            "daily": daily,
        })
    except Exception as e:
        log.error(f"Google Ads summary hatası: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/google-ads/health")
def google_ads_health():
    """Google Ads bağlantı kontrolü."""
    try:
        _ads_rest_search("SELECT campaign.name FROM campaign LIMIT 1")
        return jsonify({"ok": True, "connected": True, "customer_id": _GOOGLE_ADS_CID, "transport": "rest"})
    except Exception as e:
        return jsonify({"ok": True, "connected": False, "error": str(e)})


# ══════════════════════════════════════════════════
# GA4 — Google Analytics 4 Entegrasyonu
# Service account JSON gerekiyor:
#   1. Google Cloud Console → IAM → Service Accounts → Oluştur
#   2. GA4 Property → Yönet → Erişim Yönetimi → Service account ekle (Görüntüleyici)
#   3. JSON'ı 05-gsc-nocodb/ga4-service-account.json olarak kaydet
# ══════════════════════════════════════════════════

_GA4_PROPERTY_ID    = os.getenv("GA4_PROPERTY_ID", "")
_GA4_CRED_PATH      = os.getenv("GA4_CREDENTIALS_PATH", str(ROOT / "05-gsc-nocodb" / "ga4-service-account.json"))
_GA4_REFRESH_TOKEN  = os.getenv("GA4_REFRESH_TOKEN", "")
_GA4_TOKEN          = None
_GA4_TOKEN_EXP      = 0


def _get_ga4_token():
    """GA4 access token al — önce OAuth refresh token, sonra service account dener."""
    global _GA4_TOKEN, _GA4_TOKEN_EXP
    import time
    if _GA4_TOKEN and time.time() < _GA4_TOKEN_EXP - 60:
        return _GA4_TOKEN
    if not _GA4_PROPERTY_ID:
        raise ValueError("GA4_PROPERTY_ID tanimli degil — .env dosyasina ekleyin")

    # SSL fix
    try:
        import certifi
        os.environ.setdefault("SSL_CERT_FILE", certifi.where())
        os.environ.setdefault("REQUESTS_CA_BUNDLE", certifi.where())
    except ImportError:
        pass

    from google.auth.transport.requests import Request as _GReq

    # Yöntem 1: OAuth refresh token (cenk@botfusions.com hesabı)
    if _GA4_REFRESH_TOKEN:
        try:
            import yaml as _yaml
            ads_yaml_path = str(ROOT / "04-araclar" / "google_ads_mcp" / "google-ads.yaml")
            with open(ads_yaml_path) as f:
                cfg = _yaml.safe_load(f)
            from google.oauth2 import credentials as _oauth_creds
            oauth = _oauth_creds.Credentials(
                token=None,
                refresh_token=_GA4_REFRESH_TOKEN,
                client_id=cfg["client_id"],
                client_secret=cfg["client_secret"],
                token_uri="https://oauth2.googleapis.com/token",
                scopes=["https://www.googleapis.com/auth/analytics.readonly"],
            )
            oauth.refresh(_GReq())
            _GA4_TOKEN = oauth.token
            _GA4_TOKEN_EXP = oauth.expiry.timestamp() if oauth.expiry else time.time() + 3600
            log.info(f"GA4 token alindi (OAuth) → Property {_GA4_PROPERTY_ID}")
            return _GA4_TOKEN
        except Exception as oauth_err:
            log.warning(f"GA4 OAuth basarisiz: {oauth_err}")

    # Yöntem 2: Service account
    if Path(_GA4_CRED_PATH).exists():
        try:
            from google.oauth2 import service_account as _sa
            creds = _sa.Credentials.from_service_account_file(
                _GA4_CRED_PATH,
                scopes=["https://www.googleapis.com/auth/analytics.readonly"],
            )
            creds.refresh(_GReq())
            _GA4_TOKEN = creds.token
            _GA4_TOKEN_EXP = creds.expiry.timestamp() if creds.expiry else time.time() + 3600
            log.info(f"GA4 token alindi (service account) → Property {_GA4_PROPERTY_ID}")
            return _GA4_TOKEN
        except Exception as sa_err:
            log.warning(f"GA4 service account basarisiz: {sa_err}")

    raise Exception(
        "GA4 token alinamadi. get-ga4-token.py calistirip GA4_REFRESH_TOKEN alin,\n"
        "veya service account'u GA4 property'sine Görüntüleyici olarak ekleyin."
    )


def _ga4_report(date_ranges=None, dimensions=None, metrics=None, dimension_filter=None, limit=15, order_by=None):
    """GA4 Data API REST endpoint — gRPC gerektirmez."""
    token = _get_ga4_token()
    url = f"https://analyticsdata.googleapis.com/v1beta/properties/{_GA4_PROPERTY_ID}:runReport"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    body = {}
    if date_ranges:
        body["dateRanges"] = date_ranges
    if dimensions:
        body["dimensions"] = [{"name": d} for d in dimensions]
    if metrics:
        body["metrics"] = [{"name": m} for m in metrics]
    if dimension_filter:
        body["dimensionFilter"] = dimension_filter
    if limit:
        body["limit"] = str(limit)
    if order_by:
        body["orderBys"] = order_by

    r = req_lib.post(url, headers=headers, json=body, timeout=30)
    if r.status_code != 200:
        raise Exception(f"GA4 API {r.status_code}: {r.text[:300]}")
    return r.json()


@app.route("/api/ga4/summary")
def ga4_summary():
    """GA4 trafik ozeti — son N gun."""
    try:
        days = int(request.args.get("days", "30"))

        # Top sayfalar
        pages_data = _ga4_report(
            date_ranges=[{"startDate": f"{days}daysAgo", "endDate": "today"}],
            dimensions=["pagePath", "pageTitle"],
            metrics=["screenPageViews", "sessions", "averageSessionDuration", "bounceRate", "engagementRate"],
            limit=15,
            order_by=[{"metric": {"metricName": "screenPageViews"}, "desc": True}],
        )
        top_pages = []
        for row in pages_data.get("rows", []):
            top_pages.append({
                "path": row["dimensionValues"][0]["value"],
                "title": row["dimensionValues"][1]["value"],
                "pageviews": int(row["metricValues"][0]["value"]),
                "sessions": int(row["metricValues"][1]["value"]),
                "avg_session_duration": float(row["metricValues"][2]["value"]),
                "bounce_rate": float(row["metricValues"][3]["value"]),
                "engagement_rate": float(row["metricValues"][4]["value"]),
            })

        # Trafik kaynaklari
        src_data = _ga4_report(
            date_ranges=[{"startDate": f"{days}daysAgo", "endDate": "today"}],
            dimensions=["sessionDefaultChannelGroup"],
            metrics=["sessions", "screenPageViews", "engagementRate"],
            limit=10,
            order_by=[{"metric": {"metricName": "sessions"}, "desc": True}],
        )
        sources = []
        for row in src_data.get("rows", []):
            sources.append({
                "source": row["dimensionValues"][0]["value"],
                "sessions": int(row["metricValues"][0]["value"]),
                "pageviews": int(row["metricValues"][1]["value"]),
                "engagement_rate": float(row["metricValues"][2]["value"]),
            })

        # Donusumler
        conv_data = _ga4_report(
            date_ranges=[{"startDate": f"{days}daysAgo", "endDate": "today"}],
            dimensions=["pagePath"],
            metrics=["screenPageViews", "conversions"],
            limit=10,
            order_by=[{"metric": {"metricName": "conversions"}, "desc": True}],
        )
        conversions = []
        for row in conv_data.get("rows", []):
            convs = float(row["metricValues"][1]["value"])
            conversions.append({
                "path": row["dimensionValues"][0]["value"],
                "pageviews": int(row["metricValues"][0]["value"]),
                "conversions": convs,
            })

        total_pageviews = sum(p["pageviews"] for p in top_pages)
        total_sessions  = sum(p["sessions"] for p in top_pages)
        avg_engagement  = (sum(p["engagement_rate"] for p in top_pages) / len(top_pages)) if top_pages else 0
        avg_bounce      = (sum(p["bounce_rate"] for p in top_pages) / len(top_pages)) if top_pages else 0
        total_convs     = sum(c["conversions"] for c in conversions)

        return jsonify({
            "ok": True,
            "period": {"days": days},
            "totals": {
                "pageviews": total_pageviews,
                "sessions": total_sessions,
                "engagement_rate": round(avg_engagement * 100, 1),
                "bounce_rate": round(avg_bounce * 100, 1),
                "conversions": total_convs,
            },
            "top_pages": top_pages,
            "sources": sources,
            "conversions": conversions,
        })
    except Exception as e:
        log.error(f"GA4 summary hatasi: {e}")
        return jsonify({"ok": False, "error": str(e)}), 503


@app.route("/api/ga4/page")
def ga4_page():
    """Belirli bir sayfanin GA4 trend verisi."""
    try:
        url   = request.args.get("url", "/geo-hizmet")
        days  = int(request.args.get("days", "90"))
        data  = _ga4_report(
            date_ranges=[{"startDate": f"{days}daysAgo", "endDate": "today"}],
            dimensions=["date"],
            metrics=["screenPageViews", "sessions", "averageSessionDuration"],
            dimension_filter={
                "filter": {
                    "fieldName": "pagePath",
                    "stringFilter": {"matchType": "EXACT", "value": url},
                }
            },
            limit=90,
            order_by=[{"dimension": {"dimensionName": "date"}, "desc": False}],
        )
        timeline = []
        for row in data.get("rows", []):
            timeline.append({
                "period": row["dimensionValues"][0]["value"],
                "pageviews": int(row["metricValues"][0]["value"]),
                "sessions": int(row["metricValues"][1]["value"]),
                "avg_duration": float(row["metricValues"][2]["value"]),
            })
        return jsonify({"ok": True, "url": url, "timeline": timeline})
    except Exception as e:
        log.error(f"GA4 page trend hatasi: {e}")
        return jsonify({"ok": False, "error": str(e)}), 503


@app.route("/api/ga4/health")
def ga4_health():
    """GA4 baglanti kontrolu."""
    try:
        _get_ga4_token()
        _ga4_report(
            date_ranges=[{"startDate": "1daysAgo", "endDate": "today"}],
            dimensions=["pagePath"],
            metrics=["screenPageViews"],
            limit=1,
        )
        return jsonify({"ok": True, "connected": True, "property_id": _GA4_PROPERTY_ID})
    except Exception as e:
        return jsonify({"ok": True, "connected": False, "error": str(e),
                        "property_id": _GA4_PROPERTY_ID or "tanimli degil"})


# ══════════════════════════════════════════════════
# PageSpeed Proxy — CORS sorunu çözümü
# Tarayıcı direkt Google API'ye erisemiyor, buradan proxyleniyor
# ══════════════════════════════════════════════════

@app.route("/api/pagespeed")
def pagespeed():
    """Google PageSpeed Insights proxy — tarayici CORS'unu asar."""
    url = request.args.get("url", "https://botfusions.com")
    strategy = request.args.get("strategy", "mobile")
    categories = request.args.get("category", "performance,accessibility,best-practices,seo")

    psi_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    params = {
        "url": url,
        "strategy": strategy,
    }
    for cat in categories.split(","):
        params.setdefault("category", [])
        if isinstance(params.get("category"), str):
            params["category"] = [params["category"]]
        params["category"].append(cat)

    try:
        r = req_lib.get(psi_url, params=params, timeout=60)
        return jsonify(r.json())
    except Exception as e:
        log.error(f"PageSpeed proxy hatasi: {e}")
        return jsonify({"error": str(e)}), 500


# ── WaveSpeed AI — 1.000+ Model Uretim Platformu ─────
WAVESPEED_KEY = os.environ.get("WAVESPEED_API_KEY", "")
WAVESPEED_BASE = "https://api.wavespeed.ai/api/v3"


@app.route("/api/wavespeed/generate", methods=["POST", "OPTIONS"])
def wavespeed_generate():
    """WaveSpeed AI ile gorsel, video, muzik uret."""
    if request.method == "OPTIONS":
        return jsonify({}), 200
    if not WAVESPEED_KEY:
        return jsonify({"error": "WAVESPEED_API_KEY ortam degiskeni ayarlanmamis"}), 500
    body = request.get_json(silent=True) or {}
    model = body.get("model", "wavespeed-ai/flux-2-pro-text-to-image")
    prompt = body.get("prompt", "")
    if not prompt:
        return jsonify({"error": "prompt zorunlu"}), 400

    # ── Maliyet kontrolu: GPT Image 2 ve Nano Banana 2 icin zorunlu ayarlar ──
    COST_CONTROLLED = {
        "openai/gpt-image-2-text-to-image",
        "google/nano-banana-2-text-to-image",
    }
    if model in COST_CONTROLLED:
        body.setdefault("resolution", "1K")
        body.setdefault("quality", "low")
        body.setdefault("aspect_ratio", "auto")
        body.setdefault("format", "png")

    params = {k: v for k, v in body.items() if k != "model"}
    try:
        r = req_lib.post(
            f"{WAVESPEED_BASE}/{model}",
            headers={"Authorization": f"Bearer {WAVESPEED_KEY}", "Content-Type": "application/json"},
            json=params,
            timeout=30,
        )
        r.raise_for_status()
        return jsonify(r.json())
    except req_lib.exceptions.HTTPError:
        return jsonify({"error": f"WaveSpeed API hatasi: {r.status_code}", "detail": r.text}), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/wavespeed/status/<task_id>", methods=["GET"])
def wavespeed_status(task_id):
    """WaveSpeed gorev durumunu sorgula."""
    if not WAVESPEED_KEY:
        return jsonify({"error": "WAVESPEED_API_KEY ortam degiskeni ayarlanmamis"}), 500
    try:
        r = req_lib.get(
            f"{WAVESPEED_BASE}/predictions/{task_id}",
            headers={"Authorization": f"Bearer {WAVESPEED_KEY}"},
            timeout=15,
        )
        r.raise_for_status()
        data = r.json().get("data", r.json())
        return jsonify({"task_id": task_id, "status": data.get("status"), "output": data.get("output", [])})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/wavespeed/models", methods=["GET"])
def wavespeed_models():
    """Reklam ajansi icin onemli WaveSpeed modelleri."""
    models = {
        "gorsel": [
            {"id": "openai/gpt-image-2-text-to-image", "name": "GPT Image 2", "note": "Thinking model, kaliteli, metin-hassas"},
            {"id": "google/nano-banana-2-text-to-image", "name": "Nano Banana 2", "note": "Hizli, tutarli, gercekci"},
            {"id": "bytedance/seedream-v4.5", "name": "Seedream 4.5", "note": "Yaratıcı, mukemmel prompt takibi"},
        ],
        "gorsel_edit": [
            {"id": "qwen-image-edit", "name": "Qwen Image Edit", "note": "Gorsel duzenleme"},
            {"id": "wavespeed-ai/flux-2-klein-9b-edit", "name": "FLUX 2 Klein Edit", "note": "Gorsel duzenleme"},
            {"id": "alibaba/wan-2.6-image-edit", "name": "WAN 2.6 Edit", "note": "Gorsel duzenleme"},
        ],
        "video_t2v": [
            {"id": "kwaivgi/kling-v3.0-pro-text-to-video", "name": "Kling 3.0", "note": "Son Kling, ustun kalite"},
            {"id": "kwaivgi/kling-v2.6-pro-text-to-video", "name": "Kling 2.6", "note": "Gercekci, hassas hareket"},
            {"id": "bytedance/seedance-2.0-text-to-video", "name": "Seedance 2.0", "note": "Sinematik + ses"},
        ],
        "video_i2v": [
            {"id": "kwaivgi/kling-v3.0-pro-image-to-video", "name": "Kling 3.0 I2V", "note": "Gorselden video"},
            {"id": "bytedance/seedance-2.0-image-to-video", "name": "Seedance 2.0 I2V", "note": "Gorselden video + ses"},
        ],
        "muzik": [
            {"id": "wavespeed-ai/ace-step-1.5", "name": "Ace Step 1.5", "note": "Hizli muzik"},
            {"id": "elevenlabs/eleven-v3", "name": "ElevenLabs V3", "note": "Seslendirme / TTS"},
        ],
        "araclar": [
            {"id": "wavespeed-ai/image-background-remover", "name": "BG Kaldir", "note": "Arka plan temizle"},
            {"id": "clarity-ai/crystal-upscaler", "name": "Crystal Upscale", "note": "Profesyonel upscale"},
            {"id": "wavespeed-ai/ai-video-ads", "name": "AI Video Ads", "note": "Hazir reklam videosu"},
        ],
    }
    return jsonify(models)


@app.route("/api/wavespeed/balance", methods=["GET"])
def wavespeed_balance():
    """WaveSpeed bakiye sorgula."""
    if not WAVESPEED_KEY:
        return jsonify({"error": "WAVESPEED_API_KEY ortam degiskeni ayarlanmamis"}), 500
    try:
        r = req_lib.get(
            "https://api.wavespeed.ai/api/balance",
            headers={"Authorization": f"Bearer {WAVESPEED_KEY}"},
            timeout=10,
        )
        r.raise_for_status()
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Pipeline: Icerik Uretim Akisi ─────────────────
PIPELINE_TABLE = "content_packages"
PIPELINE_LOGS  = "pipeline_logs"

VALID_NICHES     = {"geo", "agentic", "chatbot"}
VALID_HOOK_TYPES = {"number", "pain_point", "curiosity", "social_proof"}
VALID_POST_TYPES = {"post", "reel", "carousel", "story"}
VALID_STATUSES   = {"draft", "content_approved", "producing_visual",
                    "visual_approved", "scheduled", "published", "failed"}


def _log_pipeline(package_id, action, detail=None):
    """Pipeline log kaydı."""
    try:
        supabase_insert(PIPELINE_LOGS, {
            "package_id": package_id,
            "action": action,
            "detail": detail or {},
        })
    except Exception:
        pass  # log hatası ana akışı durdurmamalı


@app.route("/api/pipeline/packages", methods=["GET", "POST", "OPTIONS"])
def pipeline_packages():
    """Paket listesi (GET) veya yeni paket oluştur (POST)."""
    if request.method == "OPTIONS":
        return jsonify({}), 200

    if request.method == "GET":
        status = request.args.get("status")
        niche  = request.args.get("niche")
        limit  = request.args.get("limit", "50")
        params = {"order": "created_at.desc", "limit": limit,
                  "select": "id,niche,hook_type,hook_text,status,post_type,platforms,campaign,created_at,updated_at"}
        if status:
            params["status"] = f"eq.{status}"
        if niche:
            params["niche"] = f"eq.{niche}"
        try:
            data = supabase_get(PIPELINE_TABLE, params)
            return jsonify({"packages": data})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # POST — yeni paket
    body = request.get_json(silent=True) or {}
    niche      = body.get("niche", "")
    hook_type  = body.get("hook_type", "")
    hook_text  = body.get("hook_text", "")
    caption    = body.get("caption_default", "")

    if niche not in VALID_NICHES:
        return jsonify({"error": f"niche geçersiz: {VALID_NICHES}"}), 400
    if hook_type not in VALID_HOOK_TYPES:
        return jsonify({"error": f"hook_type geçersiz: {VALID_HOOK_TYPES}"}), 400
    if not hook_text or not caption:
        return jsonify({"error": "hook_text ve caption_default zorunlu"}), 400

    post_type = body.get("post_type", "post")
    if post_type not in VALID_POST_TYPES:
        return jsonify({"error": f"post_type geçersiz: {VALID_POST_TYPES}"}), 400

    row = {
        "niche":             niche,
        "hook_type":         hook_type,
        "hook_text":         hook_text,
        "caption_default":   caption,
        "caption_x":         body.get("caption_x"),
        "caption_linkedin":  body.get("caption_linkedin"),
        "caption_pinterest": body.get("caption_pinterest"),
        "caption_instagram": body.get("caption_instagram"),
        "caption_tiktok":    body.get("caption_tiktok"),
        "caption_facebook":  body.get("caption_facebook"),
        "script_video":      body.get("script_video"),
        "visual_brief":      body.get("visual_brief", {}),
        "platforms":         body.get("platforms", []),
        "post_type":         post_type,
        "status":            "draft",
        "strategy_reason":   body.get("strategy_reason"),
        "campaign":          body.get("campaign"),
    }
    # Null alanları temizle
    row = {k: v for k, v in row.items() if v is not None}

    try:
        headers = {
            "Authorization": f"Bearer {SUPA_KEY}",
            "apikey": SUPA_KEY,
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        }
        r = req_lib.post(f"{SUPA_URL}/rest/v1/{PIPELINE_TABLE}",
                         headers=headers, json=row, timeout=10)
        r.raise_for_status()
        created = r.json()
        if created:
            _log_pipeline(created[0]["id"], "created", {"niche": niche, "hook_type": hook_type})
        return jsonify({"ok": True, "package": created[0] if created else {}}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/pipeline/packages/<int:pkg_id>", methods=["GET"])
def pipeline_package_detail(pkg_id):
    """Tek paket detayı."""
    try:
        data = supabase_get(PIPELINE_TABLE, {"id": f"eq.{pkg_id}", "limit": "1"})
        if not data:
            return jsonify({"error": "Paket bulunamadı"}), 404
        return jsonify({"package": data[0]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/pipeline/packages/<int:pkg_id>/approve", methods=["POST", "OPTIONS"])
def pipeline_approve(pkg_id):
    """İçeriği onayla → status: content_approved."""
    if request.method == "OPTIONS":
        return jsonify({}), 200
    body = request.get_json(silent=True) or {}
    try:
        headers = {
            "Authorization": f"Bearer {SUPA_KEY}",
            "apikey": SUPA_KEY,
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        }
        patch = {
            "status": "content_approved",
            "approved_by": body.get("approved_by", "user"),
            "approved_at": "now()",
        }
        r = req_lib.patch(f"{SUPA_URL}/rest/v1/{PIPELINE_TABLE}?id=eq.{pkg_id}",
                          headers=headers, json=patch, timeout=10)
        r.raise_for_status()
        _log_pipeline(pkg_id, "content_approved", {"approved_by": body.get("approved_by")})
        return jsonify({"ok": True, "status": "content_approved"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/pipeline/packages/<int:pkg_id>/reject", methods=["POST", "OPTIONS"])
def pipeline_reject(pkg_id):
    """İçeriği reddet → status: draft, neden kaydet."""
    if request.method == "OPTIONS":
        return jsonify({}), 200
    body = request.get_json(silent=True) or {}
    reason = body.get("reason", "")
    try:
        headers = {
            "Authorization": f"Bearer {SUPA_KEY}",
            "apikey": SUPA_KEY,
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        }
        patch = {"status": "draft", "rejected_reason": reason}
        r = req_lib.patch(f"{SUPA_URL}/rest/v1/{PIPELINE_TABLE}?id=eq.{pkg_id}",
                          headers=headers, json=patch, timeout=10)
        r.raise_for_status()
        _log_pipeline(pkg_id, "rejected", {"reason": reason})
        return jsonify({"ok": True, "status": "draft"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/pipeline/packages/<int:pkg_id>/approve-visual", methods=["POST", "OPTIONS"])
def pipeline_approve_visual(pkg_id):
    """Görseli onayla → status: visual_approved."""
    if request.method == "OPTIONS":
        return jsonify({}), 200
    try:
        headers = {
            "Authorization": f"Bearer {SUPA_KEY}",
            "apikey": SUPA_KEY,
            "Content-Type": "application/json",
        }
        patch = {"status": "visual_approved"}
        r = req_lib.patch(f"{SUPA_URL}/rest/v1/{PIPELINE_TABLE}?id=eq.{pkg_id}",
                          headers=headers, json=patch, timeout=10)
        r.raise_for_status()
        _log_pipeline(pkg_id, "visual_approved")
        return jsonify({"ok": True, "status": "visual_approved"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/pipeline/packages/<int:pkg_id>/publish", methods=["POST", "OPTIONS"])
def pipeline_publish(pkg_id):
    """Onaylı paketi yayınla → OmniSocials + Supabase güncelle."""
    if request.method == "OPTIONS":
        return jsonify({}), 200

    # 1) Paketi çek
    try:
        data = supabase_get(PIPELINE_TABLE, {"id": f"eq.{pkg_id}", "limit": "1"})
        if not data:
            return jsonify({"error": "Paket bulunamadı"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    pkg = data[0]
    if pkg.get("status") != "visual_approved":
        return jsonify({"error": f"Paket durumu visual_approved olmalı, şimdi: {pkg.get('status')}"}), 400

    body = request.get_json(silent=True) or {}
    media_url   = body.get("media_url")   or pkg.get("visual_brief", {}).get("media_url")
    caption     = body.get("caption")     or pkg.get("caption_default", "")
    platforms   = body.get("platforms")   or pkg.get("platforms", [])
    post_type   = pkg.get("post_type", "post")

    if not platforms:
        return jsonify({"error": "platforms zorunlu"}), 400

    published_ids = []
    errors = []

    # 2) Her platform için OmniSocials yayını
    for acct in platforms:
        try:
            payload = {
                "accountId": acct,
                "postType": "reel" if post_type in ("reel", "story") else "post",
                "content": caption[:2200],
            }
            if media_url:
                payload["mediaUrls"] = [media_url]

            scheduled = body.get("scheduled_at")
            if scheduled:
                payload["scheduledAt"] = scheduled

            result = omni_post(payload)
            omni_id = result.get("post", {}).get("id", result.get("id"))
            if omni_id:
                published_ids.append({"platform": acct, "omni_id": omni_id})

            # Supabase social_posts'a da kaydet
            supabase_insert("social_posts", {
                "omnisocials_post_id": str(omni_id) if omni_id else None,
                "caption": caption[:1000],
                "platforms": [acct],
                "post_type": post_type,
                "status": "published",
                "campaign": pkg.get("campaign"),
            })
        except Exception as e:
            errors.append({"platform": acct, "error": str(e)})

    # 3) Paket durumunu güncelle
    new_status = "published" if not errors else "failed"
    try:
        headers = {
            "Authorization": f"Bearer {SUPA_KEY}",
            "apikey": SUPA_KEY,
            "Content-Type": "application/json",
        }
        patch = {
            "status": new_status,
            "published_post_ids": [p["omni_id"] for p in published_ids if p.get("omni_id")],
            "published_at": "now()" if new_status == "published" else None,
        }
        patch = {k: v for k, v in patch.items() if v is not None}
        req_lib.patch(f"{SUPA_URL}/rest/v1/{PIPELINE_TABLE}?id=eq.{pkg_id}",
                      headers=headers, json=patch, timeout=10)
    except Exception:
        pass

    _log_pipeline(pkg_id, new_status, {"published": published_ids, "errors": errors})
    return jsonify({
        "ok": new_status == "published",
        "status": new_status,
        "published": published_ids,
        "errors": errors,
    })


@app.route("/api/pipeline/stats", methods=["GET"])
def pipeline_stats():
    """Pipeline istatistikleri — durum bazlı sayaçlar."""
    try:
        all_pkgs = supabase_get(PIPELINE_TABLE, {
            "select": "status,niche,hook_type",
            "limit": "1000",
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    by_status = {}
    by_niche  = {}
    for p in all_pkgs:
        s = p.get("status", "unknown")
        n = p.get("niche", "unknown")
        by_status[s] = by_status.get(s, 0) + 1
        by_niche[n]  = by_niche.get(n, 0) + 1

    return jsonify({
        "total": len(all_pkgs),
        "by_status": by_status,
        "by_niche": by_niche,
    })


# ── Sunucuyu başlat ────────────────────────────────
if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════╗
║   Botfusions CMO Dashboard — GSC API Sunucusu   ║
╠══════════════════════════════════════════════════╣
║  URL    : http://localhost:8765                  ║
║  Site   : https://botfusions.com                 ║
║  Durdurmak için: Ctrl+C                          ║
╚══════════════════════════════════════════════════╝
""")
    log.info(f"Sunucu başlatılıyor → http://{HOST}:{PORT}")
    app.run(host=HOST, port=PORT, debug=False)
