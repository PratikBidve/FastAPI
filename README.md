# ZingHR Enterprise Employee Management API

An enterprise-grade, high-performance microservice architecture built for secure, scalable, and deterministic employee data management. This project utilizes a modern technical stack centered on **FastAPI**, **PostgreSQL**, and **Docker**, managed via the high-speed **uv** package manager.

---

## 🏗️ Project Architecture

The system is designed following the **Separation of Concerns (SoC)** principle, ensuring that business logic, data persistence, and API transport layers remain decoupled and independently testable.

### Core Architectural Pillars:

* **Transport Layer:** FastAPI (ASGI) providing high-concurrency request handling.
* **Persistence Layer:** PostgreSQL 15 (Alpine) for ACID-compliant relational storage.
* **Schema Evolution:** Alembic for versioned, transactional DDL migrations.
* **Validation Tier:** Pydantic v2 enforcing strict data contracts and environment configuration.
* **Orchestration:** Multi-stage Docker Compose with automated service health synchronization.

---

## 📂 Project Structure

```text
.
├── alembic/                # Database migration environment
│   ├── versions/           # Versioned migration scripts (Transactional DDL)
│   └── env.py              # Alembic configuration & Metadata discovery
├── app/                    # Primary Application logic
│   ├── api/                # API Route handlers
│   │   ├── dependencies.py # Dependency injection (DB Sessions)
│   │   └── v1/             # Versioned API endpoints
│   ├── core/               # Centralized Config & Security (Pydantic Settings)
│   ├── db/                 # Database Models & Engine configuration
│   └── schemas/            # Pydantic Data Contracts (Request/Response)
├── app/tests/              # Automated Test Suite (Pytest)
├── .env                    # Environment secrets (Git-ignored)
├── .gitignore              # Optimized for Python/uv/Docker
├── alembic.ini             # Alembic configuration file
├── docker-compose.yml      # Orchestration & Network bridging
├── Dockerfile              # Production-optimized container build
├── pyproject.toml          # uv/Project metadata
└── README.md               # Documentation

```

---

## 🚀 Getting Started

### Prerequisites

* Docker & Docker Compose
* [uv](https://github.com/astral-sh/uv) (Recommended for local dev)

### 1. Environment Setup

Create a `.env` file in the root directory:

```env
PROJECT_NAME="ZingHR Enterprise API"
VERSION="1.0.0"
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_SERVER=db
POSTGRES_PORT=5432
POSTGRES_DB=zinghr_db

```

### 2. Launch the Infrastructure

This command builds the API image, pulls PostgreSQL, and synchronizes the network.

```bash
docker compose up -d --build

```

### 3. Run Migrations

Apply the schema changes to the live database:

```bash
docker compose exec app alembic upgrade head

```

---

## 🛠️ API Endpoints (V1)

| Method | Endpoint | Description | Status Code |
| --- | --- | --- | --- |
| **POST** | `/api/v1/employees/` | Create a new employee record | `201` |
| **GET** | `/api/v1/employees/{id}` | Retrieve specific employee details | `200` |
| **PUT** | `/api/v1/employees/{id}` | Update existing employee data | `200` |
| **DELETE** | `/api/v1/employees/{id}` | Atomic removal of employee record | `204` |
| **GET** | `/health` | System readiness & health check | `200` |

> **Interactive Documentation:** Once the server is running, visit `http://localhost:8000/docs` for the full OpenAPI/Swagger specification.

---

## 🧪 Testing Strategy

The project employs a **Deterministic Testing Pattern**. Integration tests are executed against an isolated SQLite database to prevent environment pollution.

**Run the test suite:**

```bash
uv run pytest

```

### Features:

* **Dependency Overriding:** Swaps PostgreSQL for SQLite during test execution.
* **Transactional Rollbacks:** Every test starts with a clean schema and wipes data upon completion.
* **Schema Validation:** Ensures API responses strictly match Pydantic contracts.

---

## 🛡️ Design Decisions & Lessons

* **BigInteger for Salaries:** The database schema utilizes `BigInteger` for the salary column to accommodate high-precision financial data and prevent `NumericValueOutOfRange` errors common with standard 32-bit integers.
* **Transactional DDL:** migrations are configured to be atomic. If a schema change fails halfway, PostgreSQL rolls back the entire operation to maintain system integrity.
* **Healthchecks:** The `docker-compose` file includes a `pg_isready` check, ensuring the FastAPI application only attempts to connect once the database is fully initialized and accepting traffic.

---

## 👤 Author

**Prateek A. Bidve**
*Senior Full Stack Engineer & AI Architect*

---

### Final Interview Quick-Ref

If asked about the **"Deep Why"** of this setup:

> "This architecture prioritizes **Environment Parity**. By using Docker volumes for hot-reloads and Alembic for schema-as-code, we eliminate 'works on my machine' issues. The use of `uv` ensures deterministic dependency resolution, while the isolated testing suite guarantees that our CI/CD pipelines can validate business logic without risking production data integrity."