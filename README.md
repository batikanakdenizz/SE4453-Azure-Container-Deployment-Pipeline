# SE4453 — Azure Hello App

Flask app with a `/hello` endpoint that connects to **Azure Database for PostgreSQL Flexible Server** using credentials pulled from **Azure Key Vault** via **Managed Identity**. Deployed on **Azure App Service** via local git push to `main` branch.

## Architecture

```
Client ──► App Service (Docker container)
                │
                ├── Managed Identity ──► Key Vault ──► db-host, db-name, db-user, db-password
                │
                └── psycopg3 ──► PostgreSQL Flexible Server (private, via VM SSH tunnel)
```

## Project structure

```
├── app/
│   ├── __init__.py          # create_app() factory
│   ├── config.py            # Config / TestingConfig classes
│   └── routes/
│       ├── __init__.py      # blueprint registration
│       └── health.py        # /hello endpoint
├── core/
│   ├── db.py                # psycopg3 connection via Key Vault secrets
│   └── keyvault.py          # DefaultAzureCredential Key Vault client
├── tests/
│   ├── conftest.py
│   └── test_health.py
├── Dockerfile
├── init.sh                  # starts SSH + gunicorn inside container
├── sshd_config              # SSH daemon config for Azure App Service
├── .env.example
├── CONTRIBUTING.md
├── requirements.txt
├── startup.txt
└── wsgi.py
```

## Git workflow (feature-based)

| Branch                           | What it adds                                      |
|----------------------------------|---------------------------------------------------|
| `feature/flask-skeleton`         | Base Flask app, routes, tests                     |
| `feature/keyvault-integration`   | Azure Key Vault client via Managed Identity       |
| `feature/postgres-connection`    | PostgreSQL connection layer                       |
| `feature/docker`                 | Dockerfile, SSH config, GitHub Actions CI/CD      |

## Local development

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # fill in KEY_VAULT_NAME
az login
python wsgi.py
curl http://localhost:8000/hello
```

## Tests

```bash
pytest tests/
```
