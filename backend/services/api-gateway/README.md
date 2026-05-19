# API Gateway

FastAPI gateway for MaatiTrace. This service exposes versioned HTTP APIs and routes requests to backend domain services.

## Development

Install dependencies:

```bash
poetry install
```

Run locally:

```bash
poetry run uvicorn app.main:app --reload
```

Health check:

```bash
curl http://localhost:8000/api/v1/health
```

