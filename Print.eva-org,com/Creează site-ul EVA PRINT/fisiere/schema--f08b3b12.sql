-- EVA PRINT website schema. Execute using a migration owner; use a separate restricted runtime role.
-- PostgreSQL 16 or newer. No customer data or credentials are included in the seed.
BEGIN;
CREATE SCHEMA IF NOT EXISTS eva_print;
SET search_path TO eva_print, public;

CREATE TABLE locales (
 code text PRIMARY KEY CHECK (code ~ '^[a-z]{2,3}(-[A-Za-z0-9]{2,8})*$'),
 native_name text NOT NULL, enabled boolean NOT NULL DEFAULT false,
 is_default boolean NOT NULL DEFAULT false, sort_order integer NOT NULL DEFAULT 0,
 fallback_code text REFERENCES locales(code), formatting_options jsonb NOT NULL DEFAULT '{}'
);
CREATE UNIQUE INDEX one_default_language ON locales(is_default) WHERE is_default;
CREATE TABLE sources (
 url text PRIMARY KEY CHECK (url ~ '^https://'), title text NOT NULL,
 checked_at date NOT NULL, notes text
);
CREATE TABLE printers (
 id text PRIMARY KEY, name text NOT NULL,
 nominal_x_mm numeric NOT NULL CHECK (nominal_x_mm>0), nominal_y_mm numeric NOT NULL CHECK (nominal_y_mm>0), nominal_z_mm numeric NOT NULL CHECK (nominal_z_mm>0),
 verified_usable_x_mm numeric, verified_usable_y_mm numeric, verified_usable_z_mm numeric,
 toolheads integer NOT NULL CHECK (toolheads>0), toolheads_confirmed boolean NOT NULL DEFAULT false,
 reference_nozzle_max_c numeric, reference_bed_max_c numeric,
 installed_configuration jsonb NOT NULL DEFAULT '{}', verification_status text NOT NULL DEFAULT 'needs_owner_confirmation', source_url text REFERENCES sources(url)
);
CREATE TABLE material_families (code text PRIMARY KEY, name_en text NOT NULL);
CREATE TABLE materials (
 id text PRIMARY KEY, slug text UNIQUE NOT NULL, name text NOT NULL,
 family_code text NOT NULL REFERENCES material_families(code), brand text NOT NULL,
 variant text, service_status text NOT NULL,
 stock_status text NOT NULL DEFAULT 'unverified',
 manufacturer_tds_status text NOT NULL,
 publication_status text NOT NULL DEFAULT 'draft' CHECK(publication_status IN ('draft','reviewed','published','archived')),
 source_url text, settings jsonb NOT NULL DEFAULT '{}', properties jsonb NOT NULL DEFAULT '[]',
 created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE colors (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), material_id text NOT NULL REFERENCES materials(id),
 supplier_color_name text NOT NULL, supplier_sku text, diameter_mm numeric CHECK(diameter_mm>0),
 display_hex text CHECK(display_hex IS NULL OR display_hex ~ '^#[0-9A-Fa-f]{6}$'),
 finish text, source_url text,
 available_at_supplier boolean, quantity_in_stock_kg numeric CHECK(quantity_in_stock_kg>=0),
 stock_verified_at timestamptz, active boolean NOT NULL DEFAULT true
);
CREATE TABLE supplier_sku_options (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), material_id text NOT NULL REFERENCES materials(id),
 supplier_sku text, supplier_variant_title text NOT NULL,
 available_at_supplier boolean, diameter_note text, source_url text NOT NULL,
 raw_supplier_options jsonb NOT NULL DEFAULT '{}',
 CHECK(source_url ~ '^https://')
);
CREATE TABLE material_printer_compatibility (
 material_id text NOT NULL REFERENCES materials(id), printer_id text NOT NULL REFERENCES printers(id),
 status text NOT NULL, validated_profile_ref text, notes text, validated_at timestamptz,
 PRIMARY KEY(material_id,printer_id)
);
CREATE TABLE industries (id text PRIMARY KEY, slug text UNIQUE NOT NULL, publication_status text NOT NULL DEFAULT 'draft');
CREATE TABLE industry_materials (
 industry_id text NOT NULL REFERENCES industries(id), material_id text NOT NULL REFERENCES materials(id),
 relationship text NOT NULL DEFAULT 'proposed', PRIMARY KEY(industry_id,material_id)
);
CREATE TABLE assets (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), relative_path text UNIQUE NOT NULL,
 kind text NOT NULL CHECK(kind IN ('photo','drawing_svg','drawing_png','drawing_pdf','drawing_dxf','manufacturer_pdf','manufacturer_zip','overview_pdf')),
 source_url text, source_page_url text, attribution text,
 rights_status text NOT NULL CHECK(rights_status IN ('eva_original','reference_only','permission_granted','licensed')),
 publication_status text NOT NULL DEFAULT 'reference_only', checksum_sha256 text,
 created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE material_assets (
 material_id text NOT NULL REFERENCES materials(id), asset_id uuid NOT NULL REFERENCES assets(id),
 role text NOT NULL, PRIMARY KEY(material_id,asset_id,role)
);
CREATE TABLE examples (
 id text PRIMARY KEY, kind text NOT NULL CHECK(kind IN ('proposed_application','documented_external_reference','eva_completed_project')),
 material_id text REFERENCES materials(id), industry_id text REFERENCES industries(id),
 source_url text, publication_status text NOT NULL DEFAULT 'draft',
 approved_for_portfolio boolean NOT NULL DEFAULT false,
 CHECK(NOT approved_for_portfolio OR kind='eva_completed_project')
);
CREATE TABLE example_assets (
 example_id text NOT NULL REFERENCES examples(id), asset_id uuid NOT NULL REFERENCES assets(id),
 PRIMARY KEY(example_id,asset_id)
);
CREATE TABLE users (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), email text NOT NULL,
 email_verified_at timestamptz, display_name text,
 preferred_locale text NOT NULL DEFAULT 'en' REFERENCES locales(code),
 role text NOT NULL DEFAULT 'customer' CHECK(role IN ('customer','engineer','admin')),
 active boolean NOT NULL DEFAULT true, created_at timestamptz NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX users_email_lower_unique ON users(lower(email));
