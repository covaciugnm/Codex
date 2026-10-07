import pg from 'pg';
import { EventEmitter } from 'node:events';
import { databaseConfig, normalizeLocale, variables } from './config.mjs';

export class ContentStore extends EventEmitter {
  constructor(config = databaseConfig()) {
    super();
    this.config = config;
    this.pool = new pg.Pool({ ...config, max: 10 });
    this.pool.on('error', error => this.report(error));
    this.cache = new Map();
    this.epoch = 0;
    this.connected = false;
    this.closed = false;
  }
  report(error) { console.error(JSON.stringify({ event: 'database_error', code: error.code || 'DATABASE_ERROR' })); }
  invalidate(revision) {
    this.epoch++;
    this.cache.clear();
    this.emit('content', { revision: String(revision) });
  }
  async revision() {
    const { rows } = await this.pool.query('SELECT revision::text FROM content_revision WHERE singleton');
    if (!rows.length) throw new Error('Content schema is not initialized');
    return rows[0].revision;
  }
  async ready() {
    await this.pool.query('SELECT 1 FROM content_revision WHERE singleton');
  }
  async get(requestedLocale) {
    const locale = normalizeLocale(requestedLocale);
    if (this.connected && this.cache.has(locale)) return this.cache.get(locale);
    const epoch = this.epoch;
    // One statement gives revision and messages the same PostgreSQL snapshot.
    const { rows } = await this.pool.query(`
      SELECT revision::text,
        COALESCE((SELECT jsonb_object_agg(key,value) FROM content_messages WHERE locale='en'),'{}'::jsonb)
        || COALESCE((SELECT jsonb_object_agg(key,value) FROM content_messages WHERE locale=$1),'{}'::jsonb) AS messages,
        COALESCE((SELECT jsonb_object_agg(key,value) FROM content_variables),'{}'::jsonb) AS variables,
        (SELECT count(*)::int FROM content_messages WHERE locale='en') AS base_count
      FROM content_revision WHERE singleton`, [locale]);
    if (!rows.length || !rows[0].base_count) throw new Error('English content is not initialized');
    for (const [key, value] of Object.entries(rows[0].variables)) {
      if (!['string', 'number', 'boolean'].includes(typeof value) || (typeof value === 'number' && !Number.isFinite(value))) {
        throw new Error(`Variable ${key} is not a finite JSON scalar`);
      }
    }
    const bundle = { locale, revision: rows[0].revision, variables: { ...variables, ...rows[0].variables }, messages: rows[0].messages };
    if (this.connected && epoch === this.epoch) this.cache.set(locale, bundle);
    return bundle;
  }
  async listen() {
    if (this.closed) return;
    const client = new pg.Client(this.config);
    this.listener = client;
    let failed = false;
    const reconnect = error => {
      if (failed || this.closed) return;
      failed = true;
      this.connected = false;
      this.cache.clear();
      this.epoch++;
      if (error) this.report(error);
      void client.end().catch(() => {});
      this.retry = setTimeout(() => void this.listen(), 2000);
      this.retry.unref();
    };
    client.on('error', reconnect);
    client.on('end', () => reconnect());
    client.on('notification', message => {
      if (message.channel === 'content_changed') this.invalidate(message.payload);
    });
    try {
      await client.connect();
      await client.query('LISTEN content_changed');
      this.connected = true;
      this.invalidate(await this.revision());
    } catch (error) { reconnect(error); }
  }
  async close() {
    this.closed = true;
    clearTimeout(this.retry);
    await this.listener?.end().catch(() => {});
    await this.pool.end();
  }
}
