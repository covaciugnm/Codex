import test from 'node:test';
import assert from 'node:assert/strict';
import { once } from 'node:events';
import { randomBytes } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import pg from 'pg';
import { ContentStore } from '../server/content.mjs';
import { locales, databaseConfig } from '../server/config.mjs';
import { migrate, importSeeds } from '../scripts/shared.mjs';
import { provisionRuntime } from '../scripts/provision-runtime.mjs';
import { setVariable } from '../scripts/set-variable.mjs';

test('PostgreSQL: atomic imports, persistence, SQL-trigger invalidation and fallback', { skip: !process.env.TEST_DATABASE_URL && process.env.TEST_PG !== '1' }, async t => {
  const schema = `eva_test_${randomBytes(8).toString('hex')}`;
  const ownerConfig = process.env.TEST_DATABASE_URL ? { connectionString: process.env.TEST_DATABASE_URL } : databaseConfig();
  const admin = new pg.Pool(ownerConfig);
  await admin.query(`CREATE SCHEMA ${schema}`);
  const config = { ...ownerConfig, options: `-c search_path=${schema}`, connectionTimeoutMillis: 5000 };
  const db = new pg.Pool(config);
  const store = new ContentStore(config);
  t.after(async () => {
    await store.close();
    await db.end();
    await admin.query(`DROP SCHEMA ${schema} CASCADE`);
    await admin.end();
  });
  await migrate(db);
  await migrate(db);
  const seeds = Object.fromEntries(locales.map(locale => [locale, { title: `Title ${locale}` }]));
  seeds.en['only.english'] = 'English fallback';
  assert.equal((await importSeeds(db, seeds, { initialOnly: true })).changed, 8);
  const firstRevision = await store.revision();
  assert.equal((await importSeeds(db, seeds)).changed, 0);
  assert.equal(await store.revision(), firstRevision, 'same import does not invalidate cache');
  await store.listen();
  const original = await store.get('ro');
  assert.equal(original.messages.title, 'Title ro');
  assert.equal(original.messages['only.english'], 'English fallback');
  const notification = once(store, 'content', { signal: AbortSignal.timeout(5000) });
  await db.query('UPDATE content_messages SET value=$1 WHERE locale=$2 AND key=$3', ['Edited directly in SQL', 'ro', 'title']);
  await notification;
  const edited = await store.get('ro');
  assert.equal(edited.messages.title, 'Edited directly in SQL');
  assert.notEqual(edited.revision, original.revision);
  const sameRevision = await store.revision();
  await db.query("UPDATE content_messages SET value=value WHERE locale='ro'");
  assert.equal(await store.revision(), sameRevision, 'no-op SQL update does not bump revision');
  assert.equal((await importSeeds(db, seeds, { initialOnly: true })).skipped, true);
  assert.equal((await store.get('ro')).messages.title, 'Edited directly in SQL', 'restart bootstrap preserves edits');
  const invalid = structuredClone(seeds);
  invalid.en.title = 'Must roll back';
  invalid.bg = { invalid: 123 };
  await assert.rejects(importSeeds(db, invalid));
  assert.equal((await store.get('en')).messages.title, 'Title en', 'failed import is atomic');
  assert.equal((await store.get('sp')).locale, 'es');
  const deletion = once(store, 'content', { signal: AbortSignal.timeout(5000) });
  await db.query("DELETE FROM content_messages WHERE locale='ro' AND key='title'");
  await deletion;
  assert.equal((await store.get('ro')).messages.title, 'Title en');
  assert.equal((await store.get('ro')).variables.docsPages, 89);
  const beforeVariableRevision = await store.revision();
  const variableNotification = once(store, 'content', { signal: AbortSignal.timeout(5000) });
  assert.equal((await setVariable(db, 'docsPages', 90)).changed, 1);
  await variableNotification;
  assert.equal((await store.get('ro')).variables.docsPages, 90, 'variable edits invalidate cached bundles');
  assert.notEqual(await store.revision(), beforeVariableRevision);
  const variableRevision = await store.revision();
  assert.equal((await setVariable(db, 'docsPages', 90)).changed, 0);
  assert.equal(await store.revision(), variableRevision, 'same variable value does not change revision');
  await migrate(db);
  assert.equal((await store.get('en')).variables.docsPages, 90, 'migration rerun preserves variable edits');
  const directVariableNotification = once(store, 'content', { signal: AbortSignal.timeout(5000) });
  await db.query("UPDATE content_variables SET value='91'::jsonb WHERE key='docsPages'");
  await directVariableNotification;
  assert.equal((await store.get('ro')).variables.docsPages, 91, 'direct SQL variable edit invalidates cache');
  await assert.rejects(db.query("INSERT INTO content_variables(key,value) VALUES('invalid','{}'::jsonb)"), { code: '23514' });
  for (const value of ['1e999', '-1e999']) {
    await assert.rejects(db.query('INSERT INTO content_variables(key,value) VALUES($1,$2::jsonb)', ['invalid.number', value]), { code: '23514' });
  }
  const upgradeClient = await db.connect();
  try {
    await upgradeClient.query('BEGIN');
    await upgradeClient.query('ALTER TABLE content_variables DROP CONSTRAINT content_variables_finite_number');
    await upgradeClient.query("INSERT INTO content_variables(key,value) VALUES('legacy.invalid','1e999'::jsonb)");
    await upgradeClient.query('SAVEPOINT before_upgrade');
    const migration003 = await readFile(new URL('../db/003-finite-variable-numbers.sql', import.meta.url), 'utf8');
    await assert.rejects(upgradeClient.query(migration003), error => error.code === '23514' && error.message.includes('legacy.invalid'));
    await upgradeClient.query('ROLLBACK TO SAVEPOINT before_upgrade');
    const unchanged = await upgradeClient.query("SELECT value='1e999'::jsonb AS preserved FROM content_variables WHERE key='legacy.invalid'");
    assert.equal(unchanged.rows[0].preserved, true, 'upgrade reports invalid legacy data without changing it');
  } finally {
    await upgradeClient.query('ROLLBACK');
    upgradeClient.release();
  }
  const maximumNotification = once(store, 'content', { signal: AbortSignal.timeout(5000) });
  await db.query("INSERT INTO content_variables(key,value) VALUES('maximum.number','1.7976931348623157e308'::jsonb),('minimum.number','-1.7976931348623157e308'::jsonb)");
  await maximumNotification;
  const finiteBundle = await store.get('en');
  assert.equal(finiteBundle.variables['maximum.number'], Number.MAX_VALUE);
  assert.equal(finiteBundle.variables['minimum.number'], -Number.MAX_VALUE);
  assert.equal(JSON.parse(JSON.stringify(finiteBundle)).variables['maximum.number'], Number.MAX_VALUE);
  const disconnected = new ContentStore(config);
  assert.equal((await disconnected.get('ro')).messages.title, 'Title en', 'new process reads persisted SQL state');
  assert.equal((await disconnected.get('ro')).variables.docsPages, 91, 'new process reads persisted variables');
  await disconnected.close();

  const role = `${schema}_reader`;
  const password = randomBytes(32).toString('hex');
  await provisionRuntime(db, { role, password });
  const connection = new pg.Client(config).connectionParameters;
  const reader = new ContentStore({ host: connection.host, port: connection.port, database: connection.database, ssl: connection.ssl, user: role, password, options: `-c search_path=${schema}` });
  try {
    await reader.listen();
    assert.equal(reader.connected, true, 'read-only login supports LISTEN');
    assert.equal((await reader.get('en')).messages.title, 'Title en');
    assert.equal((await reader.get('en')).variables.docsPages, 91, 'runtime role can read shared variables');
    const privileges = await reader.pool.query('SELECT rolsuper,rolcreatedb,rolcreaterole,rolreplication,rolbypassrls FROM pg_roles WHERE rolname=current_user');
    assert.deepEqual(Object.values(privileges.rows[0]), [false, false, false, false, false]);
    const connectionClient = await reader.pool.connect();
    try {
      // Disable the read-only default to verify actual SQL permissions still deny writes.
      await connectionClient.query('SET default_transaction_read_only=off');
      await assert.rejects(connectionClient.query("UPDATE content_messages SET value='forbidden'"), { code: '42501' });
      await assert.rejects(connectionClient.query("UPDATE content_variables SET value='0'::jsonb"), { code: '42501' });
      await assert.rejects(connectionClient.query('SELECT * FROM site_metadata'), { code: '42501' });
      await assert.rejects(connectionClient.query('CREATE TABLE forbidden(id int)'), { code: '42501' });
    } finally { connectionClient.release(); }
    const readerNotification = once(reader, 'content', { signal: AbortSignal.timeout(5000) });
    await db.query("UPDATE content_messages SET value='Reader sees notification' WHERE locale='en' AND key='title'");
    await readerNotification;
    assert.equal((await reader.get('en')).messages.title, 'Reader sees notification');
  } finally {
    await reader.close();
    await admin.query(`DROP OWNED BY "${role}"`);
    await admin.query(`DROP ROLE "${role}"`);
  }
});
