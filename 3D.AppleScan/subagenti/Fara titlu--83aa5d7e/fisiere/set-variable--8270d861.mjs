import { parseArgs } from 'node:util';
import { withPool, isMain, fail } from './shared.mjs';

export function parseVariableValue(raw) {
  const value = JSON.parse(raw);
  if (!['string', 'number', 'boolean'].includes(typeof value) || (typeof value === 'number' && !Number.isFinite(value))) throw new Error('Variable must be a JSON string, finite number, or boolean');
  if (Buffer.byteLength(JSON.stringify(value), 'utf8') > 16384) throw new Error('Variable exceeds the 16 KiB limit');
  return value;
}

export async function setVariable(db, key, value) {
  if (typeof key !== 'string' || !key.length || key.length > 200) throw new Error('Variable key must contain 1 to 200 characters');
  const json = JSON.stringify(value);
  parseVariableValue(json);
  const result = await db.query(`INSERT INTO content_variables(key,value) VALUES($1,$2::jsonb)
    ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=now()
    WHERE content_variables.value IS DISTINCT FROM excluded.value`, [key, json]);
  return { key, changed: result.rowCount };
}

if (isMain(import.meta.url)) {
  try {
    const { values } = parseArgs({ options: { key: { type: 'string' }, value: { type: 'string' } }, strict: true });
    if (!values.key || values.value === undefined) throw new Error('Usage: node scripts/set-variable.mjs --key docsPages --value 89');
    const value = parseVariableValue(values.value);
    await withPool(async db => console.log(JSON.stringify({ event: 'variable_updated', ...await setVariable(db, values.key, value) })));
  } catch (error) { fail(error); }
}
