"""Author verification fixtures; independent audit and iOS hardware tests remain separate.
Requires jsonschema==4.26.0; no production database is opened.
"""
import copy
import datetime
import hashlib
import json
import pathlib
import sqlite3
import tempfile
from importlib.metadata import version
import jsonschema

ROOT = pathlib.Path(__file__).resolve().parents[1]
schema_path = ROOT / '03_contracte/project.schema.json'
sql_path = ROOT / '03_contracte/local_schema.sql'
schema = json.loads(schema_path.read_text(encoding='utf-8'))
jsonschema.Draft202012Validator.check_schema(schema)
validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
checks = []


def check(name, function):
    try:
        function()
        checks.append({'id': name, 'status': 'passed'})
    except Exception as error:
        checks.append({'id': name, 'status': 'failed', 'error': str(error)})


def demand(condition):
    if not condition:
        raise AssertionError('Expected condition was false')


def semantic(document):
    """Partial domain validator: reference graph, IDs, CAS path, time, poses.
    Does not read/hash payload files or establish physical calibration quality.
    """
    validator.validate(document)
    assets = {a['sha256']: a for a in document['assets']}
    demand(len(assets) == len(document['assets']))
    for a in document['assets']:
        demand(a['cas_path'] == f"cas/{a['sha256'][:2]}/{a['sha256']}")
    for collection, key in [('calibrations', 'calibration_id'), ('rooms', 'room_id'), ('objects', 'object_id')]:
        demand(len({item[key] for item in document[collection]}) == len(document[collection]))
    for calibration in document['calibrations']:
        demand(calibration['artifact_sha256'] in assets)
    rooms = {room['room_id'] for room in document['rooms']}
    for room in document['rooms']:
        demand(room['geometry_sha256'] in assets)
        demand(int(room['revision']) <= int(document['revision']))
    for obj in document['objects']:
        demand(obj['model_sha256'] in assets)
        demand(obj['room_id'] is None or obj['room_id'] in rooms)
        demand(int(obj['revision']) <= int(document['revision']))
    for pose in [r['project_from_room'] for r in document['rooms']] + [o['pose'] for o in document['objects']]:
        demand(abs(sum(x*x for x in pose['quaternion_xyzw']) - 1.0) < 1e-6)
    demand(datetime.datetime.fromisoformat(document['updated_at']) >= datetime.datetime.fromisoformat(document['created_at']))


def reject(document, domain=False):
    try:
        (semantic if domain else validator.validate)(document)
    except (jsonschema.ValidationError, AssertionError, ValueError):
        return
    raise AssertionError('Invalid fixture accepted')


sample = {
    'schema_version': 'eva-project/1',
    'project_id': '11111111-2222-4333-8444-555555555555',
    'title': 'Synthetic fixture', 'kind': 'object_persistent', 'state': 'processed',
    'units': 'm', 'created_at': '2026-10-02T00:00:00Z',
    'updated_at': '2026-10-02T00:00:01Z', 'revision': '1',
    'calibrations': [{'calibration_id': 'cal-1', 'hardware_profile': 'fixture-only', 'revision': '0', 'artifact_sha256': 'a'*64, 'created_at': '2026-10-02T00:00:00Z'}],
    'assets': [{'sha256': 'a'*64, 'byte_length': '1', 'media_type': 'application/json', 'cas_path': 'cas/aa/'+'a'*64}],
    'rooms': [],
    'objects': [{'object_id': 'obj-1', 'name': 'Synthetic', 'model_sha256': 'a'*64, 'room_id': None, 'revision': '1', 'frame_id': 'project', 'state': 'observed', 'ambiguity_status': 'none', 'pose': {'translation_m': [0,0,0], 'quaternion_xyzw': [0,0,0,1]}}]
}
check('JSON-01-valid-processed-project', lambda: semantic(sample))
for label, key, value in [
    ('overflow', 'revision', '9223372036854775808'),
    ('leading-zero', 'revision', '01'),
    ('negative', 'revision', '-1'),
    ('live-kind', 'kind', 'live_ephemeral'),
    ('wrong-unit', 'units', 'mm'),
    ('invalid-date', 'created_at', '2026-99-02T00:00:00Z'),
    ('empty-processed-assets', 'assets', []),
    ('unknown-property', 'surprise', 1),
]:
    fixture = copy.deepcopy(sample); fixture[key] = value
    check('JSON-negative-'+label, lambda f=fixture: reject(f))
