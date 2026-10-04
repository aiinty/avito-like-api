# Avito-like API

A training REST API for mobile development.

This project is designed for students to demonstrate how a mobile application can communicate with a REST API. The API provides a simple marketplace model with user authentication, advertisements, categories, messaging, and image uploads.

## Features

- User registration and authentication
- JWT access/refresh tokens
- User profiles
- Marketplace items and categories
- Item creation, editing, and deletion
- Item filtering and pagination
- Messages associated with items
- Image uploading

## Technology Stack

- **Python 3.12**
- **FastAPI** - REST API framework
- **SQLModel (SQLAlchemy)** - database models and ORM
- **PostgreSQL** - relational database
- **asyncpg** - asynchronous PostgreSQL driver
- **Alembic** - database migrations
- **Pydantic** - data validation and serialization
- **JWT** - authentication
- **Docker / Docker Compose** - application and database containers
- **Uvicorn** - ASGI server

## Project Structure

```text
.
├── src/
│   ├── db/                # Database configuration
│   ├── modules/
│   │   ├── auth/          # Authentication and JWT
│   │   ├── users/         # User module
│   │   ├── items/         # Marketplace items
│   │   ├── categories/    # Item categories
│   │   ├── messages/      # Item messages
│   │   └── files/         # File uploads
│   │
│   ├── utils/             # Shared utilities and seed data
│   └── main.py            # FastAPI application
│
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── entrypoint.sh
└── requirements.txt
```

## Docker quick start

Create a `.env` file based on `.env.example` and configure the PostgreSQL and JWT settings.

Then start the application:

```bash
docker compose up --build
```

During container startup:

1. PostgreSQL is started
2. Alembic applies pending migrations
3. Initial data is inserted by the seed script
4. The FastAPI application is started

The API will be available at:

```text
http://localhost:8000
```

API documentation is available at:

```text
http://localhost:8000/docs
```

## Authentication

The API uses JWT-based authentication.

A successful login returns:

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer"
}
```

The access token is used to access protected endpoints:

```http
Authorization: Bearer <access_token>
```

## API

The main API endpoints are:

| Endpoint | Description |
| --- | --- |
| `/auth` | Registration, login, token refresh, current user |
| `/items` | Marketplace items |
| `/items/{id}/messages` | Messages for an item |
| `/upload` | Image uploads |

For the complete list of endpoints and request/response schemas, use the automatically generated Swagger documentation at `/docs`
