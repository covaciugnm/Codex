import { parseArgs } from 'node:util';
import { locales } from '../server/config.mjs';
import { withPool, fail } from './shared.mjs';
try {
  const { values } = parseArgs({ options: { lang: { type: 'string' }, key: { type: 'string' }, value: { type: 'string' } }, strict: true });
  const lang = values.lang === 'sp' ? 'es' : values.lang;
  if (!locales.includes(lang) || !values.key || values.key.length > 200 || values.value === undefined) throw new Error('Usage: node scripts/set-content.mjs --lang ro --key hero.title --value "Text"');
  await withPool(async db => {
    const result = await db.query(`INSERT INTO content_messages(locale,key,value) VALUES($1,$2,$3)
      ON CONFLICT(locale,key) DO UPDATE SET value=excluded.value, updated_at=now()
      WHERE content_messages.value IS DISTINCT FROM excluded.value`, [lang, values.key, values.value]);
    console.log(JSON.stringify({ event: 'content_updated', locale: lang, key: values.key, changed: result.rowCount }));
  });
} catch (error) { fail(error); }
