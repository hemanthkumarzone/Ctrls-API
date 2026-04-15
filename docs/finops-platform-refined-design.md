# FinOps Platform Refined System Design

## Scope
This document refines the current `Ctrls-API` backend architecture for a multi-tenant FinOps monitoring platform with:

- React frontend
- FastAPI backend
- Golang agent
- Multi-cloud and on-prem monitoring
- GPU and AI inference observability

It is grounded in the current backend structure under `app/` and is intended to guide the next implementation phase.

## Current-State Review

### What is already strong
- The backend is already organized around `api`, `models`, `schemas`, `repositories`, and `services`.
- The domain model in `app/models/all_models.py` already covers:
  - tenants
  - users
  - cloud accounts
  - kubernetes clusters, nodes, pods
  - accelerators
  - jobs
  - cost line items
  - recommendations
  - hourly resource metrics
- API versioning already exists with `/api/v1`.
- The backend is clearly intended to support PostgreSQL and TimescaleDB.

### Current gaps to address
- Telemetry ingestion is not implemented yet:
  - `app/api/v1/endpoints/metrics.py`
  - `app/api/v1/endpoints/agents.py`
  - `app/services/metrics_service.py`
  - `app/repositories/metrics_repo.py`
- Tenant isolation is modeled in tables, but enforcement is incomplete.
- Authentication and tenancy are not fully aligned:
  - JWT creation does not include `tenant_id`
  - tenant middleware expects `tenant_id` in JWT
  - current login flow looks up users globally by email
- The current hourly metrics model is too limited for dense per-second telemetry, GPU attribution, and inference-level observability.
- The frontend in the neighboring UI repo is still heavily mock-driven, so the live dashboard contract is not yet stable.

## Recommended Target Architecture

Use FastAPI as the control plane and query plane, but avoid making synchronous API writes directly into the long-term metrics store for every sample.

```text
React Dashboard
   |
   v
Load Balancer / API Gateway
   |
   +--> FastAPI Control Plane
   |      - auth
   |      - tenant management
   |      - resource inventory
   |      - dashboards
   |      - reporting
   |      - cost analytics
   |
   +--> FastAPI Ingestion API
          - agent auth
          - payload validation
          - rate limiting
          - queue publishing
                 |
                 v
            Kafka / RabbitMQ
                 |
     +-----------+-----------+
     |                       |
     v                       v
Metrics Workers         Events / Inference Workers
     |                       |
     v                       v
TimescaleDB             PostgreSQL
     |
     +--> Continuous Aggregates / Rollups
     |
     v
Redis Cache
     |
     v
FastAPI Query APIs
     |
     v
React Dashboard
```

## Deployment Recommendation

Stay with a modular monolith first, not a full microservices split.

Run the same codebase in separate runtime roles:

- `api`
  - user-facing APIs
  - metadata CRUD
  - dashboard queries
- `ingest`
  - agent ingestion endpoints
  - lightweight validation
  - queue publishing
- `worker`
  - anomaly detection
  - metric enrichment
  - rollups
  - AI inference summarization
  - cost aggregation

This gives you:

- simpler development and deployment than microservices
- independent scaling by workload type
- cleaner migration path later if ingestion or analytics outgrows the monolith

## Refined Component Responsibilities

### React frontend
- Tenant-aware dashboard and admin UI
- Real-time KPI panels using websocket or server-sent events
- Historical drill-down via aggregated query APIs
- RBAC-aware navigation and page access

### FastAPI backend
- Authentication and authorization
- Organization, user, role, and policy management
- Resource inventory normalization
- Cost, budget, recommendation, anomaly, and reporting APIs
- Query APIs for both real-time and historical metrics

### Go agent
- Collect host metrics:
  - CPU
  - memory
  - disk
  - network
  - process-level stats
- Collect GPU metrics:
  - utilization
  - memory used
  - temperature
  - power
  - model/pod/process attribution where possible
- Collect AI inference metrics from:
  - model serving runtime
  - application instrumentation
  - node-local exporters
- Batch and compress metrics before sending
- Retry safely with sequence numbers and idempotency keys

## Multi-Tenant Design

### Isolation strategy
Use three layers of tenant isolation:

1. API layer
   - every authenticated request resolves `organization_id`
2. Application layer
   - repositories always query with `organization_id`
3. Database layer
   - PostgreSQL row-level security for critical shared tables

### Tenant model recommendation
Use `organizations` as the primary tenant boundary.

Each of the following should be scoped by `organization_id`:

- users
- roles
- resources
- agents
- cloud accounts
- metrics
- inference data
- alerts
- reports
- recommendations

### RBAC recommendation
Recommended roles:

- `org_owner`
- `org_admin`
- `finops_manager`
- `engineer`
- `viewer`
- `billing_reader`

Permissions should be policy-based, not hardcoded string checks inside endpoints.

## Security Improvements

### Immediate fixes needed in current backend
- Include `tenant_id` or `organization_id` in JWT claims.
- Stop authenticating users by global email alone.
- Require tenant-scoped login or resolve tenant membership explicitly.
- Split human auth and agent auth into different mechanisms.

