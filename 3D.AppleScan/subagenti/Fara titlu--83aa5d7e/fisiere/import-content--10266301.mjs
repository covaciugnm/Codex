import { parseArgs } from 'node:util';
import { resolve } from 'node:path';
import { withPool, importSeeds, readSeeds, root, fail } from './shared.mjs';
try {
  const { values } = parseArgs({ options: { dir: { type: 'string' } }, strict: true });
  const seeds = await readSeeds(values.dir ? resolve(values.dir) : resolve(root, 'content/locales'));
  await withPool(async db => console.log(JSON.stringify({ event: 'content_imported', ...await importSeeds(db, seeds) })));
} catch (error) { fail(error); }
