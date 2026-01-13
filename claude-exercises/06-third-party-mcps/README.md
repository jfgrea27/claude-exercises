# Third-party MCPs

> **Note:** To replay this exercise, please `git checkout 06-third-party-mcps`.

In [05-mcps](../05-mcps/README.md), we used extended Claude Code's context with a local MCP.

In this exercise, we will explore a third-party MCP, namely [Atlassian Rovo](https://www.atlassian.com/platform/remote-mcp-server) that allows you to create and complete Jira tickets.

For the purpose of this exercies, assume that the following ticket is present in Jira:

Epic: Add book type

```
Description
Users would like to view a top level type of the book.
The list of book types can be one of
	•	fiction
	•	non_fiction
	•	unknown
Please add this to books_api, fixing the tests etc.
The code coverage should still be passed 80%.

```

with the following linked tasks

```
Task 1: Update db schema of books to include book_type
Task 2: Update REST endpoints for books to include book_type
```

Notes:

- ALthough these were human written, Claude Code can also create these tickets and you could create a subagent using plan-mode to help you with that task.

Let's now ask Claude Code to implement this!

> **Note:** If you just want to follow and want to see the differences, Claude Code committed changes to the branch `dev-4`.

1. Open Claude Code

```sh
claude
```

2. Login into Atlassian mcp

```sh # inside claude code
/mcp
# login
```

3. Prompt (copy)

```txt
can you implement ticket EPIC_TICKET_ID.
- Create a branch EPIC_TICKET_ID
- For each task in the epic:
  - Create a commit with implementation
```

Here add your own EPIC_TICKET_ID

Claude Code output:

```
I'll fetch the details of epic DEV-4 from Jira.
...
I found the epic. DEV-4: Add book type requires:
  - Adding a book type field to books_api with values: fiction, non_fiction, unknown
  - Fixing tests and maintaining 80% code coverage
...
I found 2 tasks under the DEV-4 epic:

  1. DEV-5: Update db schema of books to include book_type (use enums)
  2. DEV-6: Update REST endpoints for books to include book_type (default to unknown)
...
Let me explore the books_api codebase to understand the current structure.
...
I'm now in plan mode. I already have a good understanding of the codebase from the exploration. Let me read the key files to understand the exact patterns, then create the implementation plan.
...
Implementation Plan: DEV-4 - Add Book Type

 Summary

 Add a book_type field to the books_api with values: fiction, non_fiction, unknown.

 Jira Tasks

 Task 1: DEV-5 - Update db schema of books to include book_type

 Description: Use enums for the book_type field

 Steps:
 1. Create BookType Python enum in books-api/src/books_api/models/books.py
   - Values: FICTION = "fiction", NON_FICTION = "non_fiction", UNKNOWN = "unknown"
 2. Add book_type field to Book model using SQLAlchemy Enum type
   - Default to BookType.UNKNOWN, nullable=False
 3. Add tests in books-api/test/models/test_books.py
 4. Add tests in books-api/test/db/test_books.py

 Task 2: DEV-6 - Update REST endpoints for books to include book_type

 Description: Default to unknown if book_type not provided

 Steps:
 1. Update Pydantic schemas in books-api/src/books_api/http/books/schemas.py
   - Add book_type: BookType = BookType.UNKNOWN to BookBase
   - Add book_type: BookType | None = None to BookUpdate
 2. Add tests in books-api/test/http/books/test_schemas.py
 3. Add tests in books-api/test/http/books/test_routes.py

 Git Workflow

 1. Create branch dev-4 from main
 2. Execute DEV-5 → commit with message referencing DEV-5
 3. Execute DEV-6 → commit with message referencing DEV-6

 Execution Order

 1. Create git branch dev-4
 2. Implement DEV-5 (db schema) → just check → commit
 3. Implement DEV-6 (REST endpoints) → just check → commit

 Verification (after both tasks complete)

 1. Run just test - all tests pass
 2. Run just test-cov - coverage >= 80%
 3. Run just typecheck - no type errors
 4. Run just fmt - code formatted
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

 Requested permissions:
   · Bash(prompt: run tests)
   · Bash(prompt: run type checking)
   · Bash(prompt: run code formatting)
   · Bash(prompt: create git branch)
   · Bash(prompt: git commit)
...
Plan approved. Let me start implementing.
...

```

The commits look like this:

```
commit f5902a47f639e9f6081ad5bcb8378e99f9e28277 (HEAD -> dev-4, origin/dev-4)
Author: James Rea <jfgrea27@gmail.com>
Date:   Tue Jan 13 08:59:24 2026 +0000

    DEV-6: Update REST endpoints for books to include book_type

    Add book_type field to Pydantic schemas (BookBase, BookUpdate).
    Default to unknown if book_type not provided.

    Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

commit 8e60b642c7c0800b3ecc3215cf5242577ee90060
Author: James Rea <jfgrea27@gmail.com>
Date:   Tue Jan 13 08:57:34 2026 +0000

    DEV-5: Update db schema of books to include book_type

    Add BookType enum with values: fiction, non_fiction, unknown.
    Add book_type field to Book model with default of unknown.

    Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

which matches what was written in JIRA.

Notes:

- This is quite a small task and so we can put it all in one context window in Claude Code's main agent. For larger items, perhaps use a subagent per task since this will have a fresh context.
