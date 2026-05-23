-- ============================================================
-- Botfusions GEO Tarama Tablosu
-- Tarih: 2026-05-14
-- Calistir: Supabase Dashboard -> SQL Editor -> Run
-- ============================================================

CREATE TABLE IF NOT EXISTS geo_scans (
  id             BIGSERIAL PRIMARY KEY,
  url            TEXT NOT NULL,
  brand          TEXT DEFAULT 'Botfusions',
  geo_score      NUMERIC(5,1),
  grade          TEXT CHECK (grade IN ('A','B','C','D','F')),
  components     JSONB DEFAULT '{}',   -- 6 bilesenin agirlikli skoru
  scores         JSONB DEFAULT '{}',   -- citability, technical, schema, llms
  page_meta      JSONB DEFAULT '{}',   -- title, word_count, h1, schema_count vs.
  llms_txt       BOOLEAN DEFAULT FALSE,
  llms_full_txt  BOOLEAN DEFAULT FALSE,
  robots_exists  BOOLEAN DEFAULT FALSE,
  findings       JSONB DEFAULT '[]',   -- bulgular listesi (level + text)
  created_at     TIMESTAMPTZ DEFAULT NOW()
);

-- Indeksler
CREATE INDEX IF NOT EXISTS idx_geo_scans_url     ON geo_scans(url);
CREATE INDEX IF NOT EXISTS idx_geo_scans_created ON geo_scans(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_geo_scans_score   ON geo_scans(geo_score DESC);

-- RLS
ALTER TABLE geo_scans ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Anon Read geo_scans"    ON geo_scans;
DROP POLICY IF EXISTS "Service All geo_scans"  ON geo_scans;

CREATE POLICY "Anon Read geo_scans"
  ON geo_scans FOR SELECT USING (true);

CREATE POLICY "Service All geo_scans"
  ON geo_scans FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');

-- ============================================================
-- KONTROL: SELECT * FROM geo_scans ORDER BY created_at DESC;
-- ============================================================
