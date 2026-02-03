# Personal Finance Tracker

> A full-stack application to practice SOLID, DRY, TDD, and BDD principles using FastAPI and React.js

---

## Project Goal

Build a personal finance management system where users can track expenses, set budgets, and create custom automation rules — applying clean architecture patterns and software design principles across the stack.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | FastAPI, Uvicorn, Python 3.11+ |
| **Dependency Management** | Poetry |
| **ORM** | SQLAlchemy 2.0 (async) |
| **Database** | PostgreSQL |
| **Migrations** | Alembic |
| **Validation** | Pydantic v2 |
| **Authentication** | python-jose (JWT), passlib (bcrypt), httpx (OAuth) |
| **Testing** | pytest, pytest-asyncio, pytest-bdd, httpx |
| **Frontend** | React.js 18+, TypeScript |
| **State/Fetch** | TanStack Query (React Query) |
| **Forms** | React Hook Form + Zod |
| **Routing** | React Router v6 |
| **Styling** | Tailwind CSS |

---

## Core Features

### 1. Transaction Management
- Create, read, update, and delete transactions
- Categorize transactions (food, transport, bills, etc.)
- Filter and search by date, category, amount

### 2. Budget System
- Set monthly budgets per category
- Track progress against budget limits
- Visual indicators for budget health

### 3. Rules Engine
- Custom automation rules ("when X happens, do Y")
- Rule types: spending limits, date triggers, category alerts
- Notification system (email, push) when rules are triggered

### 4. Dashboard & Analytics
- Monthly spending overview
- Category breakdown charts
- Trend analysis over time

### 5. Data Import/Export
- CSV import for bank statements
- Export transactions to CSV/PDF

### 6. Authentication & Authorization
- User registration and login (JWT-based)
- OAuth2 integration (Google, GitHub)
- Role-Based Access Control (RBAC)
- Permission-based resource access
- Refresh token rotation

---

## Architecture Overview

### Simple Layered Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   api/v1/endpoints/                     │
│        (Request handling, validation, responses)        │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                      services/                          │
│            (Business logic, orchestration)              │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                 models/ + schemas/                      │
│       (SQLAlchemy models, Pydantic validation)          │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                     PostgreSQL                          │
└─────────────────────────────────────────────────────────┘
```

**Why no Repository Pattern?**
- SQLAlchemy 2.0 is already an abstraction over the database
- FastAPI's `Depends()` makes session injection and mocking straightforward
- Adds boilerplate without real benefit at this project scale
- You'll practice plenty of patterns elsewhere (Strategy, Factory, DI)

---

## Authentication & Authorization

### Authentication Flow

```
┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
│  Client  │──1──▶│  Login   │──2──▶│  Auth    │──3──▶│ Database │
│          │      │ Endpoint │      │ Service  │      │          │
└──────────┘      └──────────┘      └──────────┘      └──────────┘
     │                                   │
     │◀──────────── 4 ───────────────────┘
     │         (JWT + Refresh Token)
     │
     │            ┌──────────┐      ┌──────────┐
     └─────5────▶│ Protected│──6──▶│  Auth    │
                 │ Endpoint │      │ Middleware│
                 └──────────┘      └──────────┘
                      │                  │
                      │◀───── 7 ─────────┘
                      │    (User Context)
