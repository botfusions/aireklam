-- ============================================================
-- Botfusions AI Reklam Ajansi -- Supabase Kurulum SQL
-- Tarih: 2026-05-14
-- Calistirma: Supabase Dashboard -> SQL Editor -> Run
-- ============================================================


-- ============================================================
-- 1. STORAGE BUCKET (Gorsel & Video Deposu)
-- ============================================================

INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
  'media-library',
  'media-library',
  true,
  104857600,  -- 100MB limit
  ARRAY['image/jpeg','image/png','image/gif','image/webp','video/mp4','video/mov','video/quicktime']
)
ON CONFLICT (id) DO NOTHING;

-- Bucket public erisim politikasi
DROP POLICY IF EXISTS "Public Read"   ON storage.objects;
DROP POLICY IF EXISTS "Service Upload" ON storage.objects;
DROP POLICY IF EXISTS "Service Delete" ON storage.objects;

CREATE POLICY "Public Read"
  ON storage.objects FOR SELECT
  USING (bucket_id = 'media-library');

CREATE POLICY "Service Upload"
  ON storage.objects FOR INSERT
  WITH CHECK (bucket_id = 'media-library');

CREATE POLICY "Service Delete"
  ON storage.objects FOR DELETE
  USING (bucket_id = 'media-library');


-- ============================================================
-- 2. MEDIA_LIBRARY TABLOSU
-- Uretilen tum gorsel ve videolar burada saklanir
-- ============================================================

CREATE TABLE IF NOT EXISTS media_library (
  id              BIGSERIAL PRIMARY KEY,
  filename        TEXT NOT NULL,
  type            TEXT NOT NULL CHECK (type IN ('image', 'video')),
  mime_type       TEXT,
  size_bytes      BIGINT,
  width           INTEGER,
  height          INTEGER,
  duration_sec    NUMERIC,                    -- Video icin sure (saniye)
  storage_path    TEXT,                       -- Supabase Storage path
  public_url      TEXT NOT NULL,              -- Erisim URL'i
  omnisocials_id  TEXT,                       -- OmniSocials media ID (varsa)
  source          TEXT DEFAULT 'local'        -- 'local' | 'omnisocials' | 'google-drive'
                  CHECK (source IN ('local', 'omnisocials', 'google-drive')),
  tags            TEXT[] DEFAULT '{}',        -- ['geo', 'linkedin', 'reel'] gibi
  campaign        TEXT,                       -- 'geo-hizmet' gibi kampanya adi
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_media_library_type      ON media_library(type);
CREATE INDEX IF NOT EXISTS idx_media_library_campaign  ON media_library(campaign);
CREATE INDEX IF NOT EXISTS idx_media_library_created   ON media_library(created_at DESC);

-- Updated_at otomatik guncelle
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS media_library_updated_at ON media_library;
CREATE TRIGGER media_library_updated_at
  BEFORE UPDATE ON media_library
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();


-- ============================================================
-- 3. SOCIAL_POSTS TABLOSU
-- Yayinlanan tum postlar burada kayitli kalir
-- ============================================================

CREATE TABLE IF NOT EXISTS social_posts (
  id                  BIGSERIAL PRIMARY KEY,
  omnisocials_post_id TEXT,                   -- OmniSocials'tan gelen post ID
  caption             TEXT NOT NULL,
  caption_platforms   JSONB DEFAULT '{}',     -- Platform bazli farkli metinler
  media_library_id    BIGINT REFERENCES media_library(id),
  omnisocials_media_id TEXT,                  -- OmniSocials media ID
  platforms           TEXT[] NOT NULL,        -- ['instagram','facebook','x']
  post_type           TEXT DEFAULT 'post'
                      CHECK (post_type IN ('post', 'reel', 'story')),
  status              TEXT DEFAULT 'draft'
                      CHECK (status IN ('draft','posting','published','partially_posted','failed','scheduled')),
  published_urls      JSONB DEFAULT '{}',     -- Platform URL'leri
  failed_platforms    JSONB DEFAULT '[]',     -- Basarisiz platformlar
  scheduled_at        TIMESTAMPTZ,
  published_at        TIMESTAMPTZ,
  campaign            TEXT,
  youtube_title       TEXT,
  notes               TEXT,
  created_at          TIMESTAMPTZ DEFAULT NOW(),
  updated_at          TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_social_posts_status    ON social_posts(status);
CREATE INDEX IF NOT EXISTS idx_social_posts_campaign  ON social_posts(campaign);
CREATE INDEX IF NOT EXISTS idx_social_posts_created   ON social_posts(created_at DESC);

DROP TRIGGER IF EXISTS social_posts_updated_at ON social_posts;
CREATE TRIGGER social_posts_updated_at
  BEFORE UPDATE ON social_posts
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();


-- ============================================================
-- 4. ROW LEVEL SECURITY (RLS)
-- ============================================================

ALTER TABLE media_library  ENABLE ROW LEVEL SECURITY;
ALTER TABLE social_posts   ENABLE ROW LEVEL SECURITY;

-- Anon key okuyabilir
DROP POLICY IF EXISTS "Anon Read media_library" ON media_library;
DROP POLICY IF EXISTS "Anon Read social_posts"  ON social_posts;
DROP POLICY IF EXISTS "Service All media_library" ON media_library;
DROP POLICY IF EXISTS "Service All social_posts"  ON social_posts;

CREATE POLICY "Anon Read media_library"
  ON media_library FOR SELECT USING (true);

CREATE POLICY "Anon Read social_posts"
  ON social_posts FOR SELECT USING (true);

-- Service key her seyi yapabilir
CREATE POLICY "Service All media_library"
  ON media_library FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "Service All social_posts"
  ON social_posts FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');


-- ============================================================
-- 5. ORNEK KAYIT -- Ilk basarili yayin (14 Mayis 2026)
-- ============================================================

INSERT INTO media_library (filename, type, mime_type, public_url, omnisocials_id, source, campaign)
VALUES (
  'linkedin-ad-45s.mp4',
  'video',
  'video/mp4',
  'https://cdn.omnisocials.com/file/library-omnisocials/e50fd039-debb-4c42-b75f-fe36f3901244/library/1778747383581-roxo54_c6208440-d120-4707-8345-3274e9b14cfe.mp4',
  '1881',
  'omnisocials',
  'geo-hizmet'
);

INSERT INTO social_posts (omnisocials_post_id, caption, platforms, post_type, status, campaign, youtube_title, published_at)
VALUES (
  '1881',
  'Geleneksel SEO mavi link dunyasi, yerini hizla yapay zekanin yonlendirdigi Atif Ekonomisi Citation Economy birakiyor...',
  ARRAY['instagram','facebook','youtube','tiktok','x'],
  'reel',
  'published',
  'geo-hizmet',
  'Atif Ekonomisi: Yapay Zeka Caginda SEO Kurallari | Botfusions GEO',
  '2026-05-14T08:30:00Z'
);


-- ============================================================
-- TAMAMLANDI
-- Kontrol: SELECT * FROM media_library; SELECT * FROM social_posts;
-- ============================================================
