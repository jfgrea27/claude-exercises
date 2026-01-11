# Subagents

> **Note:** To replay this exercise, please `git checkout 03-subagents`.

Subagents are specialized AI subagents in Claude Code for task-specific workflows.

You can manage agents via the `/agents` command in Claude Code.

In this example, we will fix a duplicate rows in database bug. To make this more general, and to use TDD approach, we will create `bug-fixer` agent that will write a test for the failing test, fix the bug and see the test pass.

1. Open Claude Code

```sh
claude
# start the agent wizard
/agent
```

2. Create agent (copy prompt)

```txt
You are an export bug fixer that uses TDD approach: write test, fix bug, see test pass.
```

Notes:

- A subagent will use a Markdown prompt for the specialised task it knows, you can edit that as much as you want
- You can specify project or system-wide agents. Here we chose project-wide so that you can see it in the project.
- Claude Code will invoke the subagent when it believes it is relevant

3. Prompt for the bug (copy)

```txt
There is a bug in the code, I see two times the same book title in the database.
```

Claude Code output:

```sh
I'll use the bug-fixer-tdd agent to investigate and fix the duplicate books issue using a test-driven approach.
...
bug-fixer-tdd(Fix duplicate books bug)
...
The bug has been fixed. Here's what was done:

  Problem: The Book model had no unique constraint on the title field, allowing duplicate books to be created.

  Fix: Added unique=True to the title column in books_api/src/books_api/models/books.py:10:

  title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

  Test added: A new test test_cannot_create_duplicate_book_with_same_title verifies that attempting to create a duplicate book now raises an IntegrityError.

  All 50 tests pass, typecheck passes, and formatting is correct. You'll need to recreate your database to apply the new schema constraint (the existing duplicates were cleared when the test database was recreated).
```

Notes:

We see that a test was added.
