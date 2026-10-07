import { withPool, migrate, importSeeds, readSeeds, fail } from './shared.mjs';
import { seedAppI18n } from './seed-app-i18n.mjs';
await withPool(async db => {
  await migrate(db);
  const result = await importSeeds(db, await readSeeds(), { initialOnly: true });
  const i18n = await seedAppI18n(db);
  console.log(JSON.stringify({ event: 'bootstrap', ...result, appI18nChanged: i18n.changed }));
}).catch(fail);