### Human authentication
- JWT access token + refresh token
- Claims should include:
  - `sub`
  - `organization_id`
  - `roles`
  - `token_type`

### Agent authentication
Recommended options:

- Phase 1:
  - per-agent token
  - organization-scoped
  - short expiration
  - rotated regularly
- Phase 2:
  - mutual TLS with agent certificate identity
  - optional Vault or SPIRE integration

### Additional controls
- Encrypt cloud credentials with KMS or Vault
- Add audit logs for:
  - login
  - token issuance
  - role changes
  - agent registration
  - cloud account changes
  - configuration updates

## Metrics Storage Strategy

### Why PostgreSQL alone is not enough
Dense metrics such as:

- per-second CPU
- per-second GPU
- inference request events
- pod/node metrics across many tenants

will quickly create write and query pressure if stored only in normalized OLTP tables.

### Recommended split
- PostgreSQL:
  - metadata
  - RBAC
  - resource inventory
  - cost models
  - budgets
  - anomalies
  - recommendations
- TimescaleDB:
  - raw samples
  - minute rollups
  - hourly rollups
  - inference request events

### Retention policy
- raw metrics: `7-30 days`
- 1-minute aggregates: `90 days`
- 1-hour aggregates: `13-24 months`
- inference request detail: `7-30 days`
- inference rollups: `12+ months`

## Refined Data Model

### Core metadata entities
- organizations
- users
- roles
- user_roles
- cloud_accounts
- resources
- agents
- model_endpoints
- alerts
- budgets
- reports

### Time-series entities
- metric_samples
- metric_rollup_1m
- metric_rollup_5m
- metric_rollup_1h
- inference_requests
- model_minute_rollups

### Resource normalization
Avoid separate storage strategies per provider for all monitoring data.

Instead, create a common `resources` table that represents:

- cloud VM
- on-prem host
- kubernetes cluster
- kubernetes node
- kubernetes pod
- GPU
- storage volume
- model endpoint
- service

Provider-specific metadata stays in JSONB, while shared query dimensions stay normalized.

## Refined Database Schema

See `docs/refined_timescale_schema.sql` for concrete SQL.

High-level design:

```text
organizations
  -> users
  -> roles
  -> cloud_accounts
  -> resources
      -> agents
      -> model_endpoints
      -> metric_samples
  -> inference_requests
```

## Ingestion Design

### Recommended ingestion path

```text
Go Agent
  -> POST /api/v1/agents/register
  -> POST /api/v1/agents/{agent_id}/heartbeat
  -> POST /api/v1/ingest/metrics
  -> POST /api/v1/ingest/inference
  -> POST /api/v1/ingest/events
```

### Why batch ingestion
Batching is the best default for this platform because it:

- reduces API overhead
- reduces DB write amplification
- improves compression
- survives transient failures better
- is simpler than fully streaming ingestion

### Batch guidance
- default flush every `5-15 seconds`
- gzip payloads
- include:
  - `agent_id`
  - `sequence`
  - `captured_at`
  - `idempotency_key`
- allow partial acceptance with per-record validation errors

### Sample ingestion payload

```json
{
  "agent_id": "8f96dfab-9f2c-4bd7-91e0-0b8d68d0f8f7",
  "sequence": 10452,
  "captured_at": "2026-04-15T10:00:05Z",
  "samples": [
    {
      "resource_ref": {
        "provider": "onprem",
        "resource_type": "gpu",
        "external_id": "host-01/gpu-0"
      },
      "metric_name": "gpu.utilization",
      "value": 81.2,
      "unit": "percent",
      "dimensions": {
        "model_name": "llama-3",
        "pod_uid": "pod-123"
      }
    }
  ]
}
```

## API Design Recommendation

### Control plane APIs
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `GET /api/v1/organizations/current`
- `GET /api/v1/resources`
- `GET /api/v1/resources/{resource_id}`
- `GET /api/v1/metrics/query`
- `GET /api/v1/models/{model_id}/inference/summary`
- `GET /api/v1/dashboard/summary`

### Agent APIs
- `POST /api/v1/agents/register`
- `POST /api/v1/agents/{agent_id}/heartbeat`
- `POST /api/v1/ingest/metrics`
- `POST /api/v1/ingest/inference`
- `POST /api/v1/ingest/events`

### Query patterns
Support these query dimensions consistently:

- organization
- provider
- account
- region
- cluster
- namespace
- pod
- host
- GPU
- model
- service
- tag
- time range

## Real-Time And Historical Metrics

### Real-time path
- Agent sends near-real-time batches
- Ingestion workers write raw samples
- Redis caches latest status per resource
- UI polls or subscribes for:
  - latest health
  - active alerts
  - recent GPU status
  - current inference throughput

### Historical path
- Raw data stored in hypertables
- Continuous aggregates compute:
  - 1-minute
  - 5-minute
  - 1-hour summaries
- Dashboard reads rollups by default
- Raw samples are only queried for narrow debug windows

## AI Monitoring Enhancements

### What to track per request
- request timestamp
- latency
- queue time
- input tokens
- output tokens
- throughput
- status code
- error code
- cost
- model endpoint
- GPU seconds

