# Plan usage

> **Note:** To replay this exercise, please `git checkout 02-plan-usage`.

Claude Code can make large changes. To ensure that the changes made make sense, you can ask Claude Code to output a plan. This _plan mode_ will summarise the required changes, and might even be useful to input into a fresh context window in case your Claude Code session is running out.
.

For the purpose of this exercise, we will add a PATH book endpoint.

1. Open Claude Code

```sh
claude
```

2. Prompt it to make a change (copy prompt below)

```txt
Add a PATCH books endpoint.
Update the README.md, .http file, tests and src
Create a plan for the changes above and ask me to approve it before making the changes.
```

Claude Code output:

```txt
I'll enter plan mode to explore the codebase and design the implementation for the PATCH books endpoint.
...
Entered plan mode
...
The plan is ready. Here's a summary:

  PATCH /books/{book_id} Implementation Plan

  Files to modify (6 total):
  ┌─────────────────┬─────────────────────────────────────────────────────────────┐
  │      File       │                           Change                            │
  ├─────────────────┼─────────────────────────────────────────────────────────────┤
  │ schemas.py      │ Add BookUpdate model with all optional fields               │
  ├─────────────────┼─────────────────────────────────────────────────────────────┤
  │ routes.py       │ Add PATCH endpoint using existing update_book() db function │
  ├─────────────────┼─────────────────────────────────────────────────────────────┤
  │ README.md       │ Document the new endpoint                                   │
  ├─────────────────┼─────────────────────────────────────────────────────────────┤
  │ .http           │ Add PATCH request examples                                  │
  ├─────────────────┼─────────────────────────────────────────────────────────────┤
  │ test_routes.py  │ Add TestPatchBook class with 4 test cases                   │
  ├─────────────────┼─────────────────────────────────────────────────────────────┤
  │ test_schemas.py │ Add tests for BookUpdate schema                             │
  └─────────────────┴─────────────────────────────────────────────────────────────┘
  Key details:
  - Uses existing update_book() function from db layer
  - Returns 404 if book not found
  - Filters out None values to only update provided fields
  - Returns the updated book as BookResponse

──────────────────────────────────────────────────────────────────────────────────────────────────────────────
 Ready to code?

 Here is Claude's plan:
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
 Plan: Add PATCH /books/{book_id} Endpoint

 Overview

 Add a PATCH endpoint to partially update book resources. The infrastructure already supports this - the
 update_book() database function exists but isn't exposed via HTTP.

 Files to Modify

 1. Schema (books_api/src/books_api/http/books/schemas.py)

 - Add BookUpdate Pydantic model with all fields optional:
 class BookUpdate(BaseModel):
     title: str | None = None
     author: str | None = None
     description: str | None = None
     year: int | None = None

 2. Routes (books_api/src/books_api/http/books/routes.py)

 - Add PATCH endpoint:
 @router.patch("/{book_id}", response_model=BookResponse)
 def patch_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
     # Get existing book, return 404 if not found
     # Filter out None values from update data
     # Call update_book() from db layer
     # Return updated book

 3. README (books_api/README.md)

 - Add PATCH /books/{id} to the API endpoints table

 4. HTTP file (books_api/.http)

 - Add PATCH request examples (partial updates)

 5. Route Tests (books_api/test/http/books/test_routes.py)

 - Add TestPatchBook class with tests:
   - Patch existing book (single field)
   - Patch existing book (multiple fields)
   - Patch non-existent book (404)
   - Patch with empty body (no changes)

 6. Schema Tests (books_api/test/http/books/test_schemas.py)

 - Add tests for BookUpdate schema:
   - All fields optional
   - Partial updates valid
   - Empty update valid

 Verification

 1. Run just typecheck to verify types
 2. Run just fmt to format code
 3. Run tests with pytest
 4. Manual test with .http file
...
ACCEPT PLAN
...
I'll start implementing the PATCH endpoint. Let me set up the todo list and read the files I need to modify.
...
more changes relevant
...
All done. Here's a summary of the changes:

  Changes Made

  1. Schema (books_api/src/books_api/http/books/schemas.py)
  - Added BookUpdate model with all optional fields for partial updates

  2. Routes (books_api/src/books_api/http/books/routes.py)
  - Added PATCH /books/{book_id} endpoint that:
    - Returns 404 if book not found
    - Filters out None values to only update provided fields
    - Returns updated book as BookResponse

  3. README (books_api/README.md)
  - Added PATCH /books/{id} to the API endpoints list

  4. HTTP file (books_api/.http)
  - Added PATCH request example for manual testing

  5. Route tests (books_api/test/http/books/test_routes.py)
  - Added TestPatchBook class with 4 tests

  6. Schema tests (books_api/test/http/books/test_schemas.py)
  - Added TestBookUpdate class with 3 tests

  Verification:
  - Typecheck: passed
  - Format: passed
  - Tests: 49 passed
```

Notes:

- Plans can be used to reduce the context size for large features.
- Formatting and type checking are used since defined in `CLAUDE.md` (done in [claude-md](../01-claude-md/README.md)).
