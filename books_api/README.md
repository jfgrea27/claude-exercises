# Books API

A simple REST API for managing books built with FastAPI and SQLAlchemy.

## Structure

```
books_api/
├── src/
│   └── books_api/       # Source code
│       ├── db/          # Database connection and CRUD operations
│       ├── http/        # HTTP routes and schemas
│       ├── models/      # SQLAlchemy models
│       ├── utils/       # Utilities (logging)
│       └── server.py    # FastAPI app entry point
└── test/                # Tests mirroring source structure
```

## API Endpoints

- `GET /books` - List all books
- `GET /books/{id}` - Get a book by ID
- `POST /books` - Create a new book
- `PATCH /books/{id}` - Partially update a book
- `DELETE /books/{id}` - Delete a book
