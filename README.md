# Avito-like API

A educational REST API for mobile development students.

This project demonstrates how a mobile application can communicate with a REST API backend, including authentication, user profiles, marketplace listings, messaging, and image uploads.

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

1. Clone the repository:

    ```bash
    git clone https://github.com/aiinty/avito-like-api.git
    cd avito-like-api
    ```

2. Create a `.env` file based on `.env.example` and configure it.
3. Then build and start the application:

    ```bash
    docker compose up --build
    ```

During container startup:

1. PostgreSQL is started
2. Alembic applies migrations
3. Initial categories data is inserted by the `seed.py`
4. The FastAPI application is started

## API

The API will be available at:

```text
http://localhost:8000
```

API documentation is available at:

```text
http://localhost:8000/docs
```

The main API endpoints are:

| Endpoint | Description |
| --- | --- |
| `/auth` | Registration, login, token refresh |
| `/user` | Current user, user update, items of certain user |
| `/items` | Marketplace items |
| `/categories` | Categories of items |
| `/items/{id}/messages` | Messages for an item |
| `/upload` | Image uploads |

For the complete list of endpoints and request/response schemas, use the automatically generated Swagger documentation at `/docs`

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
