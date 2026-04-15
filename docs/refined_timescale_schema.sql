-- Refined schema for a multi-tenant FinOps monitoring platform
-- Target: PostgreSQL + TimescaleDB

create extension if not exists timescaledb;
create extension if not exists citext;

create table organizations (
  id uuid primary key,
  name text not null,
  slug text not null unique,
  plan text not null default 'starter',
  status text not null default 'active',
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table users (
  id uuid primary key,
  organization_id uuid not null references organizations(id) on delete cascade,
  email citext not null,
  password_hash text not null,
  status text not null default 'active',
  profile jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (organization_id, email)
);

create table roles (
  id uuid primary key,
  organization_id uuid not null references organizations(id) on delete cascade,
  name text not null,
  description text,
  permissions jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now(),
  unique (organization_id, name)
);

create table user_roles (
  user_id uuid not null references users(id) on delete cascade,
  role_id uuid not null references roles(id) on delete cascade,
  primary key (user_id, role_id)
);

create table cloud_accounts (
  id uuid primary key,
  organization_id uuid not null references organizations(id) on delete cascade,
  provider text not null,
  account_id text not null,
  name text,
  credential_ref text,
  status text not null default 'active',
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (organization_id, provider, account_id)
);

create table resources (
  id uuid primary key,
  organization_id uuid not null references organizations(id) on delete cascade,
  cloud_account_id uuid references cloud_accounts(id) on delete set null,
  parent_resource_id uuid references resources(id) on delete set null,
  resource_type text not null,
  provider text not null,
  external_id text not null,
  name text,
  region text,
  zone text,
  labels jsonb not null default '{}'::jsonb,
  metadata jsonb not null default '{}'::jsonb,
  first_seen_at timestamptz not null default now(),
  last_seen_at timestamptz not null default now(),
  deleted_at timestamptz,
  unique (organization_id, provider, resource_type, external_id)
);

create table agents (
  id uuid primary key,
  organization_id uuid not null references organizations(id) on delete cascade,
  resource_id uuid references resources(id) on delete set null,
  hostname text not null,
  display_name text,
  status text not null default 'active',
  auth_type text not null default 'token',
  token_hash text,
  fingerprint text,
  last_seen_at timestamptz,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table model_endpoints (
  id uuid primary key,
  organization_id uuid not null references organizations(id) on delete cascade,
  resource_id uuid references resources(id) on delete set null,
  endpoint_name text not null,
  model_name text not null,
  model_version text,
  serving_platform text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (organization_id, endpoint_name)
);

create table metric_samples (
  ts timestamptz not null,
  organization_id uuid not null references organizations(id) on delete cascade,
  resource_id uuid not null references resources(id) on delete cascade,
  agent_id uuid references agents(id) on delete set null,
  ingest_id uuid not null,
  metric_name text not null,
  value double precision not null,
  unit text not null,
  dimensions jsonb not null default '{}'::jsonb,
  recorded_at timestamptz not null default now(),
  primary key (organization_id, resource_id, metric_name, ts, ingest_id)
);

select create_hypertable('metric_samples', 'ts', if_not_exists => true, chunk_time_interval => interval '1 day');

create index ix_metric_samples_org_resource_ts
  on metric_samples (organization_id, resource_id, ts desc);

create index ix_metric_samples_org_metric_ts
  on metric_samples (organization_id, metric_name, ts desc);

create index ix_metric_samples_dimensions_gin
  on metric_samples using gin (dimensions);

create table inference_requests (
  ts timestamptz not null,
  organization_id uuid not null references organizations(id) on delete cascade,
  model_endpoint_id uuid not null references model_endpoints(id) on delete cascade,
  resource_id uuid references resources(id) on delete set null,
  agent_id uuid references agents(id) on delete set null,
  request_id text not null,
  latency_ms integer not null,
  queue_ms integer,
  throughput_tps numeric(12, 4),
  tokens_input integer,
  tokens_output integer,
  gpu_seconds numeric(12, 4),
  status_code integer,
  error_code text,
  cost_usd numeric(14, 6),
  attributes jsonb not null default '{}'::jsonb,
  recorded_at timestamptz not null default now(),
  primary key (organization_id, model_endpoint_id, ts, request_id)
);

select create_hypertable('inference_requests', 'ts', if_not_exists => true, chunk_time_interval => interval '1 day');

create index ix_inference_org_endpoint_ts
  on inference_requests (organization_id, model_endpoint_id, ts desc);

create index ix_inference_org_request
  on inference_requests (organization_id, request_id);

create table model_minute_rollups (
  bucket timestamptz not null,
  organization_id uuid not null references organizations(id) on delete cascade,
  model_endpoint_id uuid not null references model_endpoints(id) on delete cascade,
  requests bigint not null default 0,
  errors bigint not null default 0,
  p50_latency_ms integer,
  p95_latency_ms integer,
  p99_latency_ms integer,
  input_tokens bigint not null default 0,
  output_tokens bigint not null default 0,
  total_gpu_seconds numeric(14, 4) not null default 0,
  avg_gpu_utilization numeric(5, 2),
  avg_gpu_memory_mb integer,
  total_cost_usd numeric(14, 6) not null default 0,
  primary key (organization_id, model_endpoint_id, bucket)
);

create table alerts (
  id uuid primary key,
  organization_id uuid not null references organizations(id) on delete cascade,
  resource_id uuid references resources(id) on delete set null,
  model_endpoint_id uuid references model_endpoints(id) on delete set null,
  alert_type text not null,
  severity text not null,
  status text not null default 'open',
  title text not null,
  description text,
  details jsonb not null default '{}'::jsonb,
  started_at timestamptz not null default now(),
  resolved_at timestamptz
);

create table recommendations (
  id uuid primary key,
  organization_id uuid not null references organizations(id) on delete cascade,
  resource_id uuid references resources(id) on delete set null,
  category text not null,
  title text not null,
  description text not null,
  impact text not null,
  effort text not null,
  estimated_savings_usd numeric(14, 6),
  status text not null default 'open',
  details jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table budgets (
  id uuid primary key,
  organization_id uuid not null references organizations(id) on delete cascade,
  name text not null,
  scope jsonb not null default '{}'::jsonb,
  amount_usd numeric(14, 6) not null,
  period text not null,
  threshold_percent integer not null default 80,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index ix_users_org on users (organization_id);
create index ix_roles_org on roles (organization_id);
create index ix_cloud_accounts_org on cloud_accounts (organization_id);
create index ix_resources_org_type on resources (organization_id, resource_type);
create index ix_resources_org_last_seen on resources (organization_id, last_seen_at desc);
create index ix_resources_labels_gin on resources using gin (labels);
create index ix_agents_org_status on agents (organization_id, status);
create index ix_model_endpoints_org on model_endpoints (organization_id);
create index ix_alerts_org_status on alerts (organization_id, status);
create index ix_recommendations_org_status on recommendations (organization_id, status);

-- Suggested TimescaleDB lifecycle policies:
-- select add_retention_policy('metric_samples', interval '30 days');
-- select add_compression_policy('metric_samples', interval '7 days');
-- select add_retention_policy('inference_requests', interval '30 days');

-- Suggested continuous aggregates should be created after production query patterns stabilize.
