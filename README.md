# Python CRUD REST API

Minimal FastAPI project using Python 3.12, environment-based config loading, and a `src` layout.

## Requirements

- Python `3.12.6`
- `pip`

## Project Structure

```text
.
├── .python-version
├── requirements.txt
├── src
│   ├── .env.example
│   ├── config
│   │   └── main.py
│   └── main.py
└── README.md
```

## Setup

1. Create the virtual environment:

```bash
python3.12 -m venv .venv
```

2. Activate it:

```bash
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Testing

The integration tests use pytest and connect to a dedicated PostgreSQL database.
Pytest is installed with the project dependencies from `requirements.txt`.

Create `.env.test` from the example and configure it with the test database
connection. Do not point this file at a development or production database.

```bash
cp .env.example .env.test
```

Create the test database, then apply the database migrations using the test
environment:

```bash
NODE_ENV=test PYTHONPATH=src ./.venv/bin/python src/db/migrate.py upgrade
```

Run all tests from the project root:

```bash
./.venv/bin/pytest
```

Run only the user controller tests:

```bash
./.venv/bin/pytest src/controllers/user_test.py
```

The root `conftest.py` sets `NODE_ENV=test`, adds `src` to Python's import path,
and initializes the exclusive test user before the test session. User controller
tests authenticate with this account. Test cleanup deletes all other records from
the test `users` table while preserving the exclusive account.

## Environment Variables

The config module reads `NODE_ENV` and loads one of these files from the project root:

- `development` -> `.env.dev`
- `test` -> `.env.test`
- `production` -> `.env.prod`

Create `.env.dev` based on [`src/.env.example`](/Volumes/Mauro/Documentos/web-development/python-crud-rest-api/src/.env.example):

```bash
cp src/.env.example .env.dev
```

Available variables:

```env
ALLOWED_ORIGINS="http://localhost:3000"
PORT="3000"
JWT_SECRET_KEY="change-me"
DISK_STORAGE_PATH="./storage"
DB_DIALECT="postgresql"
DB_HOST="127.0.0.1"
DB_PORT="5434"
DB_USER="postgres"
DB_PASSWORD="postgres"
DB_NAME="ecommerce"
```

## Run The API

From the project root:

```bash
PYTHONPATH=src ./.venv/bin/fastapi dev src/main.py
```

Alternative with Uvicorn:

```bash
PYTHONPATH=src ./.venv/bin/python -m uvicorn src.main:app --reload
```

## Endpoints

- `GET /`
- `GET /items/{item_id}`

Examples:

```bash
curl http://127.0.0.1:8000/
curl "http://127.0.0.1:8000/items/1?q=test"
```

## Configuration Usage

The app config is defined in [`src/config/main.py`](/Volumes/Mauro/Documentos/web-development/python-crud-rest-api/src/config/main.py).

Import it with:

```python
from config.main import config
```

Example:

```python
from config.main import config

print(config["environment"])
print(config["db"]["host"])
```

## Notes

- The current FastAPI app entrypoint is [`src/main.py`](/Volumes/Mauro/Documentos/web-development/python-crud-rest-api/src/main.py).
- If you run Python from the project root, keep `PYTHONPATH=src` so imports like `from config.main import config` work.