CREATE TABLE auth_accounts (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 provider text NOT NULL, provider_subject text NOT NULL,
 UNIQUE(provider,provider_subject)
);
CREATE TABLE auth_credentials (
 user_id uuid PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
 password_hash text NOT NULL, changed_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE auth_tokens (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 token_hash text UNIQUE NOT NULL, purpose text NOT NULL CHECK(purpose IN ('email_verification','password_reset','session')),
 expires_at timestamptz NOT NULL, used_at timestamptz, created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE customer_companies (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), name text NOT NULL, vat_number text,
 billing_details jsonb NOT NULL DEFAULT '{}'
);
CREATE TABLE company_memberships (
 company_id uuid NOT NULL REFERENCES customer_companies(id), user_id uuid NOT NULL REFERENCES users(id),
 membership_role text NOT NULL DEFAULT 'member', PRIMARY KEY(company_id,user_id)
);
CREATE TABLE projects (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), owner_user_id uuid NOT NULL REFERENCES users(id),
 company_id uuid REFERENCES customer_companies(id), title text NOT NULL CHECK(length(trim(title)) BETWEEN 3 AND 200),
 description text NOT NULL, intended_use text NOT NULL,
 industry_id text REFERENCES industries(id), preferred_locale text NOT NULL DEFAULT 'en' REFERENCES locales(code),
 confidentiality text NOT NULL DEFAULT 'private' CHECK(confidentiality IN ('private','nda_requested')),
 target_date date, budget_currency text CHECK(budget_currency IS NULL OR budget_currency ~ '^[A-Z]{3}$'),
 budget_amount numeric CHECK(budget_amount IS NULL OR budget_amount>=0),
 status text NOT NULL DEFAULT 'draft' CHECK(status IN ('draft','submitted','needs_information','engineering_review','quoted','accepted','scheduled','printing','quality_check','ready','shipped','collected','delivered','cancelled')),
 requirements jsonb NOT NULL DEFAULT '{}', delivery_details jsonb NOT NULL DEFAULT '{}',
 created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE project_items (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), project_id uuid NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
 title text NOT NULL, quantity integer NOT NULL CHECK(quantity>0), units text NOT NULL DEFAULT 'mm' CHECK(units IN ('mm','cm','in')),
 preferred_material_id text REFERENCES materials(id), preferred_color_id uuid REFERENCES colors(id),
 multi_material_spec jsonb NOT NULL DEFAULT '[]', dimensions jsonb NOT NULL DEFAULT '{}',
 tolerances jsonb NOT NULL DEFAULT '{}', process_requirements jsonb NOT NULL DEFAULT '{}',
 created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE project_files (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), project_id uuid NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
 project_item_id uuid REFERENCES project_items(id) ON DELETE SET NULL,
 uploaded_by_user_id uuid NOT NULL REFERENCES users(id),
 original_filename text NOT NULL, object_key text UNIQUE NOT NULL,
 mime_type text NOT NULL, file_extension text NOT NULL, size_bytes bigint NOT NULL CHECK(size_bytes>0),
 checksum_sha256 text NOT NULL, revision integer NOT NULL DEFAULT 1 CHECK(revision>0),
 scan_status text NOT NULL DEFAULT 'quarantined' CHECK(scan_status IN ('quarantined','scanning','clean','blocked','failed')),
 document_role text NOT NULL DEFAULT 'reference', visibility text NOT NULL DEFAULT 'private' CHECK(visibility='private'),
 created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE project_events (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), project_id uuid NOT NULL REFERENCES projects(id),
 actor_user_id uuid REFERENCES users(id), kind text NOT NULL, customer_visible boolean NOT NULL DEFAULT true,
 body text, data jsonb NOT NULL DEFAULT '{}', created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE quotes (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), project_id uuid NOT NULL REFERENCES projects(id),
 revision integer NOT NULL CHECK(revision>0), currency text NOT NULL CHECK(currency ~ '^[A-Z]{3}$'),
 net_amount numeric(14,2) NOT NULL CHECK(net_amount>=0), tax_amount numeric(14,2) NOT NULL CHECK(tax_amount>=0),
 shipping_amount numeric(14,2) NOT NULL DEFAULT 0 CHECK(shipping_amount>=0),
 valid_until date NOT NULL, terms jsonb NOT NULL DEFAULT '{}',
 status text NOT NULL DEFAULT 'draft' CHECK(status IN ('draft','issued','accepted','declined','expired','superseded')),
 created_by uuid REFERENCES users(id), accepted_by uuid REFERENCES users(id), accepted_at timestamptz,
 created_at timestamptz NOT NULL DEFAULT now(), UNIQUE(project_id,revision)
);
CREATE TABLE production_jobs (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), project_item_id uuid NOT NULL REFERENCES project_items(id),
 printer_id text NOT NULL REFERENCES printers(id), material_id text NOT NULL REFERENCES materials(id),
 material_lot text, slicing_profile_ref text, operator_user_id uuid REFERENCES users(id),
 status text NOT NULL DEFAULT 'planned', planned_start timestamptz, started_at timestamptz, finished_at timestamptz,
 process_record jsonb NOT NULL DEFAULT '{}', quality_record jsonb NOT NULL DEFAULT '{}'
);
CREATE TABLE contact_messages (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), name text NOT NULL, email text NOT NULL,
 subject text NOT NULL, message text NOT NULL, locale text NOT NULL REFERENCES locales(code),
 delivery_status text NOT NULL DEFAULT 'queued', created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE consents (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), user_id uuid REFERENCES users(id),
 project_id uuid REFERENCES projects(id), consent_type text NOT NULL, version text NOT NULL,
 given boolean NOT NULL, recorded_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE notification_outbox (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), project_id uuid REFERENCES projects(id),
 recipient_user_id uuid REFERENCES users(id), template_key text NOT NULL,
 payload jsonb NOT NULL DEFAULT '{}', status text NOT NULL DEFAULT 'pending',
 attempt_count integer NOT NULL DEFAULT 0 CHECK(attempt_count>=0), next_attempt_at timestamptz,
 created_at timestamptz NOT NULL DEFAULT now(), sent_at timestamptz
);
CREATE TABLE audit_events (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), actor_user_id uuid REFERENCES users(id),
 action text NOT NULL, entity_type text NOT NULL, entity_id text,
 details jsonb NOT NULL DEFAULT '{}', created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX materials_family_status ON materials(family_code,service_status);
