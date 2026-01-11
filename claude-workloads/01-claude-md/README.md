# Claude md - the basics

> **Note:** To replay this exercise, please `git checkout 01-claude-md`.

Claude Code can automatically pull the repository context including tools it can use, core files, etc. by reading the contents of a `CLAUDE.md` file, as described in [claude-code-best-practices](https://www.anthropic.com/engineering/claude-code-best-practices).

In our previous [00-basic-usage](../00-basic-usage/README.md), Claude Code did not run the linting and typing checks. Let's create a `Claude.md` file so that it can carry out specific workflows when updating code

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
 I'll find the books_api code and add the logging you requested.
...
Let me read the key files to understand the structure.
...
Done. I've added logging to the books_api:

  Info logging for requests (routes.py):
  - All endpoints now log "request started" at the beginning
  - All endpoints log "request completed" at the end (including "not found" cases)

  Debug logging for DB interactions (db/books.py):
  - get_all_books: logs query start and number of books retrieved
  - get_book_by_id: logs query and whether book was found
  - create_book: logs the data being created and the resulting book id
  - update_book: logs the book id and update data
  - delete_book: logs deletion attempts, successes, and failures

  Both files use the existing books_api logger. To see debug logs, you can pass logging.DEBUG to setup_logging() in server.py.
```

This completes the feature request as expected.

Annoyingly, the formatting is off and it didn't run any tests. So even though it did add the logging, we still need to manually check it passed the tests, etc. Could we improve this? Check out the next workload for answers :->.
