-- Medya Gelistirme Pipeline — Supabase Tablo Kurulumu
-- Calistir: Supabase Studio → SQL Editor → Yapistir + Run

-- ================================================
-- content_packages: Icerik uretim pipeline state
-- ================================================
CREATE TABLE IF NOT EXISTS content_packages (
  id                BIGSERIAL PRIMARY KEY,
  niche             TEXT NOT NULL CHECK (niche IN ('geo', 'agentic', 'chatbot')),
  hook_type         TEXT NOT NULL CHECK (hook_type IN ('number', 'pain_point', 'curiosity', 'social_proof')),
  hook_text         TEXT NOT NULL,
  caption_default   TEXT NOT NULL,
  caption_x         TEXT,
  caption_linkedin  TEXT,
  caption_pinterest TEXT,
  caption_instagram TEXT,
  caption_tiktok    TEXT,
  caption_facebook  TEXT,
  script_video      TEXT,
  visual_brief      JSONB DEFAULT '{}',
  platforms         TEXT[] DEFAULT '{}',
  post_type         TEXT DEFAULT 'post' CHECK (post_type IN ('post', 'reel', 'carousel', 'story')),
  status            TEXT DEFAULT 'draft'
    CHECK (status IN (
      'draft', 'content_approved', 'producing_visual',
      'visual_approved', 'scheduled', 'published', 'failed'
    )),
  strategy_reason   TEXT,
  campaign          TEXT,
  approved_by       TEXT,
  approved_at       TIMESTAMPTZ,
  rejected_reason   TEXT,
  published_post_ids BIGINT[] DEFAULT '{}',
  published_at      TIMESTAMPTZ,
  created_at        TIMESTAMPTZ DEFAULT NOW(),
  updated_at        TIMESTAMPTZ DEFAULT NOW()
);

-- Indexler
CREATE INDEX IF NOT EXISTS idx_cp_status    ON content_packages(status);
CREATE INDEX IF NOT EXISTS idx_cp_niche     ON content_packages(niche);
CREATE INDEX IF NOT EXISTS idx_cp_created   ON content_packages(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_cp_campaign  ON content_packages(campaign);

-- updated_at otomatik guncelleme
CREATE OR REPLACE FUNCTION update_content_packages_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_cp_updated_at ON content_packages;
CREATE TRIGGER trg_cp_updated_at
  BEFORE UPDATE ON content_packages
  FOR EACH ROW EXECUTE FUNCTION update_content_packages_updated_at();

-- ================================================
-- pipeline_logs: Pipeline olay kayitlari
-- ================================================
CREATE TABLE IF NOT EXISTS pipeline_logs (
  id          BIGSERIAL PRIMARY KEY,
  package_id  BIGINT REFERENCES content_packages(id) ON DELETE SET NULL,
  action      TEXT NOT NULL,
  detail      JSONB DEFAULT '{}',
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_pl_package ON pipeline_logs(package_id);
CREATE INDEX IF NOT EXISTS idx_pl_created ON pipeline_logs(created_at DESC);
