"""Apply the supplied walnut and hazelnut products and collection imagery."""
import json,os
from pathlib import Path
from sqlalchemy import create_engine,text
from sqlalchemy.orm import Session
from seed_dracula import main
main()
content=json.loads((Path(__file__).parent/'dracula-content.json').read_text(encoding='utf-8'))
engine=create_engine(os.environ['SUPERUSER_DATABASE_URL'])
with Session(engine) as s,s.begin():
    for key in ('collection.description','collection.noresults'):
        s.execute(text('UPDATE core.ui_translations SET values=CAST(:v AS jsonb),updated_at=now() WHERE key=:k AND tenant_id=(SELECT id FROM core.tenants WHERE slug=:slug)'),{'v':json.dumps(content['ui'][key]),'k':key,'slug':os.environ['DEFAULT_TENANT']})
    s.execute(text("UPDATE core.tenant_settings SET settings=jsonb_set(settings,'{dracula_images}',CAST(:images AS jsonb)),updated_at=now() WHERE tenant_id=(SELECT id FROM core.tenants WHERE slug=:slug)"),{'images':json.dumps(content['images']),'slug':os.environ['DEFAULT_TENANT']})
engine.dispose()
print('Walnut and hazelnut products and collection imagery ready; existing accounts and orders preserved.')
