CREATE TABLE IF NOT EXISTS content_variables (
  key text PRIMARY KEY CHECK (length(key) BETWEEN 1 AND 200),
  value jsonb NOT NULL CHECK (jsonb_typeof(value) IN ('string', 'number', 'boolean') AND octet_length(value::text) <= 16384),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE OR REPLACE FUNCTION notify_variable_change() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE next_revision bigint;
BEGIN
  IF TG_OP = 'UPDATE' AND NEW.key = OLD.key AND NEW.value IS NOT DISTINCT FROM OLD.value THEN
    RETURN NEW;
  END IF;
  UPDATE content_revision SET revision = revision + 1 WHERE singleton RETURNING revision INTO next_revision;
  PERFORM pg_notify('content_changed', next_revision::text);
  IF TG_OP = 'DELETE' THEN RETURN OLD; END IF;
  RETURN NEW;
END;
$$;
DROP TRIGGER IF EXISTS variables_changed ON content_variables;
CREATE TRIGGER variables_changed AFTER INSERT OR UPDATE OR DELETE ON content_variables
FOR EACH ROW EXECUTE FUNCTION notify_variable_change();
DROP TRIGGER IF EXISTS variables_truncated ON content_variables;
CREATE TRIGGER variables_truncated AFTER TRUNCATE ON content_variables
FOR EACH STATEMENT EXECUTE FUNCTION notify_content_truncate();

INSERT INTO content_variables(key,value) VALUES
  ('product', '"EVA 3D Scan"'::jsonb),
  ('languages', '7'::jsonb),
  ('modules', '3'::jsonb),
  ('docsPages', '89'::jsonb)
ON CONFLICT (key) DO NOTHING;
