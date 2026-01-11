# Claude Arena

The purpose of this repository is to document various workloads in Claude Code by changing a simple [Books API](./books_api/) REST server written in `Python`.

The file structure is as follows:

```
./books_api
    ./books_api       # include the source code for the app.
    ./test            # include the tests for the app.
./claude-workloads # includes the workloads (exercises) that you can follow.
```

## Setup

```bash
direnv allow
just install
```
