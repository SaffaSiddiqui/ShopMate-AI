# ShopMate AI

ShopMate AI is a retail dashboard for Pakistani businesses. It includes a React
dashboard and a FastAPI backend with persistent SQLite storage.

## Requirements

- Python 3.10 or later
- Node.js and npm

## Run locally

Open two PowerShell terminals at the project root.

In the first terminal, install the backend dependencies once, then start the API:

```powershell
python -m pip install -r backend/requirements.txt
npm run backend
```

In the second terminal, install frontend dependencies once, then start Vite:

```powershell
npm install
npm run dev
```

Open the frontend URL printed by Vite (usually `http://localhost:5173`). The
backend API is available at `http://127.0.0.1:8000`; interactive API
documentation is at `http://127.0.0.1:8000/docs`.

## Database

The backend uses Python's built-in SQLite support; no external database service
is required. On first startup, sample products, orders, customers, and sales
analytics are saved to `backend/shopmate.db`. Product, inventory, order, and
customer changes made through the API are persisted across backend restarts.

Set `SHOPMATE_DATABASE_PATH` before starting the backend to use a different
database file. The database is local to this machine and should be backed up;
it is excluded from Git.

## Features

- Responsive dashboard with sales, order, product, and low-stock metrics
- Product catalogue, order management, inventory restocking, and customer views
- Sales analytics and CSV export
- ShopMate business assistant with rules-based recommendations from live backend data
- FastAPI endpoints for products, orders, inventory, customers, analytics, and the assistant

The assistant currently uses the backend's built-in business rules; it does not
require an external AI provider or API key. When the backend is unavailable, the
frontend can still display sample data in local demo mode; those demo-mode
changes are not saved to the database.

## Validation

```powershell
npm run build
npm run test:backend
```

Backend tests use a temporary SQLite database and do not modify the application
database.
