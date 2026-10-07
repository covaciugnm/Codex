import { readFile, readdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';
import pg from 'pg';
import { databaseConfig, locales } from '../server/config.mjs';

export const root = fileURLToPath(new URL('../', import.meta.url));
export function pool() { return new pg.Pool({ ...databaseConfig(), max: 2 }); }
export function isMain(meta) { return process.argv[1] && fileURLToPath(meta) === resolve(process.argv[1]); }
export async function withPool(callback) {
  const db = pool();
  try { return await callback(db); } finally { await db.end(); }
}
export async function transaction(db, callback) {
  const client = await db.connect();
  try {
    await client.query('BEGIN');
    const value = await callback(client);
    await client.query('COMMIT');
    return value;
  } catch (error) { await client.query('ROLLBACK'); throw error; }
  finally { client.release(); }
}
export async function migrate(db) {
  return transaction(db, async client => {
    await client.query('SELECT pg_advisory_xact_lock(71834201)');
    await client.query('CREATE TABLE IF NOT EXISTS schema_migrations (name text PRIMARY KEY, checksum text NOT NULL, applied_at timestamptz NOT NULL DEFAULT now())');
    const files = (await readdir(resolve(root, 'db'))).filter(name => /^\d+.*\.sql$/.test(name)).sort();
    for (const name of files) {
      const sql = await readFile(resolve(root, 'db', name), 'utf8');
      const checksum = createHash('sha256').update(sql).digest('hex');
      const existing = await client.query('SELECT checksum FROM schema_migrations WHERE name=$1', [name]);
      if (existing.rows.length) {
        if (existing.rows[0].checksum !== checksum) throw new Error(`Applied migration changed: ${name}`);
        continue;
      }
      await client.query(sql);
      await client.query('INSERT INTO schema_migrations(name,checksum) VALUES($1,$2)', [name, checksum]);
      console.log(JSON.stringify({ event: 'migration_applied', name }));
    }
  });
}
export function validateMessages(input, locale) {
  const messages = input?.messages || input;
  if (!messages || Array.isArray(messages) || typeof messages !== 'object' || !Object.keys(messages).length) throw new Error(`Empty or invalid content for ${locale}`);
  for (const [key, value] of Object.entries(messages)) {
    if (!key.length || key.length > 200 || typeof value !== 'string') throw new Error(`Invalid string message ${locale}:${key}`);
  }
  return messages;
}
export async function readSeeds(directory = resolve(root, 'content/locales')) {
  const result = {};
  for (const locale of locales) result[locale] = validateMessages(JSON.parse(await readFile(resolve(directory, `${locale}.json`), 'utf8')), locale);
  return result;
}
export async function importSeeds(db, seeds, { initialOnly = false } = {}) {
  return transaction(db, async client => {
    await client.query('SELECT pg_advisory_xact_lock(71834202)');
    if (initialOnly) {
      const existing = await client.query("SELECT 1 FROM site_metadata WHERE key='initial_seed_complete'");
      if (existing.rowCount) return { skipped: true, changed: 0 };
      const content = await client.query('SELECT 1 FROM content_messages LIMIT 1');
      if (content.rowCount) {
        await client.query("INSERT INTO site_metadata(key,value) VALUES('initial_seed_complete','existing-content-preserved') ON CONFLICT DO NOTHING");
        return { skipped: true, changed: 0 };
      }
    }
    let changed = 0;
    for (const locale of locales) {
      for (const [key, value] of Object.entries(validateMessages(seeds[locale], locale))) {
        const result = await client.query(`INSERT INTO content_messages(locale,key,value) VALUES($1,$2,$3)
          ON CONFLICT(locale,key) DO UPDATE SET value=excluded.value, updated_at=now()
          WHERE content_messages.value IS DISTINCT FROM excluded.value`, [locale, key, value]);
        changed += result.rowCount;
      }
    }
    await client.query("INSERT INTO site_metadata(key,value) VALUES('initial_seed_complete','true') ON CONFLICT DO NOTHING");
    return { skipped: false, changed };
  });
}
export function fail(error) {
  console.error(JSON.stringify({ event: 'command_failed', message: error.message, code: error.code }));
  process.exitCode = 1;
}
