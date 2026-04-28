# SE4453 Midterm Project - Group 9

Flask-based backend with PostgreSQL database and Azure cloud deployment featuring private networking and Key Vault integration.

## Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL (local development) or Azure PostgreSQL

### Local Setup

1. **Clone & activate virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   Copy `.env.example` to `.env` and fill in your database credentials:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your PostgreSQL connection details.

4. **Run application:**
   ```bash
   python app.py
   ```
   Flask runs on `http://localhost:8000`

## API Endpoints

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| GET | `/` | Health check | `{"success": true, "message": "Backend is running"}` |
| GET | `/hello` | DB connectivity test | `{"success": true, "database_status": "connected", "server_time": "..."}` |

**Error Response:** `{"success": false, "error": "..."}` (HTTP 500 if DB connection fails)

## Azure Deployment

Resources created:
- App Service (private)
- PostgreSQL Database (private, accessed via VM SSH)
- Key Vault (with private endpoint)
- Virtual Network & Security Groups

For full setup instructions, refer to deployment documentation.

## Tech Stack
- **Backend:** Flask 3.1.3
- **Database:** PostgreSQL via psycopg2
- **Server:** Gunicorn
- **Config:** python-dotenv
- **Cloud:** Microsoft Azure

## Development Notes
- Environment variables defined in `.env` (copy from `.env.example`)
- Database connection pooling recommended for production
- Use `APP_ENV=development` for local testing
   