```

### Authorization Model (RBAC)

```
┌─────────────────────────────────────────────────────────┐
│   USERS  ──▶  ROLES  ──▶  PERMISSIONS                   │
│                                                         │
│   Admin  ──▶  admin  ──▶  transaction:read/write        │
│                          budget:read/write              │
│                          rule:read/write                │
│                          user:manage                    │
│                                                         │
│   User   ──▶  user   ──▶  transaction:read/write        │
│                          budget:read/write              │
│                          rule:read                      │
│                                                         │
│   Viewer ──▶  viewer ──▶  transaction:read              │
│                          budget:read                    │
└─────────────────────────────────────────────────────────┘
```

#### Permission Matrix

| Permission | Admin | Premium | User | Viewer |
|------------|:-----:|:-------:|:----:|:------:|
| `transaction:read` | ✓ | ✓ | ✓ | ✓ |
| `transaction:write` | ✓ | ✓ | ✓ | ✗ |
| `budget:read` | ✓ | ✓ | ✓ | ✓ |
| `budget:write` | ✓ | ✓ | ✓ | ✗ |
| `rule:read` | ✓ | ✓ | ✓ | ✓ |
| `rule:write` | ✓ | ✓ | ✗ | ✗ |
| `reports:export` | ✓ | ✓ | ✗ | ✗ |
| `user:manage` | ✓ | ✗ | ✗ | ✗ |

---

### Auth Database Models

| Model | Purpose | Key Fields |
|-------|---------|------------|
| **User** | User account | email, hashed_password, is_active, is_verified |
| **Role** | Role definitions | name, description |
| **Permission** | Permission definitions | name (e.g., "transaction:write") |
| **OAuthAccount** | OAuth provider links | provider, provider_user_id |
| **RefreshToken** | Token management | token, expires_at, is_revoked |

**Relationships:** Users ↔ Roles (M2M), Roles ↔ Permissions (M2M)

---

### Auth Services

| Service | Location | Responsibility |
|---------|----------|----------------|
| **AuthService** | `services/auth.py` | Registration, login, token refresh, logout |
| **TokenService** | `core/security.py` | JWT creation and validation |
| **PasswordService** | `core/security.py` | Password hashing/verification (bcrypt) |
| **OAuthProviders** | `oauth/` | Strategy pattern for Google, GitHub, etc. |

---

### Auth Security Practices

| Practice | Implementation |
|----------|----------------|
| **Password Hashing** | bcrypt with cost factor 12 |
| **Token Storage** | HttpOnly cookies for refresh tokens |
| **Token Expiry** | Access: 15min, Refresh: 7 days |
| **Refresh Rotation** | New refresh token on each refresh |
| **Rate Limiting** | 5 login attempts per minute |
| **Input Validation** | Pydantic schemas with strict rules |

---

## Design Patterns In Use

| Pattern | Location | Purpose |
|---------|----------|---------|
| **Strategy** | `services/rule/strategies/` | Different rule types share same interface |
| **Strategy** | `oauth/` | Google, GitHub implement same protocol |
| **Strategy** | `notifications/` | Email, Push, SMS implement same interface |
| **Factory** | `oauth/factory.py` | Creates provider instance by name |
| **Factory** | `services/rule/factory.py` | Creates rule instance by type |
| **Dependency Injection** | `api/v1/dependencies.py` | FastAPI's `Depends()` for auth, session |

---

## SOLID Principles Application

### Backend (FastAPI)

| Principle | Implementation |
|-----------|----------------|
| **Single Responsibility** | `endpoints/` handles HTTP, `services/` handles logic, `models/` handles data |
| **Open/Closed** | Rule strategies and OAuth providers extend without modifying core |
| **Liskov Substitution** | All OAuth providers / notifiers / rules implement same protocol |
| **Interface Segregation** | Schemas split: `TransactionCreate`, `TransactionRead`, `TransactionUpdate` |
| **Dependency Inversion** | Services receive session via `Depends()`, easily mockable |

### Frontend (React)

| Principle | Implementation |
|-----------|----------------|
| **Single Responsibility** | Small components: `TransactionList`, `TransactionItem`, `BudgetProgressBar` |
| **Open/Closed** | Generic `<DataTable>` accepts configs and custom renderers |
| **Dependency Inversion** | Components receive services via context/props |

---

## DRY Principles Application

### Backend
- **Shared Schemas**: Common Pydantic validators and base schemas
- **Utility Functions**: Date formatting, currency helpers in `utils/`
- **Centralized Config**: All settings in `core/config.py`
- **Exception Handlers**: Single error handling middleware
- **Base Model**: Common fields (id, created_at, updated_at) in `models/base.py`

### Frontend
- **Custom Hooks**: `useTransactions()`, `useBudgets()` encapsulate data logic
- **Shared Schemas**: Zod schemas reused across forms
- **Component Composition**: UI primitives composed into features
- **API Service Layer**: Single source for API calls

---

## Project Structure

```
personal-finance-tracker/
│
├── backend/
│   ├── src/
│   │   └── app/
│   │       ├── api/
│   │       │   └── v1/
│   │       │       ├── endpoints/
│   │       │       │   ├── auth.py
│   │       │       │   ├── transactions.py
│   │       │       │   ├── budgets.py
│   │       │       │   ├── categories.py
│   │       │       │   └── rules.py
│   │       │       ├── router.py            # Aggregates all v1 routes
│   │       │       └── dependencies.py      # API-level deps (auth, permissions)
│   │       │
│   │       ├── core/
│   │       │   ├── config.py                # Settings via pydantic-settings
│   │       │   ├── database.py              # Async engine + session factory
│   │       │   ├── security.py              # Password hashing, JWT utils
│   │       │   └── exceptions.py            # Custom exceptions + handlers
│   │       │
│   │       ├── models/                      # SQLAlchemy models
│   │       │   ├── base.py                  # Base model class
│   │       │   ├── user.py
│   │       │   ├── transaction.py
│   │       │   ├── budget.py
│   │       │   ├── category.py
│   │       │   └── rule.py
│   │       │
│   │       ├── schemas/                     # Pydantic schemas
│   │       │   ├── auth.py
│   │       │   ├── user.py
│   │       │   ├── transaction.py
│   │       │   ├── budget.py
│   │       │   └── rule.py
│   │       │
│   │       ├── services/                    # Business logic
│   │       │   ├── auth.py                  # AuthService, TokenService
│   │       │   ├── transaction.py
│   │       │   ├── budget.py
│   │       │   └── rule/
│   │       │       ├── engine.py            # RuleEngine orchestrator
│   │       │       ├── base.py              # Rule protocol
│   │       │       ├── factory.py
│   │       │       └── strategies/
│   │       │           ├── spending_limit.py
│   │       │           ├── date_trigger.py
│   │       │           └── category_alert.py
│   │       │
│   │       ├── oauth/                       # OAuth providers (Strategy pattern)
│   │       │   ├── base.py                  # OAuthProvider protocol
│   │       │   ├── google.py
│   │       │   ├── github.py
│   │       │   └── factory.py
│   │       │
│   │       ├── notifications/               # Notification channels
│   │       │   ├── base.py                  # Notifier protocol
│   │       │   ├── email.py
│   │       │   └── push.py
│   │       │
│   │       ├── utils/
│   │       │   └── helpers.py
│   │       │
│   │       └── main.py                      # FastAPI app factory
│   │
│   ├── tests/
│   │   ├── conftest.py                      # Fixtures, test DB setup
│   │   ├── factories.py                     # factory-boy factories
│   │   ├── unit/
│   │   │   ├── services/
│   │   │   └── oauth/
│   │   ├── integration/
│   │   │   └── api/
│   │   └── bdd/
│   │       ├── features/
│   │       │   ├── auth.feature
│   │       │   └── budget_alerts.feature
│   │       └── steps/
│   │
│   ├── alembic/
│   │   ├── versions/
│   │   └── env.py
│   │
│   ├── pyproject.toml
│   ├── poetry.lock
│   └── alembic.ini
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/
│   │   │   ├── auth/
│   │   │   └── features/
│   │   ├── contexts/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── schemas/
│   │   ├── pages/
│   │   └── utils/
│   ├── e2e/
│   ├── package.json
│   └── tsconfig.json
│
├── docker-compose.yml
└── README.md
```

---

## Backend Architecture Explained

### Why This Structure?

| Convention | Reason |
|------------|--------|
| **`src/` layout** | Python packaging best practice, avoids import conflicts |
| **`api/v1/`** | API versioning from day one, easy to add v2 later |
| **Separated `models/`, `schemas/`, `services/`** | Clear boundaries, easier to navigate in larger codebases |
| **`endpoints/` vs `router.py`** | Endpoints handle HTTP, router aggregates them |
| **`core/`** | Cross-cutting concerns: config, database, security |
| **Strategy folders** | `oauth/`, `notifications/`, `services/rule/strategies/` — pattern is explicit |

### Layer Responsibilities

```
┌─────────────────────────────────────────────────────────┐
│                    api/v1/endpoints/                    │
│         (HTTP handling, validation, responses)          │
└────────────────────────┬────────────────────────────────┘
                         │ calls
                         ▼
