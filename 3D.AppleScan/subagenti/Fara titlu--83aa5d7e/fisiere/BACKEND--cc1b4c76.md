# Backend and content operations

Node.js 22 serves only `public/`. PostgreSQL 17 stores editable text. Production does not read seed JSON when answering requests. A failed database or missing English base content returns HTTP 503.

## Start

1. Copy `.env.example` to `.env` and replace both passwords with different random values of at least 24 characters. Preserve existing owner credentials when updating an existing deployment.
2. Run `docker compose up -d --build app`.
3. Point the existing reverse proxy at `127.0.0.1:4160`.

The database has no host port. Its data lives in the named `site_database` volume. Do not remove this volume to update the site. The application runs as the unprivileged Node user with a read-only filesystem. The production image excludes internal documentation, deploy artifacts, tests, and `.env`.

The one-shot `migrate` service explicitly runs `node scripts/bootstrap.mjs` and `node scripts/provision-runtime.mjs` with the owner credentials before HTTP starts. Bootstrap applies numbered migrations and seeds an empty database once. A persistent `initial_seed_complete` marker prevents subsequent starts from overwriting content, including deliberate deletions. Existing content without a marker is preserved. Applied migrations are checksum-verified: add a new numbered migration instead of editing a deployed one.

The long-running `app` service receives only `PGAPP_PASSWORD` through its `PGPASSWORD` variable and authenticates as `eva_site_runtime`. This LOGIN role has no superuser, database creation, role creation, replication or row-security bypass privileges. It receives only schema USAGE and SELECT on `content_messages`, `content_revision`, and `content_variables`, with read-only transactions by default. LISTEN/NOTIFY still works. Owner credentials exist only in the database and short-lived administrative `migrate`/`content` services; `app` never migrates or seeds. The `content` service is in the `tools` profile and runs only when explicitly invoked.

