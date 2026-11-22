# Alibag Villa Booking Portal — Structure 1

Starter project for a single-villa booking website with an architecture that can later expand.

## Included
- Flask application and separate route modules
- SQLite locally; PostgreSQL when `DATABASE_URL` is configured
- Booking enquiry flow (request only; no auto-confirmation)
- Admin login starter (configure credentials via environment variables)
- Payment submission placeholder (UTR; payment must be verified manually)
- Gallery admin starter; Cloudinary integration placeholder
- CSRF via Flask-WTF, secure session defaults, upload validation starter

## Run locally
1. Create a virtual environment: `python -m venv .venv`
2. Activate it.
3. Install: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and configure values.
5. Run: `flask --app app run`

## Admin
Set `ADMIN_USERNAME` and `ADMIN_PASSWORD` in `.env`. Do not use the default username/password in production.
The initial admin authentication is a basic starter. Before public launch, implement hashed admin credentials,
2FA, lockout/rate limiting, audit logging and hardened CSRF/session settings.

## Hosting
Use a separate GitHub repository and Render service. Set secrets in Render Environment, not in GitHub.