┌─────────────────────────────────────────────────────────┐
│                      services/                          │
│              (Business logic, orchestration)            │
└────────────────────────┬────────────────────────────────┘
                         │ uses
                         ▼
┌─────────────────────────────────────────────────────────┐
│              models/ + schemas/ + core/                 │
│       (Data layer, validation, configuration)           │
└─────────────────────────────────────────────────────────┘
```

---

## Poetry Configuration

### Dependency Groups

| Group | Packages |
|-------|----------|
| **main** | fastapi, uvicorn[standard], sqlalchemy[asyncio], asyncpg, pydantic, pydantic-settings, python-jose[cryptography], passlib[bcrypt], httpx, alembic |
| **dev** | ruff, mypy, pre-commit |
| **test** | pytest, pytest-asyncio, pytest-bdd, pytest-cov, httpx, factory-boy |

### Package Configuration (pyproject.toml)

| Setting | Value | Purpose |
|---------|-------|---------|
| `packages` | `[{include = "app", from = "src"}]` | src layout support |
| `python` | `^3.11` | Minimum Python version |
| `[tool.pytest.ini_options]` | `pythonpath = ["src"]` | Test imports work correctly |
| `[tool.ruff]` | `src = ["src"]` | Linter knows src layout |

---

## API Endpoints

### Authentication
| Method | Endpoint | Auth |
|--------|----------|------|
| POST | `/api/v1/auth/register` | Public |
| POST | `/api/v1/auth/login` | Public |
| POST | `/api/v1/auth/refresh` | Public |
| POST | `/api/v1/auth/logout` | Protected |
| GET | `/api/v1/auth/me` | Protected |
| GET | `/api/v1/auth/oauth/{provider}` | Public |
| GET | `/api/v1/auth/oauth/{provider}/callback` | Public |

### Transactions
| Method | Endpoint | Permission |
|--------|----------|------------|
| GET | `/api/v1/transactions` | `transaction:read` |
| POST | `/api/v1/transactions` | `transaction:write` |
| PUT | `/api/v1/transactions/{id}` | `transaction:write` |
| DELETE | `/api/v1/transactions/{id}` | `transaction:write` |

### Budgets
| Method | Endpoint | Permission |
|--------|----------|------------|
| GET | `/api/v1/budgets` | `budget:read` |
| POST | `/api/v1/budgets` | `budget:write` |
| GET | `/api/v1/budgets/{id}/progress` | `budget:read` |

### Rules
| Method | Endpoint | Permission |
|--------|----------|------------|
| GET | `/api/v1/rules` | `rule:read` |
| POST | `/api/v1/rules` | `rule:write` |
| POST | `/api/v1/rules/evaluate` | `rule:write` |

---

## TDD/BDD Methodology

### TDD Workflow

```
┌─────────┐    ┌─────────┐    ┌──────────┐
│   RED   │───▶│  GREEN  │───▶│ REFACTOR │───┐
│  Write  │    │  Write  │    │  Clean   │   │
│ failing │    │ minimal │    │   code   │   │
│  test   │    │  code   │    │          │   │
└─────────┘    └─────────┘    └──────────┘   │
     ▲                                       │
     └───────────────────────────────────────┘