### What to track per model
- requests per minute
- p50 latency
- p95 latency
- p99 latency
- error rate
- tokens per second
- cost per 1K tokens
- GPU utilization
- GPU memory consumption

### GPU attribution guidance
Best-effort attribution should combine:

- process ID
- pod UID
- container ID
- model endpoint ID
- node name
- GPU device index

If exact attribution is not always possible, store both:

- raw device-level GPU metrics
- optional model attribution dimensions

This keeps the ingestion path robust even when attribution is incomplete.

## Queue Recommendation

### Kafka
Choose Kafka if you need:

- replay
- long-lived retention
- independent multiple consumers
- very high throughput
- partitioned scale by tenant or agent

### RabbitMQ
Choose RabbitMQ if you need:

- simpler operations
- lower throughput requirements
- task-oriented delivery
- smaller initial footprint

### Recommendation for this platform
- Start with RabbitMQ if expected telemetry volume is moderate.
- Start with Kafka if you already expect thousands of agents sending high-frequency GPU and inference telemetry.

## Redis Recommendation
Use Redis for:

- hot dashboard summaries
- latest resource status
- agent heartbeat state
- rate limiting
- short-lived query cache
- websocket fan-out state

Do not use Redis as the system of record for metrics.

## Horizontal Scaling Strategy

### FastAPI
- stateless app instances
- horizontal scale behind load balancer
- separate autoscaling for `api` and `ingest`

### Workers
- autoscale based on queue lag
- separate worker pools for:
  - metrics
  - inference
  - anomaly detection
  - reporting

### Database
- PostgreSQL primary for writes
- read replicas for analytics-heavy reads
- TimescaleDB hypertables and continuous aggregates for metric queries

## Monitoring Lifecycle

```text
1. Organization registers
2. Organization adds users and roles
3. Organization connects cloud accounts and environments
4. Agent is registered and receives credentials
5. Agent discovers resources and reports inventory
6. Agent sends metrics in batches
7. Backend normalizes resource identity
8. Metrics are stored and rolled up
9. Dashboards query summaries and trends
10. Alerts, anomalies, and recommendations are generated
11. Historical data ages into coarser aggregates
```

## User Interaction Flow

```text
React UI
  -> login
  -> fetch dashboard summary
  -> fetch cost trends
  -> fetch inventory
  -> fetch anomalies and recommendations
  -> fetch drill-down metrics
  -> render tenant-scoped views
```

## Recommended Backend Folder Structure

Current structure is workable, but it will become harder to maintain as telemetry grows.

Recommended shape:

```text
app/
  api/
    v1/
      routes/
  core/
  db/
  domain/
    organizations/
    auth/
    agents/
    resources/
    metrics/
    inference/
    billing/
    dashboards/
  ingestion/
    schemas/
    validators/
    publishers/
  workers/
    metrics/
    inference/
    anomaly/
    reporting/
```

## API Versioning Strategy

Keep `/api/v1` and evolve it conservatively.

Within `v1`:
- allow additive fields
- allow new endpoints
- avoid changing agent ingestion payload semantics incompatibly

Introduce `/api/v2` only when:
- auth contract changes materially
- tenant model changes materially
- ingestion payloads break backward compatibility

## Monolith Vs Microservices

### Recommendation
Stay with a modular monolith for now.

### Why
- faster development
- easier debugging
- lower operational overhead
- cleaner schema evolution
- easier transaction boundaries

### Split later only if
- ingestion traffic becomes operationally independent
- anomaly and forecasting workloads require isolated scaling
- different teams own different bounded contexts

## Observability Recommendations

Instrument the platform itself with:

- structured logs
- OpenTelemetry traces
- Prometheus metrics

Key fields to include everywhere:

- `organization_id`
- `agent_id`
- `resource_id`
- `request_id`
- `trace_id`
- `route`
- `worker_type`

Platform SLO candidates:

- ingestion success rate
- ingestion-to-query freshness
- dashboard p95 latency
- alert evaluation lag
- worker queue lag

## Immediate Implementation Priorities

### Priority 1
- fix tenant-aware auth and JWT claims
- implement real agent registration
- implement metrics ingestion schemas and endpoints

### Priority 2
- introduce normalized `resources` table
- add TimescaleDB hypertables for raw metrics and inference events
- add rollup jobs and retention policies

### Priority 3
- integrate Redis cache for dashboard summaries
- add queue-backed worker processing
- add AI inference performance APIs

### Priority 4
- add websocket or SSE updates for real-time dashboard panels
- add row-level security in PostgreSQL
- add audit logging and credential rotation workflows

## Proposed Next Changes In This Repository

Recommended code changes for the next implementation pass:

1. Replace the current auth token generation to include tenant context.
2. Add `app/api/v1/endpoints/ingest.py`.
3. Add concrete Pydantic schemas for agent registration and metric batches.
4. Add a normalized `resources` model instead of storing all telemetry around only accelerators and k8s entities.
5. Add Timescale-compatible models and migrations for raw metric samples and inference requests.
6. Move tenant enforcement from middleware-only logic into repository and DB-level controls.
