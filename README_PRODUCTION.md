README — Production Deployment (Family Notes Backend)
===============================================

This document describes recommended configuration and deployment steps for running the Family Notes backend in a production environment. It focuses on secure handling of secrets, NeonDB (Postgres) specifics, containerized deployment, and essential post-deploy checks.

1) Production environment variables (do NOT commit)
-------------------------------------------------
- `SECRET_KEY` — strong, unrevealed Django secret.
- `DEBUG` — set to `False` in production.
- `ALLOWED_HOSTS` — comma-separated production hostnames (e.g. `api.example.com`).
- `CORS_ALLOWED_ORIGINS` — allowed front-end origins (e.g. `https://www.example.com`).
- `DB_ENGINE` — `django.db.backends.postgresql`.
- `DB_NAME` — database name (Neon usually uses `postgres`).
- `DB_USER` — Neon DB user.
- `DB_PASSWORD` — Neon DB password (secret).
- `DB_HOST` — Neon pooler host (use the pooler endpoint, ends with `-pooler...`).
- `DB_PORT` — usually `5432`.
- `CONN_MAX_AGE` — use `0` for Neon serverless; use `>=300` when using a persistent pooler or dedicated Postgres.
- `SECURE_SSL_REDIRECT` — `True` when serving over HTTPS.
- `START_CMD` — production start command (example below uses Gunicorn).

2) NeonDB (Postgres) recommendations
------------------------------------
- Always use the Neon "pooler" endpoint for application connections to avoid connection limits.
- For Neon serverless, set `CONN_MAX_AGE=0` to avoid holding idle connections. For pooler/dedicated setups, `300-1800` is reasonable.
- Ensure TLS/SSL is required (Neon usually enforces it). Your `DATABASES` `OPTIONS` should include `sslmode=require`.

3) Example production `.env` (DO NOT store in the repo)
--------------------------------------------------------
Replace values before adding to your provider secrets.

```
SECRET_KEY=change_this_to_a_strong_random_value
DEBUG=False
ALLOWED_HOSTS=api.example.com
CORS_ALLOWED_ORIGINS=https://example.com

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=<neon_user>
DB_PASSWORD=<neon_password>
DB_HOST=<your_neon_pooler_endpoint>
DB_PORT=5432
CONN_MAX_AGE=0

SECURE_SSL_REDIRECT=True
START_CMD=gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

4) Docker and process management
---------------------------------
- The repository includes a `Dockerfile` and `docker-compose.yml` for building and running the app. In production you can either build a Docker image and push it to a registry, or use your platform's native deploy method.
- Use Gunicorn or a process manager behind a reverse proxy (NGINX, Cloud Load Balancer). Example `START_CMD` above is recommended.

Build and run (example):
```
docker-compose build --no-cache web
docker-compose up -d --force-recreate
```

5) Database migrations & release steps
-------------------------------------
Run migrations as part of your release process before sending traffic to the new release:

```
python manage.py migrate
```

If you deploy with containers, run migrations in a one-off job or as an entrypoint step that executes before worker processes start accepting traffic.

6) Secrets management (recommended)
-----------------------------------
- Use Railway/GCP/AWS/Heroku secret management rather than storing `.env` in the repository.
- In CI/CD use environment secrets (GitHub Actions Secrets, GitLab CI Variables) and inject them during deployment.

7) Healthchecks, logging & monitoring
-------------------------------------
- Add a simple health endpoint (e.g., `/health/` returning 200) and wire a healthcheck in your platform.
- Forward logs to a structured log sink (Papertrail, Datadog, Cloud Logging). Configure Django logging accordingly.
- Capture errors with Sentry or similar for production monitoring.

8) Security checklist before first public release
-------------------------------------------------
- `DEBUG=False` and `SECRET_KEY` not in repo.
- `ALLOWED_HOSTS` configured for production domain(s).
- HTTPS configured fronting your application and `SECURE_SSL_REDIRECT=True`.
- Ensure token lifetimes and SimpleJWT settings are reasonable (short access tokens, refresh rotation enabled).
- Blacklist token rotation is enabled (`rest_framework_simplejwt.token_blacklist`) and migrated.
- No hard-coded credentials in settings or source.

9) CI / Deployment pipeline suggestions
--------------------------------------
- Run `pytest` and linters in CI.
- Build reproducible Docker images and push to a registry.
- Migrate DB in a controlled step before switching traffic.
- Use canary or blue/green deployment strategies if supported by your platform.

10) Rollback plan
-----------------
- Keep the previous image available in the registry.
- If database migrations are destructive, use a feature flag or migration plan that is backwards compatible where possible.

11) Quick Troubleshooting
------------------------
- Connection errors: verify `DB_HOST` is the pooler endpoint and `CONN_MAX_AGE` is appropriate.
- Token/auth errors: check your JWT settings and system clocks (JWTs depend on correct time).
- Application fails to start: check logs and ensure `gunicorn` is installed and `START_CMD` is correct in the environment.

If you want, I can also:
- Produce a `README_PRODUCTION_CHECKLIST.md` with step-by-step commands for Railway or a sample GitHub Actions workflow for CI/CD.
- Create a minimal health endpoint and logging config modifications to the repo.
