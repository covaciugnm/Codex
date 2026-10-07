import { withPool, migrate, fail } from './shared.mjs';
await withPool(migrate).catch(fail);
