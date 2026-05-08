Family Notes — Backend

Backend project built with Django REST Framework that manages family accounts, individual profiles, and private notes. The project is configured for local development (virtualenv / Docker) and production deployment using NeonDB (Postgres).

Technologies
- Language: Python 3.10+
- Framework: Django 5.2, Django REST Framework
- Authentication: SimpleJWT
- Database: NeonDB / PostgreSQL (production), SQLite (fallback for local tests)
- Containerization: Docker + docker-compose
- WSGI Server: Gunicorn (recommended for production)

Project layout (key files)
- Accounts app: [accounts](accounts)
- Notes app: [notes](notes)
- Project settings: [core/settings.py](core/settings.py)
- Dockerfile: [Dockerfile](Dockerfile)
- Compose: [docker-compose.yml](docker-compose.yml)
- Example environment file: [.env.example](.env.example)

API Overview
- CRUD endpoints for users, families, profiles and notes (see router configuration in `core/urls.py`).

Quickstart — Local development
1. Clone the repository and enter the project directory.
2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/Scripts/activate    # PowerShell/CMD: .venv\\Scripts\\Activate.ps1 / activate.bat
```
3. Install dependencies:

```bash
pip install -r requirements.txt
```
4. Copy the example environment file and fill in local values:

```bash
cp .env.example .env   # Windows: copy .env.example .env
```
5. Run migrations and (optionally) create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```
6. Start the development server:

```bash
python manage.py runserver 0.0.0.0:8000
```

Docker / Production (quick)
- Build the image:

```bash
docker-compose build --no-cache web
```
- Start services (they will read `.env`):

```bash
docker-compose up -d --build
```
- For production, set `START_CMD=gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3` and use Neon pooler endpoint for the database.

Important environment variables
- `SECRET_KEY`: Django secret key (production: use a strong secret and do not commit).
- `DEBUG`: `True` (development) / `False` (production).
- `ALLOWED_HOSTS`: allowed hostnames in production.
- `DB_ENGINE, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT`: Neon/Postgres configuration.
- `CONN_MAX_AGE`: seconds to reuse DB connections. Neon serverless → `0`. With pooler/dedicated → `>=300`.
- `SECURE_SSL_REDIRECT`: `True` to enforce HTTPS in production.
- `START_CMD`: production start command (e.g., Gunicorn).

See [.env.example](.env.example) for a complete list of variables.

Testing
- Run the test suite:

```bash
python -m pytest -q -vv
```
- The project falls back to SQLite when DB environment variables are not present, making local tests simple and safe.

Deployment best practices
- Do not commit `.env` with secrets; use your provider's secrets manager (Railway, Heroku, GCP Secret Manager, etc.).
- Use Neon pooler endpoint to avoid connection limits.
- Set `CONN_MAX_AGE=0` for Neon serverless or increase when using a pooling layer.
- Ensure `DEBUG=False` and `ALLOWED_HOSTS` are properly configured in production.

Security
- JWT authentication via SimpleJWT with refresh token rotation and blacklisting enabled in `core/settings.py`.
- `Profile` and `Note` resources are isolated via `get_queryset` logic and serializer/viewset validations — see `notes/viewsets/note_viewset.py` and `accounts/serializers/profile_serializer.py`.

Roadmap / Suggestions
- Add CI that runs `pytest` and linters on pull requests.
- Add health checks and structured logging for production.
- Consider rate limiting if the API will be publicly available.

Maintainer
- This project is maintained by the author. See repository metadata for contact details.