CREATE INDEX material_properties_gin ON materials USING gin(properties);
CREATE INDEX project_owner_status ON projects(owner_user_id,status);
CREATE INDEX project_files_project ON project_files(project_id,created_at);
CREATE INDEX project_events_project ON project_events(project_id,created_at);
CREATE INDEX outbox_pending ON notification_outbox(status,next_attempt_at);

-- Server middleware sets these transaction-local values only after validating the session.
-- Never allow browsers to connect to PostgreSQL or set these values directly.
CREATE FUNCTION current_actor() RETURNS uuid LANGUAGE sql STABLE AS
 $$ SELECT nullif(current_setting('app.user_id',true),'')::uuid $$;
CREATE FUNCTION actor_is_staff() RETURNS boolean LANGUAGE sql STABLE AS
 $$ SELECT coalesce(current_setting('app.staff',true)='true',false) $$;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects FORCE ROW LEVEL SECURITY;
CREATE POLICY project_access ON projects USING(owner_user_id=current_actor() OR actor_is_staff())
 WITH CHECK(owner_user_id=current_actor() OR actor_is_staff());
ALTER TABLE project_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE project_items FORCE ROW LEVEL SECURITY;
CREATE POLICY item_access ON project_items USING(EXISTS(SELECT 1 FROM projects p WHERE p.id=project_id))
 WITH CHECK(EXISTS(SELECT 1 FROM projects p WHERE p.id=project_id));
