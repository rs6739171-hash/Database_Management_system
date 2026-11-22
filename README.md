# 🛒 Database Management System (E-Commerce Backend API)

An asynchronous, production-ready RESTful API backend built with **FastAPI**, **SQLModel**, and **PostgreSQL (asyncpg)**. Designed using a clean layered architecture separating API routers, dependency injection, business service layers, and database models.

---

## 🚀 Features

- **Asynchronous Architecture**: High performance async database operations using SQLAlchemy 2.0 / SQLModel with the `asyncpg` driver.
- **Layered Clean Design**:
  - **Routers**: Clean endpoints dedicated strictly to HTTP request/response handling.
  - **Services**: Business logic encapsulation (`ProductService`, `SellerService`).
  - **Dependencies**: Modular dependency injection for database sessions and service instances.
  - **Schemas & Models**: Type-safe validation using Pydantic V2 and SQLModel.
- **Product Management**: Full CRUD operations (Create, Read, Partial Update via PATCH, and Delete) with input validation.
- **Seller Authentication**: Seller signup with secure `bcrypt` password hashing and OAuth2 login endpoints.
- **Automated Schema Initialization**: Automatic table creation on application startup via FastAPI's async lifespan handler.
- **Interactive API Documentation**: Auto-generated Swagger UI and ReDoc OpenAPI specs out of the box.

---

## 🛠️ Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **FastAPI** | Modern, high-performance web framework for building APIs |
| **SQLModel** | Elegant ORM combining SQLAlchemy and Pydantic |
| **PostgreSQL** | Relational database (compatible with Supabase, AWS RDS, local Postgres) |
| **asyncpg** | Fast asynchronous PostgreSQL driver for Python |
| **Pydantic v2 & Pydantic-Settings** | Data validation and type-safe environment variable management |
| **Passlib & Bcrypt** | Secure password hashing |
| **uv** | Ultra-fast Python package and project manager |

---

## 📂 Project Structure

```text
Database_Management_system/
├── app/
│   ├── api/
│   │   ├── routers/
│   │   │   ├── __init__.py     # Aggregates product and seller routers
│   │   │   ├── product.py      # Product CRUD endpoints (/product)
│   │   │   └── sellers.py      # Seller auth endpoints (/seller)
│   │   ├── dependencies.py     # Dependency injection (Sessions, Services)
│   │   └── __init__.py
│   ├── database/
│   │   ├── models.py           # SQLModel database table definitions (Product, Seller)
│   │   ├── session.py          # Async engine, sessionmaker, and lifespan setup
│   │   └── __init__.py
│   ├── schema/
│   │   ├── models.py           # Pydantic schemas for Product (Create, Read, Update)
│   │   ├── seller.py           # Pydantic schemas for Seller (Create, Read)
│   │   └── __init__.py
│   ├── services/
│   │   ├── product.py          # Business logic for Product entity
│   │   ├── seller.py           # Business logic for Seller entity (hashing, auth)
│   │   └── __init__.py
│   ├── config.py               # Pydantic Settings configuration reading .env
│   └── __init__.py
├── main.py                     # FastAPI application entrypoint with lifespan
├── pyproject.toml              # Project dependencies and configurations
├── .env.example                # Template for environment variables
└── README.md
```

---

## ⚙️ Environment Configuration

Create a `.env` file in the project root (you can copy `.env.example`):

```bash
cp .env.example .env
```

Define the following PostgreSQL connection parameters:

```env
POSTGRES_USER=your_postgres_username
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_SERVER=your_host_or_ip
POSTGRES_PORT=5432
POSTGRES_DB=your_database_name
```

---

## 📦 Getting Started

### 1. Prerequisites
- **Python 3.12+**
- [uv](https://docs.astral.sh/uv/) (recommended) or `pip`

### 2. Installation

Clone the repository:
```bash
git clone <repository_url>
cd Database_Management_system
```

Install dependencies using `uv`:
```bash
uv sync
```

*(Alternatively, with standard pip/venv):*
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

### 3. Run the Application

Start the development server with FastAPI CLI:
```bash
fastapi dev main.py
```

Or using Uvicorn directly:
```bash
uvicorn main.py:app --reload
```

The server will start at `http://127.0.0.1:8000`.

---

## 📖 API Documentation

Once the server is running, explore the interactive documentation:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Summary of Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/product/?id={id}` | Retrieve product details by ID |
| `POST` | `/product/` | Create a new product |
| `PATCH` | `/product/?id={id}` | Partially update an existing product |
| `DELETE` | `/product/?id={id}` | Delete a product by ID |
| `POST` | `/seller/signup` | Register a new seller (with bcrypt password hashing) |
| `POST` | `/seller/login` | Seller login and authentication |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
