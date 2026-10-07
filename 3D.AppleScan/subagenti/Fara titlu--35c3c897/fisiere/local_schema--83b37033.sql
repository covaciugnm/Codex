-- Proposed local schema, one database per project. No user capture data.
-- Single connection owned by PersistenceActor. Verify these PRAGMAs after open.
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = DELETE;
PRAGMA synchronous = FULL;
PRAGMA busy_timeout = 250;
BEGIN IMMEDIATE;
CREATE TABLE schema_migrations (
  version INTEGER PRIMARY KEY CHECK(version > 0),
  applied_at TEXT NOT NULL, migration_sha256 TEXT NOT NULL CHECK(length(migration_sha256)=64 AND migration_sha256 NOT GLOB '*[^0-9a-f]*')
);
CREATE TABLE projects (
  singleton INTEGER PRIMARY KEY CHECK(singleton=1),
  project_id TEXT NOT NULL UNIQUE,
  title TEXT NOT NULL CHECK(length(title) BETWEEN 1 AND 200),
  kind TEXT NOT NULL CHECK(kind IN ('object_persistent','rooms_persistent')),
  state TEXT NOT NULL CHECK(state IN ('draft','captured','processed')),
  units TEXT NOT NULL DEFAULT 'm' CHECK(units='m'),
  created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
  current_revision INTEGER NOT NULL DEFAULT 0 CHECK(current_revision>=0)
);
CREATE TABLE blobs (
  sha256 TEXT PRIMARY KEY CHECK(length(sha256)=64 AND sha256 NOT GLOB '*[^0-9a-f]*'),
  byte_length INTEGER NOT NULL CHECK(typeof(byte_length)='integer' AND byte_length>=0),
  media_type TEXT NOT NULL CHECK(length(media_type) BETWEEN 1 AND 100),
  created_at TEXT NOT NULL
  -- CAS path derived exclusively from hash; no caller path accepted.
);
CREATE TABLE calibrations (
  calibration_id TEXT PRIMARY KEY CHECK(length(calibration_id) BETWEEN 1 AND 96),
  hardware_profile TEXT NOT NULL,
  revision INTEGER NOT NULL CHECK(revision>=0),
  artifact_sha256 TEXT NOT NULL REFERENCES blobs(sha256),
  created_at TEXT NOT NULL
);
CREATE TABLE revisions (
  revision INTEGER PRIMARY KEY CHECK(revision>=0),
  manifest_sha256 TEXT NOT NULL REFERENCES blobs(sha256),
  calibration_id TEXT NOT NULL REFERENCES calibrations(calibration_id),
  parent_revision INTEGER REFERENCES revisions(revision),
  created_at TEXT NOT NULL,
  CHECK(parent_revision IS NULL OR parent_revision < revision)
);
CREATE TABLE sessions (
  session_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL,
  calibration_id TEXT NOT NULL REFERENCES calibrations(calibration_id),
  -- Canonical decimal strings; full UInt64 range checked by application adapter.
  map_epoch TEXT NOT NULL CHECK(map_epoch='0' OR (length(map_epoch) BETWEEN 1 AND 20 AND substr(map_epoch,1,1) BETWEEN '1' AND '9' AND map_epoch NOT GLOB '*[^0-9]*')),
  clock_epoch TEXT NOT NULL CHECK(clock_epoch='0' OR (length(clock_epoch) BETWEEN 1 AND 20 AND substr(clock_epoch,1,1) BETWEEN '1' AND '9' AND clock_epoch NOT GLOB '*[^0-9]*')),
  started_at TEXT NOT NULL, ended_at TEXT
);
CREATE TABLE rooms (
  room_id TEXT PRIMARY KEY,
  name TEXT NOT NULL CHECK(length(name) BETWEEN 1 AND 200),
  revision INTEGER NOT NULL REFERENCES revisions(revision),
  geometry_sha256 TEXT NOT NULL REFERENCES blobs(sha256),
  frame_id TEXT NOT NULL,
  pose_artifact_sha256 TEXT NOT NULL REFERENCES blobs(sha256)
);
CREATE TABLE object_instances (
  object_id TEXT PRIMARY KEY,
  name TEXT NOT NULL CHECK(length(name) BETWEEN 1 AND 200),
  model_sha256 TEXT NOT NULL REFERENCES blobs(sha256),
  room_id TEXT REFERENCES rooms(room_id),
  revision INTEGER NOT NULL REFERENCES revisions(revision),
  frame_id TEXT NOT NULL,
  state TEXT NOT NULL CHECK(state IN ('observed','predicted','occluded','lost','retired')),
  ambiguity_status TEXT NOT NULL CHECK(ambiguity_status IN ('none','pose','identity','both')),
  pose_artifact_sha256 TEXT NOT NULL REFERENCES blobs(sha256)
);
CREATE TABLE jobs (
  job_id TEXT PRIMARY KEY,
  kind TEXT NOT NULL CHECK(kind IN ('reconstruct','fuse_rooms','export','thor_refine')),
  input_revision INTEGER NOT NULL REFERENCES revisions(revision),
  parameters_sha256 TEXT NOT NULL CHECK(length(parameters_sha256)=64 AND parameters_sha256 NOT GLOB '*[^0-9a-f]*'),
  algorithm_version TEXT NOT NULL,
  idempotency_key TEXT NOT NULL UNIQUE CHECK(length(idempotency_key)=64 AND idempotency_key NOT GLOB '*[^0-9a-f]*'),
  state TEXT NOT NULL CHECK(state IN ('queued','running','checkpointed','completed','failed','cancelled','needs_recapture')),
  attempt INTEGER NOT NULL DEFAULT 0 CHECK(attempt>=0),
  lease_owner TEXT, lease_expires_at TEXT,
  checkpoint_sha256 TEXT REFERENCES blobs(sha256),
  output_sha256 TEXT REFERENCES blobs(sha256),
  error_code TEXT,
  created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
  CHECK(state!='completed' OR output_sha256 IS NOT NULL),
  CHECK(state!='checkpointed' OR checkpoint_sha256 IS NOT NULL),
  CHECK(state!='running' OR (lease_owner IS NOT NULL AND lease_expires_at IS NOT NULL)),
  UNIQUE(kind,input_revision,parameters_sha256,algorithm_version)
);
CREATE TABLE events (
  event_id TEXT PRIMARY KEY,
  job_id TEXT REFERENCES jobs(job_id),
  utc_time TEXT NOT NULL,
  monotonic_ns TEXT NOT NULL,
  actor TEXT NOT NULL CHECK(length(actor)>0),
  event_type TEXT NOT NULL CHECK(length(event_type)>0),
  artifact_sha256 TEXT REFERENCES blobs(sha256),
  next_step TEXT NOT NULL CHECK(length(next_step)>0)
);
CREATE INDEX jobs_state_lease ON jobs(state,lease_expires_at);
CREATE INDEX objects_room ON object_instances(room_id);
CREATE INDEX events_job_time ON events(job_id,utc_time);
-- No migration row fabricated here: runner hashes the exact migration and logs
-- the real application time. Domain adapter validates UUIDs, timestamps, uint64
-- bounds, immutable calibration IDs, revision advancement and CAS content hashes.
COMMIT;