maximum = copy.deepcopy(sample); maximum['revision'] = '9223372036854775807'
check('JSON-max-Int64-accepted', lambda: semantic(maximum))
for label, change in [
    ('missing-asset-ref', lambda f: f['objects'][0].update(model_sha256='b'*64)),
    ('missing-room-ref', lambda f: f['objects'][0].update(room_id='absent')),
    ('duplicate-object', lambda f: f['objects'].append(copy.deepcopy(f['objects'][0]))),
    ('nonunit-quaternion', lambda f: f['objects'][0]['pose'].update(quaternion_xyzw=[0,0,0,2])),
    ('wrong-CAS-prefix', lambda f: f['assets'][0].update(cas_path='cas/bb/'+'a'*64)),
    ('future-object-revision', lambda f: f['objects'][0].update(revision='2')),
]:
    fixture = copy.deepcopy(sample); change(fixture)
    check('DOMAIN-negative-'+label, lambda f=fixture: reject(f, domain=True))

with tempfile.TemporaryDirectory(prefix='eva-ios-fixture-') as directory:
    db = sqlite3.connect(str(pathlib.Path(directory)/'fixture.sqlite'))
    db.executescript(sql_path.read_text(encoding='utf-8'))
    check('SQL-01-create-schema', lambda: demand(len(db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()) == 10))
    check('SQL-02-foreign-keys', lambda: demand(db.execute('PRAGMA foreign_keys').fetchone()[0] == 1))
    check('SQL-03-journal-delete', lambda: demand(db.execute('PRAGMA journal_mode').fetchone()[0] == 'delete'))
    check('SQL-04-synchronous-full', lambda: demand(db.execute('PRAGMA synchronous').fetchone()[0] == 2))
    db.execute("INSERT INTO projects VALUES(1,'fixture','fixture','object_persistent','draft','m','2026','2026',0)")
    db.execute("INSERT INTO blobs VALUES(?,1,'application/json','2026')", ('a'*64,))
    db.execute("INSERT INTO calibrations VALUES('cal-1','fixture',0,?,'2026')", ('a'*64,))
    db.execute("INSERT INTO revisions VALUES(0,?,'cal-1',NULL,'2026')", ('a'*64,))
    db.commit()

    def reject_sql(sql, params=()):
        db.execute('SAVEPOINT fixture')
        rejected = False
        try:
            db.execute(sql, params)
        except sqlite3.IntegrityError:
            rejected = True
        finally:
            db.execute('ROLLBACK TO fixture'); db.execute('RELEASE fixture')
        demand(rejected)

    check('SQL-negative-FK', lambda: reject_sql("INSERT INTO revisions VALUES(1,?,'missing',0,'2026')", ('a'*64,)))
    check('SQL-negative-live-kind', lambda: reject_sql("UPDATE projects SET kind='live_ephemeral'"))
    check('SQL-negative-second-project', lambda: reject_sql("INSERT INTO projects VALUES(2,'second','fixture','object_persistent','draft','m','2026','2026',0)"))
    check('SQL-negative-blob-length', lambda: reject_sql("INSERT INTO blobs VALUES(?,-1,'x','2026')", ('b'*64,)))
    check('SQL-negative-hash', lambda: reject_sql("INSERT INTO blobs VALUES('bad',1,'x','2026')"))
    job_insert = "INSERT INTO jobs(job_id,kind,input_revision,parameters_sha256,algorithm_version,idempotency_key,state,created_at,updated_at) VALUES(?, 'export',0,?,'v1',?,?,'2026','2026')"
    check('SQL-negative-completed-no-output', lambda: reject_sql(job_insert, ('j1','b'*64,'c'*64,'completed')))
    check('SQL-negative-running-no-lease', lambda: reject_sql(job_insert, ('j1','b'*64,'c'*64,'running')))
    db.execute(job_insert, ('j1','b'*64,'c'*64,'queued')); db.commit()
    check('SQL-negative-idempotency-duplicate', lambda: reject_sql(job_insert, ('j2','b'*64,'c'*64,'queued')))
    db.execute('BEGIN'); db.execute("UPDATE projects SET title='interrupted'"); db.rollback()
    check('SQL-rollback-keeps-title', lambda: demand(db.execute('SELECT title FROM projects').fetchone()[0]=='fixture'))
    check('SQL-integrity-and-FK', lambda: demand(db.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and db.execute('PRAGMA foreign_key_check').fetchall()==[]))
    db.close()

report = {
    'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'actor': 'ios_cv_designer', 'kind': 'author_contract_verification',
    'runtime': {'sqlite': sqlite3.sqlite_version, 'jsonschema': version('jsonschema')},
    'inputs': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in [schema_path, sql_path, pathlib.Path(__file__)]},
    'checks': checks, 'passed': sum(c['status']=='passed' for c in checks), 'total': len(checks),
    'limitations': ['Swift not compiled', 'No iPhone/Thor hardware run', 'Synthetic fixtures only', 'Domain validator does not hash payload files or certify calibration', 'SQLite on host is not SQLite on iOS']
}
(ROOT/'08_jurnale/ios_contract_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'passed':report['passed'],'total':report['total'],'failed':[c for c in checks if c['status']=='failed']}))
raise SystemExit(0 if report['passed']==report['total'] else 1)
