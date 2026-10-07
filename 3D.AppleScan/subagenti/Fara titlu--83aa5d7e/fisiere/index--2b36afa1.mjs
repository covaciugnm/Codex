import { ContentStore } from './content.mjs';
import { AuthStore } from './auth.mjs';
import { ProjectStore } from './projects.mjs';
import { AppI18nStore } from './appI18n.mjs';
import { createApp } from './http.mjs';
const store = new ContentStore();
const authStore = new AuthStore();
const projectStore = new ProjectStore();
const appI18nStore = new AppI18nStore();
const server = createApp({ store, authStore, projectStore, appI18nStore });
await store.listen();
server.listen(Number(process.env.PORT || 3000), '0.0.0.0', () => console.log(JSON.stringify({ event: 'listening', port: Number(process.env.PORT || 3000) })));
let stopping = false;
async function stop() {
  if (stopping) return;
  stopping = true;
  const timeout = setTimeout(() => process.exit(1), 10000).unref();
  server.closeEvents();
  server.close(async () => { await store.close(); await authStore.close(); await projectStore.close(); await appI18nStore.close(); clearTimeout(timeout); });
}
process.on('SIGTERM', stop);
process.on('SIGINT', stop);
