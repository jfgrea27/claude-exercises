# Context Management

This exercise doesn't have any feature, but is rather a set of commands that allow you to update your context window in case you run a long Claude Code session.

1. Look up your context window

```txt
❯ /context
  ⎿   Context Usage
     ⛁ ⛁ ⛁ ⛁ ⛁ ⛁ ⛁ ⛁ ⛁ ⛁   claude-opus-4-5-20251101 · 27k/200k tokens (13%)
     ⛀ ⛀ ⛀ ⛁ ⛁ ⛀ ⛶ ⛶ ⛶ ⛶   ⛁ System prompt: 3.0k tokens (1.5%)
     ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶   ⛁ System tools: 17.4k tokens (8.7%)
     ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶   ⛁ Custom agents: 391 tokens (0.2%)
     ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶   ⛁ Memory files: 80 tokens (0.0%)
     ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶   ⛁ Skills: 686 tokens (0.3%)
     ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶   ⛁ Messages: 5.2k tokens (2.6%)
     ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛝ ⛝ ⛝   ⛶ Free space: 128k (64.1%)
     ⛝ ⛝ ⛝ ⛝ ⛝ ⛝ ⛝ ⛝ ⛝ ⛝   ⛝ Autocompact buffer: 45.0k tokens (22.5%)
     ⛝ ⛝ ⛝ ⛝ ⛝ ⛝ ⛝ ⛝ ⛝ ⛝
```

You can see that Claude Code actually helps you determine which part of the code takes a lot of context.

| Component              | Description                                                                                                                                                                  | Local Configuration                                                                                                  |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **System prompt**      | Anthropic's core instructions that define Claude's behavior, capabilities, and constraints. This includes tone guidelines, safety rules, and tool usage instructions.        | Fixed by Anthropic. Cannot be modified.                                                                              |
| **System tools**       | Built-in tool definitions (Bash, Read, Edit, Write, Glob, Grep, etc.) that Claude can use. Each tool's schema and documentation consumes tokens.                             | Core tools are fixed. Add custom tools via MCP servers in `.claude/settings.local.json` or `~/.claude/settings.json` |
| **Custom agents**      | User-defined agents that extend Claude's capabilities with specialized behaviors.                                                                                            | `.claude/agents/*.md`                                                                                                |
| **Memory files**       | Your CLAUDE.md files containing project instructions, coding conventions, and preferences. Loaded hierarchically from user, project, and local levels.                       | `~/.claude/CLAUDE.md` (user), `./CLAUDE.md` (project), `./CLAUDE.local.md` (local). Edit via `/memory` command.      |
| **Skills**             | Slash command definitions and their associated prompts (e.g., /commit, /review-pr). These are loaded based on your configuration.                                            | `.claude/skills/*.md`                                                                                                |
| **Messages**           | The actual conversation history between you and Claude, including your prompts and Claude's responses. This grows as you interact.                                           | Use `/clear` to reset, `/compact` to summarize                                                                       |
| **Free space**         | Available tokens for new messages, tool outputs, and file contents. This is your working room for the current session.                                                       | N/A - determined by other components                                                                                 |
| **Autocompact buffer** | Reserved space that triggers automatic summarization when reached. Once messages + free space fill up to this point, Claude will compact the conversation to free up tokens. | N/A - managed automatically by Claude Code                                                                           |

2. Resume previous context

```sh
❯ /resume
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Resume Session
╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ ⌕ Search…                                                                                                                                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

❯ ▶ What books are available in the books-mcp? You are not allowed read books-mcp/src/db.py directly Can you add them to our books-api? Can you then use the api to list the books? (+5 other sessions)
  3 minutes ago · 12 messages · main
```

3. You want to clear the context

```sh
/clear

/context
❯ /context
  ⎿   Context Usage
     ⛁ ⛁ ⛁ ⛁ ⛁ ⛁ ⛁ ⛁ ⛁ ⛁   claude-opus-4-5-20251101 · 22k/200k tokens (11%)
     ⛀ ⛀ ⛀ ⛀ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶   ⛁ System prompt: 3.0k tokens (1.5%)
     ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶   ⛁ System tools: 17.4k tokens (8.7%)
     ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶   ⛁ Custom agents: 391 tokens (0.2%)
     ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶   ⛁ Memory files: 80 tokens (0.0%)
     ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶   ⛁ Skills: 686 tokens (0.3%)
     ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶   ⛁ Messages: 106 tokens (0.1%)
     ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛝ ⛝ ⛝   ⛶ Free space: 133k (66.7%)
     ⛝ ⛝ ⛝ ⛝ ⛝ ⛝ ⛝ ⛝ ⛝ ⛝   ⛝ Autocompact buffer: 45.0k tokens (22.5%)
     ⛝ ⛝ ⛝ ⛝ ⛝ ⛝ ⛝ ⛝ ⛝ ⛝
```

Note how we have reduced our messages to 0.1%.
The skills, custom agents, system, tools/prompts stll there since ehtye are part of the system
