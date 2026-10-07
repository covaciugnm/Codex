-- Canonical, field-level multilingual content and database-defined placement.
-- Apply after schema.sql. Display text is resolved from these tables, never source literals.
BEGIN;
SET search_path TO eva_print,public;
CREATE TABLE page_definitions (
 id text PRIMARY KEY, template_key text NOT NULL,
 route_pattern text NOT NULL UNIQUE,
 publication_status text NOT NULL DEFAULT 'draft',
 layout_version bigint NOT NULL DEFAULT 1,
 cache_tag text NOT NULL UNIQUE,
 page_options jsonb NOT NULL DEFAULT '{}'
);
CREATE TABLE page_positions (
 id text PRIMARY KEY, page_id text NOT NULL REFERENCES page_definitions(id),
 position_key text NOT NULL, parent_position_id text REFERENCES page_positions(id),
 component_key text NOT NULL, region_key text NOT NULL, sort_order integer NOT NULL DEFAULT 0,
 placement_options jsonb NOT NULL DEFAULT '{}', enabled boolean NOT NULL DEFAULT true,
 UNIQUE(page_id,position_key)
);
CREATE TABLE content_fields (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), field_key text UNIQUE NOT NULL,
 entity_type text NOT NULL, entity_id text NOT NULL, property_path text NOT NULL,
 value_type text NOT NULL CHECK(value_type IN ('text','rich_text','text_list','number','boolean','url','asset_ref','structured')),
 source_locale text NOT NULL REFERENCES locales(code), source_value jsonb NOT NULL,
 source_version bigint NOT NULL DEFAULT 1 CHECK(source_version>0),
 translatable boolean NOT NULL DEFAULT true, publication_status text NOT NULL DEFAULT 'draft',
 updated_by uuid REFERENCES users(id), updated_at timestamptz NOT NULL DEFAULT now(),
 UNIQUE(entity_type,entity_id,property_path)
);
CREATE TABLE field_translations (
 field_id uuid NOT NULL REFERENCES content_fields(id) ON DELETE CASCADE,
 locale_code text NOT NULL REFERENCES locales(code), translated_value jsonb NOT NULL,
 source_version bigint NOT NULL, review_status text NOT NULL DEFAULT 'draft'
 CHECK(review_status IN ('draft','machine_translated','reviewed','stale')),
 translated_by uuid REFERENCES users(id), reviewed_by uuid REFERENCES users(id),
 updated_at timestamptz NOT NULL DEFAULT now(), reviewed_at timestamptz,
 PRIMARY KEY(field_id,locale_code)
);
CREATE TABLE field_placements (
 field_id uuid NOT NULL REFERENCES content_fields(id), position_id text NOT NULL REFERENCES page_positions(id),
 binding_key text NOT NULL, display_order integer NOT NULL DEFAULT 0,
 variant_options jsonb NOT NULL DEFAULT '{}',
 PRIMARY KEY(field_id,position_id,binding_key)
);
CREATE TABLE localized_positions (
 position_id text NOT NULL REFERENCES page_positions(id), locale_code text NOT NULL REFERENCES locales(code),
 sort_order_override integer, placement_options_override jsonb NOT NULL DEFAULT '{}',
 PRIMARY KEY(position_id,locale_code)
);
CREATE TABLE menu_definitions (id text PRIMARY KEY, location_key text NOT NULL, options jsonb NOT NULL DEFAULT '{}');
CREATE TABLE menu_items (
 id text PRIMARY KEY, menu_id text NOT NULL REFERENCES menu_definitions(id), parent_id text REFERENCES menu_items(id),
 label_field_id uuid NOT NULL REFERENCES content_fields(id), route_key text NOT NULL,
 sort_order integer NOT NULL DEFAULT 0, visibility_rule jsonb NOT NULL DEFAULT '{}', enabled boolean NOT NULL DEFAULT true
);
CREATE TABLE form_definitions (id text PRIMARY KEY, version bigint NOT NULL DEFAULT 1, settings jsonb NOT NULL DEFAULT '{}');
CREATE TABLE form_fields (
 id text PRIMARY KEY, form_id text NOT NULL REFERENCES form_definitions(id),
 property_key text NOT NULL, input_type text NOT NULL, step_number integer NOT NULL DEFAULT 1,
 sort_order integer NOT NULL DEFAULT 0, label_field_id uuid NOT NULL REFERENCES content_fields(id),
 placeholder_field_id uuid REFERENCES content_fields(id), help_field_id uuid REFERENCES content_fields(id),
 validation_rules jsonb NOT NULL DEFAULT '{}', options_source jsonb NOT NULL DEFAULT '{}',
 UNIQUE(form_id,property_key)
);
CREATE TABLE translation_jobs (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), field_id uuid NOT NULL REFERENCES content_fields(id),
 locale_code text NOT NULL REFERENCES locales(code), source_version bigint NOT NULL,
 status text NOT NULL DEFAULT 'queued' CHECK(status IN ('queued','working','ready_for_review','published','failed','superseded')),
 created_at timestamptz NOT NULL DEFAULT now(), completed_at timestamptz,
 UNIQUE(field_id,locale_code,source_version)
);
CREATE TABLE field_revisions (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), field_id uuid NOT NULL REFERENCES content_fields(id),
 source_version bigint NOT NULL, source_value jsonb NOT NULL, actor_user_id uuid REFERENCES users(id),
 created_at timestamptz NOT NULL DEFAULT now(), UNIQUE(field_id,source_version)
);
CREATE TABLE render_events (
 id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, entity_type text NOT NULL, entity_id text NOT NULL,
 reason text NOT NULL, data jsonb NOT NULL DEFAULT '{}', created_at timestamptz NOT NULL DEFAULT now(),
 processed_at timestamptz
);
CREATE TABLE site_settings (
 setting_key text PRIMARY KEY, value jsonb NOT NULL,
 setting_type text NOT NULL, updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE content_token_bindings (
 token_key text PRIMARY KEY CHECK(token_key ~ '^[a-z][a-z0-9_]*$'),
 setting_key text REFERENCES site_settings(setting_key),
 entity_binding jsonb, value_format text NOT NULL DEFAULT 'text',
 CHECK((setting_key IS NOT NULL)::integer+(entity_binding IS NOT NULL)::integer=1)
);
CREATE TABLE locale_plural_templates (
 field_id uuid NOT NULL REFERENCES content_fields(id), locale_code text NOT NULL REFERENCES locales(code),
 plural_category text NOT NULL CHECK(plural_category IN ('zero','one','two','few','many','other')),
 template_value jsonb NOT NULL, source_version bigint NOT NULL,
 review_status text NOT NULL DEFAULT 'draft' CHECK(review_status IN ('draft','reviewed','stale')),
 PRIMARY KEY(field_id,locale_code,plural_category)
);
CREATE TABLE translation_resolution_policy (
 id integer PRIMARY KEY CHECK(id=1), allow_stale_public_translation boolean NOT NULL DEFAULT false,
 show_fallback_language_label boolean NOT NULL DEFAULT true,
 automatic_machine_translation boolean NOT NULL DEFAULT false
);
INSERT INTO translation_resolution_policy(id) VALUES(1);
CREATE INDEX field_entity_lookup ON content_fields(entity_type,entity_id);
CREATE INDEX field_translation_lookup ON field_translations(locale_code,review_status,source_version);
CREATE INDEX positions_page_region ON page_positions(page_id,region_key,sort_order);
CREATE INDEX translations_queue ON translation_jobs(status,created_at);
CREATE INDEX render_queue ON render_events(processed_at,id);

CREATE FUNCTION advance_source_version() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 IF NEW.source_value IS DISTINCT FROM OLD.source_value OR NEW.source_locale IS DISTINCT FROM OLD.source_locale THEN
  INSERT INTO field_revisions(field_id,source_version,source_value,actor_user_id)
   VALUES(OLD.id,OLD.source_version,OLD.source_value,NEW.updated_by) ON CONFLICT DO NOTHING;
  NEW.source_version=OLD.source_version+1;
  NEW.updated_at=now();
 END IF;
 RETURN NEW;
END $$;
CREATE TRIGGER advance_content_version BEFORE UPDATE ON content_fields
 FOR EACH ROW EXECUTE FUNCTION advance_source_version();
CREATE FUNCTION propagate_field_change() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 IF NEW.source_version IS DISTINCT FROM OLD.source_version THEN
  UPDATE field_translations SET review_status='stale',updated_at=now() WHERE field_id=NEW.id;
  UPDATE locale_plural_templates SET review_status='stale' WHERE field_id=NEW.id;
  UPDATE translation_jobs SET status='superseded' WHERE field_id=NEW.id AND status IN ('queued','working','ready_for_review');
  IF NEW.translatable THEN
   INSERT INTO translation_jobs(field_id,locale_code,source_version)
    SELECT NEW.id,code,NEW.source_version FROM locales WHERE code<>NEW.source_locale
    ON CONFLICT DO NOTHING;
  END IF;
  INSERT INTO render_events(entity_type,entity_id,reason,data)
   VALUES(NEW.entity_type,NEW.entity_id,'source_field_changed',jsonb_build_object('field_key',NEW.field_key,'source_version',NEW.source_version));
  PERFORM pg_notify('eva_content_changed',NEW.id::text);
 END IF;
 RETURN NEW;
END $$;
CREATE TRIGGER propagate_content_change AFTER UPDATE ON content_fields
 FOR EACH ROW EXECUTE FUNCTION propagate_field_change();
CREATE FUNCTION invalidate_field_publication() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 IF NEW.publication_status IS DISTINCT FROM OLD.publication_status OR NEW.translatable IS DISTINCT FROM OLD.translatable THEN
  INSERT INTO render_events(entity_type,entity_id,reason) VALUES(NEW.entity_type,NEW.entity_id,'field_visibility_changed');
 END IF;
 RETURN NEW;
END $$;
CREATE TRIGGER field_publication_changed AFTER UPDATE ON content_fields FOR EACH ROW EXECUTE FUNCTION invalidate_field_publication();
CREATE FUNCTION translation_must_match_source() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 IF NEW.review_status<>'stale' AND NOT EXISTS (
  SELECT 1 FROM content_fields f WHERE f.id=NEW.field_id AND f.source_version=NEW.source_version
 ) THEN RAISE EXCEPTION 'A reviewed translation must match the current source version'; END IF;
 RETURN NEW;
END $$;
CREATE TRIGGER validate_translation_version BEFORE INSERT OR UPDATE ON field_translations
 FOR EACH ROW EXECUTE FUNCTION translation_must_match_source();
CREATE TRIGGER validate_plural_version BEFORE INSERT OR UPDATE ON locale_plural_templates
 FOR EACH ROW EXECUTE FUNCTION translation_must_match_source();
CREATE FUNCTION translation_preserves_tokens() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE source_tokens text[]; translated_tokens text[]; source_text text;
BEGIN
 IF NEW.review_status='stale' THEN RETURN NEW; END IF;
 SELECT source_value::text INTO source_text FROM content_fields WHERE id=NEW.field_id;
 SELECT ARRAY(SELECT DISTINCT tokens[1] FROM regexp_matches(source_text,'\{([a-z][a-z0-9_]*)\}','g') AS m(tokens) ORDER BY tokens[1]) INTO source_tokens;
 SELECT ARRAY(SELECT DISTINCT tokens[1] FROM regexp_matches(NEW.translated_value::text,'\{([a-z][a-z0-9_]*)\}','g') AS m(tokens) ORDER BY tokens[1]) INTO translated_tokens;
 IF source_tokens IS DISTINCT FROM translated_tokens THEN RAISE EXCEPTION 'Translation must preserve registered source tokens'; END IF;
 RETURN NEW;
END $$;
CREATE TRIGGER preserve_translation_tokens BEFORE INSERT OR UPDATE ON field_translations
 FOR EACH ROW EXECUTE FUNCTION translation_preserves_tokens();
CREATE FUNCTION emit_translation_render_event() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 INSERT INTO render_events(entity_type,entity_id,reason,data)
  SELECT entity_type,entity_id,'translation_changed',jsonb_build_object('locale',NEW.locale_code,'field_key',field_key)
  FROM content_fields WHERE id=NEW.field_id;
 PERFORM pg_notify('eva_content_changed',NEW.field_id::text);
 RETURN NEW;
END $$;
CREATE TRIGGER translation_render_event AFTER INSERT OR UPDATE ON field_translations
 FOR EACH ROW EXECUTE FUNCTION emit_translation_render_event();
CREATE FUNCTION emit_position_render_event() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 UPDATE page_definitions SET layout_version=layout_version+1 WHERE id=coalesce(NEW.page_id,OLD.page_id);
 INSERT INTO render_events(entity_type,entity_id,reason) VALUES('page',coalesce(NEW.page_id,OLD.page_id),'layout_changed');
 RETURN coalesce(NEW,OLD);
END $$;
CREATE TRIGGER position_render_event AFTER INSERT OR UPDATE OR DELETE ON page_positions
 FOR EACH ROW EXECUTE FUNCTION emit_position_render_event();

CREATE FUNCTION queue_new_locale() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 INSERT INTO translation_jobs(field_id,locale_code,source_version)
  SELECT id,NEW.code,source_version FROM content_fields
  WHERE translatable AND source_locale<>NEW.code ON CONFLICT DO NOTHING;
 INSERT INTO render_events(entity_type,entity_id,reason) VALUES('site',NEW.code,'locale_added');
 RETURN NEW;
END $$;
CREATE TRIGGER new_locale_jobs AFTER INSERT ON locales FOR EACH ROW EXECUTE FUNCTION queue_new_locale();

-- Small shared definitions affect many pages; use a durable site-wide invalidation event.
CREATE FUNCTION invalidate_shared_definition() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 INSERT INTO render_events(entity_type,entity_id,reason,data)
  VALUES('site',TG_TABLE_NAME,'shared_definition_changed',jsonb_build_object('operation',TG_OP));
 PERFORM pg_notify('eva_content_changed',TG_TABLE_NAME);
 IF TG_OP='DELETE' THEN RETURN OLD; ELSE RETURN NEW; END IF;
END $$;
CREATE TRIGGER placement_invalidation AFTER INSERT OR UPDATE OR DELETE ON field_placements FOR EACH ROW EXECUTE FUNCTION invalidate_shared_definition();
CREATE TRIGGER localized_position_invalidation AFTER INSERT OR UPDATE OR DELETE ON localized_positions FOR EACH ROW EXECUTE FUNCTION invalidate_shared_definition();
CREATE TRIGGER menu_invalidation AFTER INSERT OR UPDATE OR DELETE ON menu_items FOR EACH ROW EXECUTE FUNCTION invalidate_shared_definition();
CREATE TRIGGER form_invalidation AFTER INSERT OR UPDATE OR DELETE ON form_fields FOR EACH ROW EXECUTE FUNCTION invalidate_shared_definition();
CREATE TRIGGER locale_invalidation AFTER UPDATE OR DELETE ON locales FOR EACH ROW EXECUTE FUNCTION invalidate_shared_definition();
CREATE TRIGGER settings_invalidation AFTER INSERT OR UPDATE OR DELETE ON site_settings FOR EACH ROW EXECUTE FUNCTION invalidate_shared_definition();
CREATE TRIGGER token_invalidation AFTER INSERT OR UPDATE OR DELETE ON content_token_bindings FOR EACH ROW EXECUTE FUNCTION invalidate_shared_definition();
CREATE TRIGGER plural_invalidation AFTER INSERT OR UPDATE OR DELETE ON locale_plural_templates FOR EACH ROW EXECUTE FUNCTION invalidate_shared_definition();

CREATE FUNCTION queue_initial_field_translations() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 IF NEW.translatable THEN
  INSERT INTO translation_jobs(field_id,locale_code,source_version)
   SELECT NEW.id,code,NEW.source_version FROM locales WHERE code<>NEW.source_locale ON CONFLICT DO NOTHING;
 END IF;
 INSERT INTO render_events(entity_type,entity_id,reason) VALUES(NEW.entity_type,NEW.entity_id,'field_added');
 RETURN NEW;
END $$;
CREATE TRIGGER initial_field_translations AFTER INSERT ON content_fields FOR EACH ROW EXECUTE FUNCTION queue_initial_field_translations();

-- Single bulk query resolves every page/entity field for one requested language.
-- A missing or stale translation falls back to the field's current source language.
CREATE FUNCTION resolved_fields(p_entity_type text,p_entity_id text,p_locale text)
 RETURNS TABLE(field_key text,value jsonb,resolved_locale text,is_fallback boolean,source_version bigint)
 LANGUAGE sql STABLE AS $$
 SELECT f.field_key,
  CASE WHEN NOT f.translatable OR p_locale=f.source_locale THEN f.source_value
       WHEN t.review_status='reviewed' AND t.source_version=f.source_version THEN t.translated_value ELSE f.source_value END,
  CASE WHEN f.translatable AND p_locale<>f.source_locale AND t.review_status='reviewed' AND t.source_version=f.source_version THEN p_locale ELSE f.source_locale END,
  f.translatable AND p_locale<>f.source_locale AND NOT coalesce(t.review_status='reviewed' AND t.source_version=f.source_version,false),
  f.source_version
 FROM content_fields f LEFT JOIN field_translations t ON t.field_id=f.id AND t.locale_code=p_locale
 WHERE f.entity_type=p_entity_type AND f.entity_id=p_entity_id AND f.publication_status='published'
 $$;

-- All binary content resides in PostgreSQL under the owner's all-data-in-DB requirement.
-- Chunking supports bounded-memory streaming; private blobs are never public static files.
CREATE TABLE file_blobs (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 project_file_id uuid UNIQUE REFERENCES project_files(id) ON DELETE CASCADE,
 asset_id uuid UNIQUE REFERENCES assets(id) ON DELETE CASCADE,
 byte_length bigint NOT NULL CHECK(byte_length>0), checksum_sha256 text NOT NULL,
 media_type text NOT NULL, visibility text NOT NULL CHECK(visibility IN ('private','licensed_public')),
 encryption_key_ref text, complete boolean NOT NULL DEFAULT false,
 created_at timestamptz NOT NULL DEFAULT now(),
 CHECK((project_file_id IS NOT NULL)::integer+(asset_id IS NOT NULL)::integer=1),
 CHECK(project_file_id IS NULL OR visibility='private')
);
CREATE TABLE file_blob_chunks (
 blob_id uuid NOT NULL REFERENCES file_blobs(id) ON DELETE CASCADE,
 chunk_index integer NOT NULL CHECK(chunk_index>=0),
 data bytea NOT NULL CHECK(octet_length(data)>0 AND octet_length(data)<=8388608),
 PRIMARY KEY(blob_id,chunk_index)
);
CREATE TABLE asset_derivatives (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), source_asset_id uuid NOT NULL REFERENCES assets(id),
 derivative_asset_id uuid UNIQUE NOT NULL REFERENCES assets(id),
 width_px integer CHECK(width_px>0), height_px integer CHECK(height_px>0),
 format text NOT NULL, purpose text NOT NULL
);
ALTER TABLE file_blobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE file_blobs FORCE ROW LEVEL SECURITY;
CREATE POLICY blob_access ON file_blobs USING(
 actor_is_staff() OR (complete AND (
 (visibility='licensed_public' AND EXISTS(SELECT 1 FROM assets a WHERE a.id=asset_id AND a.rights_status IN ('eva_original','licensed','permission_granted') AND a.publication_status='published'))
 OR EXISTS(SELECT 1 FROM project_files pf WHERE pf.id=project_file_id AND pf.scan_status='clean')
 ))
) WITH CHECK(actor_is_staff() OR EXISTS(SELECT 1 FROM project_files pf WHERE pf.id=project_file_id AND pf.uploaded_by_user_id=current_actor()));
ALTER TABLE file_blob_chunks ENABLE ROW LEVEL SECURITY;
ALTER TABLE file_blob_chunks FORCE ROW LEVEL SECURITY;
CREATE POLICY chunk_access ON file_blob_chunks USING(EXISTS(SELECT 1 FROM file_blobs b WHERE b.id=blob_id))
 WITH CHECK(EXISTS(SELECT 1 FROM file_blobs b WHERE b.id=blob_id AND (actor_is_staff() OR EXISTS(SELECT 1 FROM project_files pf WHERE pf.id=b.project_file_id AND pf.uploaded_by_user_id=current_actor()))));
COMMIT;