PostgreSQL `17.11-alpine` was selected against the [official supported-version table](https://www.postgresql.org/support/versioning/). Keep within the supported 17.x series when applying minor security updates and back up the volume first.

## API

ETags hash the complete response, including configuration variables. Deploying changed variables therefore invalidates the browser response even when the database revision is unchanged.

Static assets and HTML have filesystem-based weak ETags and Last-Modified headers. Matching conditional requests return 304 before the file payload is read. Assets revalidate on reuse, so deploying an updated file takes effect without waiting for a cache lifetime to expire. HEAD returns the same file metadata without reading or sending the body.

| Route | Behavior |
| --- | --- |
| `GET /api/content?lang=ro` | `{locale, revision, variables, messages}`; revision is a decimal string, messages is a flat string map. |
| `GET /api/events` | SSE `event: content` with JSON `{revision}` on connect and after committed text changes. Fetch the selected locale again. |
| `GET /healthz` | Process liveness. |
| `GET /readyz` | Queries the database; HTTP 503 when unavailable. |

Locales are `en`, `de`, `fr`, `es`, `ro`, `hu`, `bg`. `sp` aliases `es`. Missing or unsupported locale selects `en`; missing translated keys use English. The response always identifies the canonical locale and returns `Content-Language`. `variables` contains `product`, `languages`, `modules`, and `docsPages`. Text values may reference these variables; interpolation belongs to the frontend.

Each content response has an ETag and `Cache-Control: no-cache`; matching `If-None-Match` returns 304. PostgreSQL triggers advance a global revision for actual insert/update/delete changes and notify connected app instances after commit. A dedicated `LISTEN` connection invalidates memory caches and broadcasts SSE. Reconnection clears all caches and sends the latest revision. While that connection is down, reads bypass the memory cache. A no-op import/update keeps the revision unchanged. `TRUNCATE` invalidates content too.

The proxy must support long-lived SSE connections and disable response buffering for `/api/events`. The app sends `X-Accel-Buffering: no` and a heartbeat every 25 seconds. The frontend should refetch after reconnect or when the page becomes visible.

## Edit text without a rebuild

Run from the project folder:

```sh
docker compose run --rm content node scripts/set-content.mjs --lang ro --key hero.title --value 'Text nou'
```

Or use a parameterized SQL update through an authorized database console:

```sql
UPDATE content_messages
SET value = 'Text nou', updated_at = now()
WHERE locale = 'ro' AND key = 'hero.title';
```

Connected browsers receive the revision event immediately after commit. There is no public editing API. Database access and command execution remain administrative operations.

## Edit shared variables without a rebuild

Variables live in `content_variables`, independently of translated messages. Migration `002-content-variables.sql` adds initial defaults with `ON CONFLICT DO NOTHING`; later migrations, imports and restarts preserve edits. The API reads variables and translated messages in the same database snapshot. Configuration defaults fill missing variable keys only; a database error still returns 503. Inserts, changed updates, deletes and truncates use the same revision and notification mechanism as text changes.

```sh
docker compose run --rm content node scripts/set-variable.mjs --key docsPages --value 89
docker compose run --rm content node scripts/set-variable.mjs --key product --value '"EVA 3D Scan"'
```

`--value` must be valid JSON: a string in double quotes, a finite number, or a boolean. Objects, arrays, null and values exceeding 16 KiB are rejected. The outer single quotes in the string example are shell quoting; the inner double quotes are part of JSON. Values retain their JSON types in the API. Repeating a value is a no-op. Direct SQL updates to `content_variables` notify browsers after commit as well. Runtime credentials cannot write variables.

After deploying this upgrade, run the normal Compose deployment to apply migration 002 and grant the runtime role SELECT on the new table. Keep the existing volume and `.env` passwords. Existing variable values are never overwritten by the default seed.

Migration 003 also constrains numeric values to the finite JavaScript range, including edits made directly in SQL. If an existing variable exceeds that range, migration stops and names its key; explicitly correct that value and rerun the migration. No data is silently changed. The runtime rejects nonfinite or nonscalar values instead of serializing them as null.

## Explicit import

```sh
docker compose run --rm content node scripts/import-content.mjs
```

This intentionally imports the seven JSON files packaged into the image. Matching keys are overwritten only when values differ. Additional database keys are preserved. Repeating the same import makes no changes. All locales are validated and imported in one transaction. To import files outside the image, mount an approved directory and use `--dir /path/to/locales`. JSON files can be flat string maps or `{ "messages": { ... } }`.

Outside Docker, scripts accept `DATABASE_URL` or the standard `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, and `PGPASSWORD` environment variables. For a new database, run `npm run bootstrap`; `npm start` itself never seeds or migrates.

## Validation

`npm test` covers HTTP behavior and locale/content validation. Setting `TEST_DATABASE_URL` or `TEST_PG=1` enables real PostgreSQL tests; the latter uses the existing PG environment variables. They create a uniquely named schema and temporary reader role, test transactional imports, restart preservation, real SQL notification invalidation, English fallback, read-only permissions and LISTEN, then remove test resources. The administrative test role needs schema and role creation permissions.

On the Docker host, run all tests against the real database without placing credentials in the command:

```sh
docker compose run --rm -e TEST_PG=1 -v "$PWD/tests:/app/tests:ro" content npm test
```

The test directory is mounted only for this run and is not shipped in the production image. Use `docker compose logs migrate` to inspect migration/provision results, and `docker compose ps` to verify health. Password rotation requires rerunning `migrate` and recreating `app` with the corresponding environment; editing `.env` alone does not rotate the database owner's password on an existing volume.

The public routes `/objects`, `/measure`, `/spaces`, `/technology`, `/documentation`, and `/about` all serve the SPA entry page. Unrecognized paths return 404. Resolved files and symlink targets must stay inside `public/`; internal source files are not reachable over HTTP. Only GET and HEAD are accepted.
