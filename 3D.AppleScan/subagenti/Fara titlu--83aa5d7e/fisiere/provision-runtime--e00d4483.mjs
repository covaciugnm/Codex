import { withPool, transaction, isMain, fail } from './shared.mjs';

export async function provisionRuntime(db, { password = process.env.PGAPP_PASSWORD, role = 'eva_site_runtime' } = {}) {
  if (!password || password.length < 24 || /^REPLACE/i.test(password)) throw new Error('PGAPP_PASSWORD must be a new random password of at least 24 characters');
  if (password === process.env.PGPASSWORD) throw new Error('PGAPP_PASSWORD must differ from the owner password');
  if (!/^[a-z][a-z0-9_]{0,62}$/.test(role)) throw new Error('Invalid runtime role name');
  return transaction(db, async client => {
    await client.query('SELECT pg_advisory_xact_lock(71834203)');
    const existing = await client.query('SELECT 1 FROM pg_roles WHERE rolname=$1', [role]);
    if (!existing.rowCount) await client.query(`CREATE ROLE "${role}" NOLOGIN`);
    // Ask PostgreSQL to quote the password; it never appears in command output.
    const statement = await client.query("SELECT format('ALTER ROLE %I LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOREPLICATION NOBYPASSRLS PASSWORD %L', $1::text, $2::text) AS sql", [role, password]);
    await client.query(statement.rows[0].sql);
    const memberships = await client.query('SELECT parent.rolname FROM pg_auth_members membership JOIN pg_roles parent ON parent.oid=membership.roleid JOIN pg_roles member ON member.oid=membership.member WHERE member.rolname=$1', [role]);
    for (const { rolname } of memberships.rows) {
      const revoke = await client.query("SELECT format('REVOKE %I FROM %I', $1::text, $2::text) AS sql", [rolname, role]);
      await client.query(revoke.rows[0].sql);
    }
    await client.query(`ALTER ROLE "${role}" SET default_transaction_read_only = on`);
    const permissions = await client.query(`SELECT format(
      'REVOKE ALL ON SCHEMA %I FROM %I; GRANT USAGE ON SCHEMA %I TO %I; REVOKE ALL ON ALL TABLES IN SCHEMA %I FROM %I; REVOKE ALL ON ALL SEQUENCES IN SCHEMA %I FROM %I; GRANT SELECT ON content_messages, content_revision, content_variables TO %I; GRANT SELECT, INSERT, UPDATE, DELETE ON users, user_sessions TO %I; GRANT SELECT, INSERT, UPDATE, DELETE ON projects TO %I; GRANT SELECT ON app_i18n TO %I',
      current_schema(), $1::text, current_schema(), $1::text, current_schema(), $1::text, current_schema(), $1::text, $1::text, $1::text, $1::text, $1::text) AS sql`, [role]);
    await client.query(permissions.rows[0].sql);
    return { role };
  });
}

if (isMain(import.meta.url)) {
  await withPool(async db => console.log(JSON.stringify({ event: 'runtime_role_ready', ...await provisionRuntime(db) }))).catch(fail);
}
