# Skills

> **Note:** To replay this exercise, please `git checkout 04-skills`.

Although we have added some top-level workflow to apply in our [CLAUDE.md](../../CLAUDE.md), Claude Code also allows you to define [Agent Skills](https://code.claude.com/docs/en/skills) relevant to a specific task.

These skills are only loaded in when the relevant work is required (unlike `CLAUDE.md`).

This differs to [03-subagents](../03-subagents/README.md) in that subagents will create a whole new context, whilst a skill is only provies knowledge.

For this example, let's assume we want to create 2 new REST resources: users and borrowings, where users can borrow books.
We can define the skill [project-structure](../../.claude/skills/project-structure.md) that details how we structure `books_api`.

Let's create these two resources:

1. Open Claude Code

```sh
claude
```

2. Prompt (copy prompt below)

```txt
Can you create the CRUD operations for users, borrowings
Users can borrow books.
```

Claude Code output

```txt
I'll help you create CRUD operations for users and borrowings. Let me first explore the codebase to understand the existing structure.
...
Read(../claude-workloads/04-skills/README.md)
...
I've created the CRUD operations for users and borrowings following the existing project structure. Here's what was implemented:

  Users (/users)

  - Model: models/users.py - User with id, name, email fields
  - DB operations: db/users.py - get_all_users, get_user_by_id, create_user, update_user, delete_user
  - HTTP endpoints:
    - GET /users - List all users
    - GET /users/{user_id} - Get a specific user
    - POST /users - Create a new user
    - PATCH /users/{user_id} - Update a user
    - DELETE /users/{user_id} - Delete a user

  Borrowings (/borrowings)

  - Model: models/borrowings.py - Borrowing with id, user_id, book_id, borrowed_at, returned_at fields
  - DB operations: db/borrowings.py - get_all_borrowings, get_borrowing_by_id, get_borrowings_by_user, get_borrowings_by_book, create_borrowing, update_borrowing, return_book, delete_borrowing
  - HTTP endpoints:
    - GET /borrowings - List all borrowings (optionally filter by user_id)
    - GET /borrowings/{borrowing_id} - Get a specific borrowing
    - POST /borrowings - Create a new borrowing (validates user and book exist)
    - PATCH /borrowings/{borrowing_id} - Update a borrowing
    - DELETE /borrowings/{borrowing_id} - Delete a borrowing
    - POST /borrowings/{borrowing_id}/return - Mark a book as returned

  Tests

  Created comprehensive tests for both resources following the existing test patterns:
  - test/models/test_users.py, test/models/test_borrowings.py
  - test/db/test_users.py, test/db/test_borrowings.py
  - test/http/users/test_routes.py, test/http/borrowings/test_routes.py

  Typecheck and formatting have passed.
```

Note:

- This is a pretty small codebase, so we might want to split the test creation into its own subagent in larger codebases. The main agent will still read the skill, but this would reduce the context window.
- It's still using the CLAUDE.md we used.