ALTER TABLE project_files ENABLE ROW LEVEL SECURITY;
ALTER TABLE project_files FORCE ROW LEVEL SECURITY;
CREATE POLICY file_access ON project_files USING(EXISTS(SELECT 1 FROM projects p WHERE p.id=project_id))
 WITH CHECK(EXISTS(SELECT 1 FROM projects p WHERE p.id=project_id) AND (uploaded_by_user_id=current_actor() OR actor_is_staff()));
ALTER TABLE project_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE project_events FORCE ROW LEVEL SECURITY;
CREATE POLICY event_access ON project_events USING(EXISTS(SELECT 1 FROM projects p WHERE p.id=project_id) AND (customer_visible OR actor_is_staff()))
 WITH CHECK(actor_is_staff());
ALTER TABLE quotes ENABLE ROW LEVEL SECURITY;
ALTER TABLE quotes FORCE ROW LEVEL SECURITY;
CREATE POLICY quote_access ON quotes USING(EXISTS(SELECT 1 FROM projects p WHERE p.id=project_id) AND (status<>'draft' OR actor_is_staff()))
 WITH CHECK(actor_is_staff());

-- Cross-item references cannot point to another project.
CREATE FUNCTION file_item_project_matches() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 IF NEW.project_item_id IS NOT NULL AND NOT EXISTS (
   SELECT 1 FROM project_items WHERE id=NEW.project_item_id AND project_id=NEW.project_id
 ) THEN RAISE EXCEPTION 'File item must belong to the same project'; END IF;
 RETURN NEW;
END $$;
CREATE TRIGGER project_file_item_check BEFORE INSERT OR UPDATE OF project_id,project_item_id ON project_files
 FOR EACH ROW EXECUTE FUNCTION file_item_project_matches();

-- Do not grant broad access to auth_credentials, auth_tokens, billing, contact or audit tables.
-- The deployment migration must explicitly grant table privileges to the service roles.
COMMIT;
