# Claude md - the basics

> **Note:** To replay this exercise, please `git checkout 01-claude-md`.

Claude Code can automatically pull the repository context including tools it can use, core files, etc. by reading the contents of a `CLAUDE.md` file, as described in [claude-code-best-practices](https://www.anthropic.com/engineering/claude-code-best-practices).

In our previous [00-basic-usage](../00-basic-usage/README.md), Claude Code did not run the linting and typing checks. Let's create a `Claude.md` file so that it can carry out specific workflows when updating code.

We will visit the same feature as [00-basic-usage](../00-basic-usage/README.md), namely adding logging.

1. Open Claude Code

```sh
claude
```

2. Prompt it to make a change (copy prompt below)

```txt
Add more logging to books_api
- info for starting/ending of requests.
- debug for any db interaction
```

Claude Code output:

```
I can see the logger is already set up. I'll add the logging statements to both files.
...
Now I'll run typecheck and format as per the project instructions.
...
Bash(just typecheck) # this is the type checking
...
Bash(just fmt) # this is the formating
...
 Done. I added logging to the books_api:

  Routes (routes.py): Info-level logging for request start/end
  - GET /books, GET /books/{id}, POST /books, DELETE /books/{id}

  DB layer (db/books.py): Debug-level logging for all database operations
  - get_all_books - query and result count
  - get_book_by_id - query and found/not found
  - create_book - input data and created id
  - update_book - book id and update data
  - delete_book - book id being deleted

  Typecheck passed and code was formatted.
```

This completes the feature request as expected and with the corresponding formatting.

It is worth noting that since Claude Code has a limited context window size, the `CLAUDE.md` is part of this context window, and so make sure the file's content is succinct.
