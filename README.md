# SE4453 — Azure Hello App

Flask app with a `/hello` endpoint that connects to **Azure Database for PostgreSQL Flexible Server** using credentials pulled from **Azure Key Vault** via a **User-Assigned Managed Identity**. Built into a Docker image by **GitHub Actions**, pushed to **Azure Container Registry (ACR)**, and deployed to **Azure App Service** on every merge to `main`.

## Architecture

```
GitHub push to main ─► GitHub Actions
                       ├── docker build + docker push ─► ACR (acrbatikanzeynep)
                       └── webapps-deploy ─► App Service: linuxFxVersion = DOCKER|...

Client ─► App Service (Docker container, port 8000)
              │
              ├── User-Assigned Identity (appServiceID)
              │      ├── AcrPull          ─► pulls image from ACR
              │      └── KV Secrets User  ─► reads db-host, db-name, db-user, db-password
              │
              └── psycopg3 ─► PostgreSQL Flexible Server (private, VNet-integrated)
```

## Deployment pipeline

1. Developer pushes a feature branch and opens a PR against `main`.
2. PR is reviewed and merged. The merge to `main` triggers `.github/workflows/build-push.yml`.
3. Workflow logs in to Azure with the `apiapp-cicd` Service Principal stored in `AZURE_CREDENTIALS` (scoped only to the `apiapp` resource).
4. Workflow logs in to ACR with admin credentials (`REGISTRY_USERNAME` / `REGISTRY_PASSWORD`).
5. Workflow builds the Docker image, tags it with the commit SHA, and pushes it to ACR.
6. `azure/webapps-deploy@v2` updates `apiapp.linuxFxVersion` to point at the new image.
7. App Service restarts the container, pulling the image via the **User-Assigned Identity** (`acrUseManagedIdentityCreds=true`, `acrUserManagedIdentityId` = UAI clientId).
8. The container starts SSH on port 2222 (Azure App Service custom-container console) and gunicorn on port 8000 (`WEBSITES_PORT=8000`).

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

| Branch                           | What it adds                                                         |
|----------------------------------|----------------------------------------------------------------------|
| `feature/flask-skeleton`         | Base Flask app, routes, tests                                        |
| `feature/keyvault-integration`   | Azure Key Vault client via Managed Identity                          |
| `feature/postgres-connection`    | PostgreSQL connection layer                                          |
| `feature/docker`                 | Dockerfile, SSH config                                               |
| `feature/app-refactor`           | psycopg3 migration, structured logging, error handling               |
| `feature/github-workflows`       | GitHub Actions workflow for ACR build + App Service deploy           |
| `feature/repoint-pipeline`       | Switch deploy target from `finalProjectApp` to `apiapp` (final cutover) |

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
