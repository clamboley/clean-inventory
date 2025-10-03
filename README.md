# Inventory Management App

An internal web application for managing IT company assets (computers, peripherals, etc.).  
Built to easily create, track, transfer, and update inventory items without confusion.  
Designed with a **clean architecture** in mind, with **FastAPI + PostgreSQL backend**, and a **React + Mantine frontend**.

## Features

- 📦 **Inventory Management**
  - List, filter, and search items by any field.
  - View personal inventory or the full company inventory.
  - Add new items via form or bulk import (Excel).
  - Export personal or filtered inventory to Excel.

- 📝 **Item Updates & Workflow**
  - Users can directly edit their own items.
  - Changes to others’ items generate a **ticket** for approval.
  - Managers/admins can approve or reject tickets.

- 🔐 **Authentication & Authorization**
  - Secure login with JWT tokens.
  - Role-based access: `user`, `manager`, `admin`.

- 🔔 **Notifications**
  - Real-time alerts when items are assigned, tickets created, or approved.

- 📜 **History & Audit**
  - Track all movements and changes with timestamps and responsible users.

## Tech Stack

### Backend
- [Python](https://www.python.org/) with [uv](https://docs.astral.sh/uv/) as package/runtime manager
- [FastAPI](https://fastapi.tiangolo.com/) for REST API
- [PostgreSQL](https://www.postgresql.org/) as database
- [SQLAlchemy](https://www.sqlalchemy.org/) for ORM
- [Pydantic](https://docs.pydantic.dev/) for request/response validation
- Clean Architecture principles (entities, services, repositories, controllers)
- JWT authentication

### Frontend
- [React](https://react.dev/) with [Vite](https://vitejs.dev/) for bundling
- [TypeScript](https://www.typescriptlang.org/) for type safety
- [Mantine](https://mantine.dev/) for UI components
- [React Router](https://reactrouter.com/) for navigation

### DevOps & Tooling
- TODO

## Project Structure

```bash
.
├── backend/            # FastAPI backend (Clean Architecture)
│   ├── app/
│   │   ├── api/             # API layer
│   │   │   ├── controllers  # FastAPI routers (auth, items, users)
│   │   │   └── validators   # Pydantic models for requests/responses
│   │   ├── business/        # Core domain & use cases
│   │   │   ├── entities     # Domain models (Item, User, etc.)
│   │   │   └── services     # Business logic
│   │   ├── connections/     # External connections
│   │   │   ├── dao          # Database session/DAO
│   │   │   └── repositories # Persistence layer (PostgreSQL repos)
│   │   ├── core/            # App config, DI container, logging, security
│   │   ├── exceptions/      # Domain-specific exceptions
│   │   └── main.py
│   ├── migrations/          # Alembic migrations
│   ├── pyproject.toml
│   └── uv.lock
│
├── frontend/            # React + Mantine frontend
│   ├── src/
│   │   ├── api              # API client
│   │   ├── components/      # Reusable UI components (layout, common widgets)
│   │   ├── contexts/        # Global state management
│   │   ├── hooks/           # Custom stateful logic
│   │   ├── models/          # Type models & interface definitions
│   │   ├── pages/           # Application pages (Inventory, Dashboard, etc.)
│   │   ├── services/        # General business logic and utilities
│   │   ├── styles/          # Global styles, CSS modules
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── Router.tsx
│   ├── package.json
│   ├── vite.config.mjs
│   └── yarn.lock
│
└── README.md
```

## Getting Started

TODO
