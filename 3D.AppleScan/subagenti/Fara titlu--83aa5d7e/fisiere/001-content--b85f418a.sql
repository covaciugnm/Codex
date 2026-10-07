CREATE TABLE IF NOT EXISTS content_revision (
  singleton boolean PRIMARY KEY DEFAULT true CHECK (singleton),
  revision bigint NOT NULL DEFAULT 0
);
INSERT INTO content_revision(singleton) VALUES (true) ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS content_messages (
  locale text NOT NULL CHECK (locale IN ('en','de','fr','es','ro','hu','bg')),
  key text NOT NULL CHECK (length(key) BETWEEN 1 AND 200),
  value text NOT NULL,
  updated_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (locale, key)
);
CREATE TABLE IF NOT EXISTS site_metadata (
  key text PRIMARY KEY,
  value text NOT NULL
);

CREATE OR REPLACE FUNCTION notify_content_change() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE next_revision bigint;
BEGIN
  IF TG_OP = 'UPDATE' AND NEW.locale = OLD.locale AND NEW.key = OLD.key AND NEW.value IS NOT DISTINCT FROM OLD.value THEN
    RETURN NEW;
  END IF;
  UPDATE content_revision SET revision = revision + 1 WHERE singleton RETURNING revision INTO next_revision;
  PERFORM pg_notify('content_changed', next_revision::text);
  IF TG_OP = 'DELETE' THEN RETURN OLD; END IF;
  RETURN NEW;
END;
$$;
DROP TRIGGER IF EXISTS content_changed ON content_messages;
CREATE TRIGGER content_changed AFTER INSERT OR UPDATE OR DELETE ON content_messages
FOR EACH ROW EXECUTE FUNCTION notify_content_change();

CREATE OR REPLACE FUNCTION notify_content_truncate() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE next_revision bigint;
BEGIN
  UPDATE content_revision SET revision = revision + 1 WHERE singleton RETURNING revision INTO next_revision;
  PERFORM pg_notify('content_changed', next_revision::text);
  RETURN NULL;
END;
$$;
DROP TRIGGER IF EXISTS content_truncated ON content_messages;
CREATE TRIGGER content_truncated AFTER TRUNCATE ON content_messages
FOR EACH STATEMENT EXECUTE FUNCTION notify_content_truncate();
