# Claude Arena

The purpose of this repository is to document various exercises in Claude Code by modifying a simple [Books API](./books-api/) REST server written in Python.

## Exercises

The following exercises are available in the `claude-exercises/` directory:

| Exercise                                                       | Description                                                | Branch                |
| -------------------------------------------------------------- | ---------------------------------------------------------- | --------------------- |
| [00-basic-usage](./claude-exercises/00-basic-usage/)           | Basic prompting with Claude Code                           | `00-basic-usage`      |
| [01-claude-md](./claude-exercises/01-claude-md/)               | Using `CLAUDE.md` for project-specific workflows           | `01-claude-md`        |
| [02-plan-usage](./claude-exercises/02-plan-usage/)             | Using plan mode for larger changes                         | `02-plan-usage`       |
| [03-subagents](./claude-exercises/03-subagents/)               | Creating specialized subagents for task-specific workflows | `03-subagents`        |
| [04-skills](./claude-exercises/04-skills/)                     | Defining agent skills for context-aware assistance         | `04-skills`           |
| [05-mcps](./claude-exercises/05-mcps/)                         | Creating and using MCP servers                             | `05-mcps`             |
| [06-third-party-mcps](./claude-exercises/06-third-party-mcps/) | Using third-party MCPs like Atlassian Rovo for Jira        | `06-third-party-mcps` |

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

## General Claude Code Best Practices

### Prompting Best Practices

- **Be specific**: Instead of "fix the bug," try "fix the login bug where users see a blank screen after entering wrong credentials"
- **Provide context**: Include error messages, stack traces, reproduction steps
- **Let Claude explore first**: Ask Claude to analyze code before making changes
- **Use `ultrathink:`** for complex problems requiring deeper reasoning

### Workflow Best Practices

- **Name sessions**: Use `/rename <name>` for descriptive names, resume with `claude --resume name`
- **Use Plan Mode** (`Shift+Tab`) for safe exploration before committing to changes
- **Leverage subagents** for verbose output (tests, logs) to keep main context clean
- **Use git worktrees** for parallel development on multiple features
- **Keyboard shortcuts**: `?` for help, `Tab` for completion, `Ctrl+O` for verbose mode

### Configuration Best Practices

- **Organize settings by scope**: User (`~/.claude/settings.json`), Project (`.claude/settings.json`), Local (`.claude/settings.local.json`)
- **Use CLAUDE.md effectively**: Document build commands, code style, architecture patterns
- **Modular rules**: Use `.claude/rules/` for topic-specific instructions
- **Configure permissions strategically**: Use allowlist for safe operations, denylist for risky ones

### Performance Tips

- **Manage token usage**: Use subagents for high-volume operations
- **Monitor costs**: Use `/cost` command
- **Use file references strategically**: `@file.js` only when needed
- **Use Glob/Grep tools** for efficient file searching

### Security Best Practices

- **Review before approval**: Never approve commands blindly
- **Protect sensitive files**: Use permission deny rules for `.env`, secrets
- **Enable sandboxing**: `/sandbox` for filesystem/network isolation
- **Avoid piping untrusted content** directly to Claude

### Common Patterns

- **Understanding codebases**: Start with "give me an overview" then drill down
- **Fixing bugs**: Share error + context, get recommendations, apply + verify
- **Refactoring**: Identify issues, get suggestions, apply in small increments, test
- **Git operations**: Ask conversationally ("commit my changes", "create a pr")

### Essential Commands

| Command           | Purpose                      |
| ----------------- | ---------------------------- |
| `claude -c`       | Continue recent conversation |
| `claude --resume` | Resume specific session      |
| `/agents`         | View/create subagents        |
| `/permissions`    | Review permissions           |
| `/cost`           | Check token usage            |
| `/rewind`         | Go back to previous state    |
