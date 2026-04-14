# AI FinOps Platform

A production-grade REST API for AI FinOps (Financial Operations) built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- **Multi-tenant Architecture**: Row-level isolation with tenant_id
- **JWT Authentication**: Access and refresh tokens with role-based access control
- **Kubernetes Integration**: Track clusters, nodes, pods, and accelerators
- **Cost Analytics**: Real-time cost monitoring and anomaly detection
- **Job Orchestration**: Track AI training/inference jobs with resource usage
- **FinOps Intelligence**: Cost optimization recommendations and idle resource detection

## Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0 with Pydantic v2
- **Database**: PostgreSQL (with TimescaleDB for metrics)
- **Auth**: JWT with role-based permissions
- **Background Jobs**: Celery + Redis
- **Migrations**: Alembic
- **Validation**: Pydantic
- **Logging**: Structured logging with structlog

## Quick Start

1. **Clone and setup**:
   ```bash
   git clone <repo>
   cd ai-finops-platform
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. **Database setup**:
   ```bash
   # Start PostgreSQL and Redis
   docker-compose up -d postgres redis

   # Run migrations
   alembic upgrade head

   # Seed initial data
   python -m app.cli.seed
   ```

3. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access API docs**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/refresh` - Refresh access token

### Users
- `GET /api/v1/users/me` - Get current user
- `GET /api/v1/users/` - List users (admin)
- `POST /api/v1/users/` - Create user (admin)

### Tenants
- `GET /api/v1/tenants/` - List tenants (owner)
- `POST /api/v1/tenants/` - Create tenant (owner)

### Jobs
- `GET /api/v1/jobs/` - List jobs with filters
- `POST /api/v1/jobs/` - Create job
- `GET /api/v1/jobs/{job_id}` - Get job details
- `POST /api/v1/jobs/{job_id}/start` - Start job
- `POST /api/v1/jobs/{job_id}/stop` - Stop job

### Cost Analytics
- `GET /api/v1/cost/overview` - Cost overview
- `GET /api/v1/cost/by-service` - Cost by service
- `GET /api/v1/cost/by-job` - Cost by job
- `GET /api/v1/cost/anomalies` - Cost anomalies
- `GET /api/v1/cost/trend` - Cost trend over time

## Testing

Run the included test script to verify basic API functionality:

```bash
python test_api.py
```

This will test:
- Health check endpoint
- User registration
- User login
- User logout

## Architecture

```
app/
├── api/                    # API layer
│   ├── deps.py            # Dependencies (auth, DB)
│   └── v1/endpoints/      # Endpoint routers
├── core/                  # Core functionality
│   ├── config.py          # Settings
│   ├── security.py        # JWT, hashing
│   └── logging.py         # Structured logging
├── db/                    # Database layer
│   ├── session.py         # DB session
│   └── migrations/        # Alembic migrations
├── models/                # SQLAlchemy models
├── schemas/               # Pydantic schemas
├── repositories/          # Data access layer
├── services/              # Business logic
└── utils/                 # Utilities
```

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
isort .
```

### Database Migrations
```bash
# Create migration
alembic revision --autogenerate -m "migration message"

# Run migrations
alembic upgrade head

# Downgrade
alembic downgrade -1
```

## Deployment

### Docker
```bash
docker-compose up -d
```

### Production
- Set `ENVIRONMENT=production` in `.env`
- Use gunicorn for production server
- Configure proper logging and monitoring
- Set up database backups
- Use Redis cluster for high availability

## Security

- JWT tokens with expiration
- Password hashing with bcrypt
- Role-based access control (owner/admin/viewer)
- Tenant-level data isolation
- CORS configuration
- Input validation with Pydantic

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests
4. Ensure code passes linting
5. Submit a pull request

## License

MIT License