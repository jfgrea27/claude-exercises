# Claude Arena

The purpose of this repository is to document various exercises in Claude Code by modifying a simple [Books API](./books-api/) REST server written in Python.

## Exercises

The following exercises are available in the `claude-exercises/` directory:

| Exercise | Description | Branch |
|----------|-------------|--------|
| [00-basic-usage](./claude-exercises/00-basic-usage/) | Basic prompting with Claude Code | `00-basic-usage` |
| [01-claude-md](./claude-exercises/01-claude-md/) | Using `CLAUDE.md` for project-specific workflows | `01-claude-md` |
| [02-plan-usage](./claude-exercises/02-plan-usage/) | Using plan mode for larger changes | `02-plan-usage` |
| [03-subagents](./claude-exercises/03-subagents/) | Creating specialized subagents for task-specific workflows | `03-subagents` |
| [04-skills](./claude-exercises/04-skills/) | Defining agent skills for context-aware assistance | `04-skills` |

To replay an exercise, checkout the corresponding branch (e.g., `git checkout 00-basic-usage`).

## Books API Structure

```
books-api/
├── src/
│   └── books_api/       # Source code
│       ├── db/          # Database connection and CRUD operations
│       ├── http/        # HTTP routes and schemas
│       ├── models/      # SQLAlchemy models
│       ├── utils/       # Utilities (logging)
│       └── server.py    # FastAPI app entry point
└── test/                # Tests mirroring source structure
```

### API Endpoints

- `GET /books` - List all books
- `GET /books/{id}` - Get a book by ID
- `POST /books` - Create a new book
- `PATCH /books/{id}` - Partially update a book
- `DELETE /books/{id}` - Delete a book

## Setup

```bash
direnv allow
just install
```

## Available Commands

```bash
just serve      # Run the development server
just test       # Run tests
just test-cov   # Run tests with coverage
just lint       # Lint code
just fmt        # Format code
just typecheck  # Type check
just check      # Run all checks (lint, typecheck, test)
```
