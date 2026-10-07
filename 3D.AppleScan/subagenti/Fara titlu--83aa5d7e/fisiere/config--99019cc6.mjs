export const locales = Object.freeze(['en', 'de', 'fr', 'es', 'ro', 'hu', 'bg']);
export const variables = Object.freeze({ product: 'EVA 3D Scan', languages: 7, modules: 3, docsPages: 89 });
export function normalizeLocale(value) {
  const candidate = String(value || 'en').toLowerCase();
  if (candidate === 'sp') return 'es';
  return locales.includes(candidate) ? candidate : 'en';
}
export function databaseConfig(env = process.env) {
  const common = { connectionTimeoutMillis: 5000, statement_timeout: 5000, query_timeout: 6000, application_name: 'eva-presentation' };
  if (env.DATABASE_URL) return { ...common, connectionString: env.DATABASE_URL };
  return { ...common, host: env.PGHOST || 'db', port: Number(env.PGPORT || 5432), database: env.PGDATABASE || 'eva_site', user: env.PGUSER || 'eva_site', password: env.PGPASSWORD };
}
