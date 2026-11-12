# ShopMate AI — Backend API

FastAPI-powered backend for **ShopMate AI**, an intelligent e-commerce and retail management dashboard tailored for Pakistani retail businesses.

---

## 📁 Directory Structure

```text
backend/
├── main.py                  # FastAPI application entrypoint, CORS & error handlers
├── requirements.txt         # Python project dependencies
├── README.md                # Backend setup, endpoints and usage documentation
├── models/                  # Pydantic schemas for data validation
│   ├── __init__.py
│   ├── product.py           # Product schemas (ProductCreate, ProductUpdate, etc.)
│   ├── order.py             # Order schemas and OrderStatus enum
│   ├── inventory.py         # Restock and inventory status schemas
│   ├── customer.py          # Customer schemas
│   ├── analytics.py         # Sales analytics and performance schemas
│   └── agent.py             # AI Agent query and recommendation schemas
├── services/                # Business logic and data management
│   ├── __init__.py
│   ├── database.py          # SQLite schema and persistence layer
│   ├── store_data.py        # SQLite-backed store seeded with Pakistani shop sample data
│   ├── product_service.py   # Catalog CRUD, search, and filtering
│   ├── order_service.py     # Order processing and lifecycle updates
│   ├── inventory_service.py # Stock tracking and replenishment logic
│   ├── customer_service.py  # Customer registry and lookups
│   └── analytics_service.py # Aggregated metrics and daily/weekly trends
├── agents/                  # AI business intelligence agent
│   ├── __init__.py
│   └── shop_agent.py        # Real-time inventory alerts, sales insights & conversational Q&A
├── routes/                  # REST API route handlers
│   ├── __init__.py
│   ├── health.py            # /health & /api/health
│   ├── products.py          # /api/products
│   ├── orders.py            # /api/orders
│   ├── inventory.py         # /api/inventory
│   ├── customers.py         # /api/customers
│   ├── analytics.py         # /api/analytics
│   └── agent.py             # /api/agent
└── tests/                   # Automated test suite
    └── run_tests.py         # Comprehensive test runner (60 assertions)
```

---

## 🛠️ Setup & Installation

### 1. Prerequisites
- Python 3.10+ (Python 3.11, 3.12, 3.13, 3.14 supported)
- pip

### 2. Create and Activate Virtual Environment (Recommended)

From the project root:

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**On macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```powershell
pip install -r backend/requirements.txt
```

---

## 🚀 Running the Server

Start the development server with auto-reload:

```powershell
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

The API will be available at:
- **Base URL:** `http://127.0.0.1:8000`
- **Interactive Swagger Docs:** `http://127.0.0.1:8000/docs`
- **ReDoc Documentation:** `http://127.0.0.1:8000/redoc`

## 💾 Database

The backend uses SQLite (included with Python), so no separate database server or
package installation is required. On first startup, sample products, orders,
customers, and sales data are seeded into `backend/shopmate.db`. Changes made
through the API are saved there and remain available after restarting the server.

To store the database somewhere else, set `SHOPMATE_DATABASE_PATH` before starting
the backend. For example, in PowerShell:

```powershell
$env:SHOPMATE_DATABASE_PATH = "C:\data\shopmate.db"
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

Existing SQLite data is preserved at startup; sample data is only inserted into
empty tables.

---

## 🧪 Running Automated Tests

Run the test suite verifying all 56 endpoint behaviors, validation errors, and business rules:

```powershell
python -u backend/tests/run_tests.py
```

---

## 📡 API Endpoints Reference

### 1. Health Check
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API status and route index |
| `GET` | `/health` | Service health check |
| `GET` | `/api/health` | Service health with timestamp and database mode |

### 2. Products (`/api/products`)
| Method | Endpoint | Query / Body Params | Description |
|---|---|---|---|
| `GET` | `/api/products` | `search`, `category`, `low_stock`, `min_price`, `max_price` | List catalog products |
| `GET` | `/api/products/{sku}` | — | Get single product by SKU |
| `POST` | `/api/products` | JSON body (`name`, `sku`, `price`, `stock`, `category`, `emoji`, `color`) | Add new product |
| `PUT` | `/api/products/{sku}` | JSON body (`name`, `price`, `stock`, `category`, etc.) | Update product details |
| `DELETE` | `/api/products/{sku}` | — | Delete product from catalog |

### 3. Orders (`/api/orders`)
| Method | Endpoint | Query / Body Params | Description |
|---|---|---|---|
| `GET` | `/api/orders` | `status`, `customer`, `search` | List orders with filters |
| `GET` | `/api/orders/{order_id}` | — | Retrieve order by ID (`#SM-2084` or `SM-2084`) |
| `POST` | `/api/orders` | JSON body (`customer`, `item`, `amount`, `status`; optional `product_sku`, `quantity`) | Create order (auto-assigns ID & initials; reserves stock when SKU is supplied) |
| `PATCH` | `/api/orders/{order_id}/status` | JSON body (`status`: "Processing" \| "Shipped" \| "Delivered" \| "Cancelled") | Advance order status |
| `DELETE` | `/api/orders/{order_id}` | — | Cancel / remove order |

### 4. Inventory (`/api/inventory`)
| Method | Endpoint | Query / Body Params | Description |
|---|---|---|---|
| `GET` | `/api/inventory` | — | Inventory summary, total units, status badges |
| `GET` | `/api/inventory/low-stock` | `threshold` (default: 10) | List products running low |
| `POST` | `/api/inventory/{sku}/restock` | JSON body (`quantity`: integer > 0) | Restock product inventory |

### 5. Customers (`/api/customers`)
| Method | Endpoint | Query / Body Params | Description |
|---|---|---|---|
| `GET` | `/api/customers` | `search`, `city` | List customers |
| `GET` | `/api/customers/{phone}` | — | Get customer details by phone number |
| `POST` | `/api/customers` | JSON body (`name`, `phone`, `city`, `orders`, `spent`) | Register customer |
| `PUT` | `/api/customers/{phone}` | JSON body (`name`, `city`, `spent`, etc.) | Update customer |
| `DELETE` | `/api/customers/{phone}` | — | Remove customer record |

### 6. Sales Analytics (`/api/analytics`)
| Method | Endpoint | Query Params | Description |
|---|---|---|---|
| `GET` | `/api/analytics/overview` | `period` ("7 days" \| "30 days") | Gross sales, order count, AOV, peak day |
| `GET` | `/api/analytics/sales` | `period` ("7 days" \| "30 days") | Daily / weekly sales breakdown |
| `GET` | `/api/analytics/top-products` | `limit` (default: 5) | Top revenue and volume products |
| `GET` | `/api/analytics/categories` | — | Revenue and units sold per category |

### 7. AI Business Agent (`/api/agent`)
| Method | Endpoint | Query / Body Params | Description |
|---|---|---|---|
| `POST` | `/api/agent/chat` | JSON body (`message`: string) | Conversational advisor based on real-time metrics |
| `GET` | `/api/agent/recommendations` | — | Automated high/medium/low priority recommendations |

---

## 🛡️ Input Validation & Error Handling

- **Pydantic Validation**: All requests are validated against strict type, length, and range constraints (e.g. price > 0, stock >= 0).
- **Formatted Error Responses**: Unprocessable entities return structured HTTP 422 responses identifying exact invalid fields.
- **CORS Configured**: Pre-configured `CORSMiddleware` allows frontend origins like `http://localhost:5173` without CORS blocks.
- **Frontend Isolation**: The backend operates independently from the React frontend in `frontend/`.