```

### BDD Example Scenarios

**Authentication:**
- Register → receive verification email
- Login valid → receive tokens
- Login invalid → error, no tokens
- No token → 401
- No permission → 403

**Budget Alerts:**
- Exceed budget → alert notification
- Within budget → no alert

---

### Test Pyramid

```
                    ┌───────────┐
                    │    E2E    │  ← Few
                   ─┴───────────┴─
                  ┌───────────────┐
                  │  Integration  │  ← Medium
                 ─┴───────────────┴─
                ┌───────────────────┐
                │    Unit Tests     │  ← Many
                └───────────────────┘
```

### Testing Tools

| Layer | Tool | Location |
|-------|------|----------|
| Backend Unit | pytest, pytest-asyncio | `tests/unit/` |
| Backend BDD | pytest-bdd | `tests/bdd/features/` + `tests/bdd/steps/` |
| Backend Integration | httpx, TestClient | `tests/integration/` |
| Test Fixtures | factory-boy | `tests/factories.py` |
| Frontend Unit | Jest, Vitest | `src/**/__tests__/` |
| Frontend Components | React Testing Library | `src/components/**/__tests__/` |
| Frontend E2E | Playwright | `e2e/` |

---

## Development Phases

### Phase 1: Foundation
- [ ] Project scaffolding with src layout
- [ ] Poetry setup with dependency groups (main, dev, test)
- [ ] Core setup: config, database, exceptions
- [ ] Base model with common fields
- [ ] Alembic configuration
- [ ] Testing infrastructure (conftest.py, factories.py)
- [ ] Transaction CRUD with TDD
- [ ] Category management

### Phase 2: Authentication
- [ ] User, Role, Permission models in `models/`
- [ ] Security utilities in `core/security.py` (TDD)
- [ ] AuthService in `services/auth.py` (TDD)
- [ ] Auth dependencies in `api/v1/dependencies.py`
- [ ] Auth endpoints in `api/v1/endpoints/auth.py`
- [ ] OAuth providers in `oauth/` (Strategy pattern)
- [ ] Frontend: AuthContext, forms, ProtectedRoute

### Phase 3: Budget & Rules
- [ ] Budget service and endpoints
- [ ] Rule engine in `services/rule/` (TDD)
- [ ] Rule strategies: spending_limit, date_trigger
- [ ] Notification channels in `notifications/`
- [ ] BDD feature files in `tests/bdd/features/`

### Phase 4: Dashboard
- [ ] Dashboard components
- [ ] Charts (Recharts)
- [ ] Monthly reports

### Phase 5: Polish
- [ ] CSV import/export
- [ ] E2E tests with Playwright
- [ ] Security audit
- [ ] Documentation

---

## Learning Outcomes

By completing this project, you will have practiced:

1. **SOLID Principles** — SRP, OCP, LSP, ISP, DIP in Python and TypeScript
2. **Design Patterns** — Strategy, Factory, Dependency Injection
3. **TDD** — Red-Green-Refactor cycle
4. **BDD** — Gherkin syntax, feature files
5. **Authentication** — JWT, OAuth2, password hashing
6. **Authorization** — RBAC, permissions
7. **FastAPI** — Async, `Depends()`, Pydantic, middleware
8. **React** — Hooks, context, TypeScript
9. **Testing** — Unit, integration, E2E
10. **Database Design** — Relational modeling, migrations

---

## Resources

### Core
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)
- [React Query Documentation](https://tanstack.com/query/latest)

### Architecture
- [SOLID Principles in Python](https://realpython.com/solid-principles-python/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

### Auth
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [OAuth 2.0 Simplified](https://aaronparecki.com/oauth-2-simplified/)
- [JWT.io](https://jwt.io/introduction)
- [OWASP Auth Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

### Testing
- [pytest-bdd](https://pytest-bdd.readthedocs.io/)
- [TDD with Python](https://www.obeythetestinggoat.com/)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [Playwright](https://playwright.dev/docs/intro)
