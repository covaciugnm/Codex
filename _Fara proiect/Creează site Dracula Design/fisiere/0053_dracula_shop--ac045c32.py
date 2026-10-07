"""Dracula extensions; upstream CESIRO migrations remain intact."""
from alembic import op
revision='0053_dracula_shop'
down_revision='0052_products_warehouse_meta'
branch_labels=None
depends_on=None

def upgrade():
    op.execute("ALTER DOMAIN core.locale_code DROP CONSTRAINT locale_code_check")
    op.execute("ALTER DOMAIN core.locale_code ADD CONSTRAINT locale_code_check CHECK (VALUE ~ '^[a-z]{2,3}(-[A-Za-z0-9]{2,8})*$')")
    op.execute('ALTER TABLE sales.orders ADD COLUMN IF NOT EXISTS is_test boolean NOT NULL DEFAULT false')
    op.execute('''CREATE TABLE sales.dracula_checkout_requests (
      tenant_id uuid NOT NULL REFERENCES core.tenants(id), user_id uuid NOT NULL REFERENCES identity.users(id),
      request_key text NOT NULL, request_hash text NOT NULL, result jsonb NOT NULL,
      created_at timestamptz NOT NULL DEFAULT now(), PRIMARY KEY(tenant_id,user_id,request_key))''')
    op.execute('ALTER TABLE sales.dracula_checkout_requests ENABLE ROW LEVEL SECURITY')
    op.execute('''CREATE POLICY own_request ON sales.dracula_checkout_requests
      USING(tenant_id=core.current_tenant_id() AND user_id=NULLIF(current_setting('app.user_id',true),'')::uuid)
      WITH CHECK(tenant_id=core.current_tenant_id() AND user_id=NULLIF(current_setting('app.user_id',true),'')::uuid)''')
    op.execute('GRANT SELECT,INSERT ON sales.dracula_checkout_requests TO eva_storefront')
    op.execute('GRANT ALL ON sales.dracula_checkout_requests TO eva_admin_api')
    op.execute('''CREATE TABLE cms.dracula_inquiries (
      id uuid PRIMARY KEY DEFAULT gen_random_uuid(),tenant_id uuid NOT NULL REFERENCES core.tenants(id),
      user_id uuid,kind text NOT NULL,name text NOT NULL,email text NOT NULL,body text NOT NULL,
      locale core.locale_code NOT NULL,status text NOT NULL DEFAULT 'new',created_at timestamptz NOT NULL DEFAULT now())''')
    op.execute('ALTER TABLE cms.dracula_inquiries ENABLE ROW LEVEL SECURITY')
    op.execute('''CREATE POLICY tenant_inquiry ON cms.dracula_inquiries
      USING(tenant_id=core.current_tenant_id() AND current_setting('app.admin',true)='on')
      WITH CHECK(tenant_id=core.current_tenant_id())''')
    op.execute('GRANT INSERT ON cms.dracula_inquiries TO eva_storefront')
    op.execute('GRANT ALL ON cms.dracula_inquiries TO eva_admin_api')

def downgrade():
    raise RuntimeError('Use a verified database backup to roll back the shop migration.')
