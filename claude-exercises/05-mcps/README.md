# MCPs

> **Note:** To replay this exercise, please `git checkout 05-mcps`.

[MCP (Model Context Protocol)](https://modelcontextprotocol.io/) servers allow Claude Code to interact with external tools and data sources. This exercise demonstrates how to create and configure a simple MCP server.

We have created a `books-mcp` server that provides information about available books. The server exposes three tools:
- `get_books` - Get all available books
- `get_book_by_id` - Get a specific book by ID
- `search_books` - Search books by title or author

## Setup

1. Install dependencies (includes the MCP server)

```sh
just install
```

2. Add the MCP server to your Claude Code settings

Open your Claude Code settings file at `.claude/settings.json` and add:

```json
{
  "mcpServers": {
    "books": {
      "command": "mcp",
      "args": ["run", "/path/to/claude-exercises/books-mcp/src/books_mcp/server.py"]
    }
  }
}
```

Replace `/path/to/claude-exercises` with your actual path.

Alternatively, you can add it to the project-level settings at `.claude/settings.json`:

```json
{
  "mcpServers": {
    "books": {
      "command": "mcp",
      "args": ["run", "./books-mcp/src/books_mcp/server.py"]
    }
  }
}
```

3. Restart Claude Code to load the MCP server

```sh
claude
```

You can also test the MCP server directly with:

```sh
just mcp
```

## Usage

Once configured, you can use the MCP tools in your prompts:

1. Open Claude Code

```sh
claude
```

2. Prompt (copy prompt below)

```txt
What books are available in the library?
```

Claude Code output

```txt
Let me check what books are available.

Using mcp__books__get_books tool...

Here are the 5 books available in the library:

1. To Kill a Mockingbird by Harper Lee (1960)
   A novel about racial injustice in the Deep South, seen through the eyes of young Scout Finch.

2. 1984 by George Orwell (1949)
   A dystopian novel set in a totalitarian society under constant surveillance.

3. Pride and Prejudice by Jane Austen (1813)
   A romantic novel following Elizabeth Bennet as she navigates issues of manners, morality, and marriage.

4. The Great Gatsby by F. Scott Fitzgerald (1925)
   A story of wealth, love, and the American Dream in the Jazz Age.

5. One Hundred Years of Solitude by Gabriel Garcia Marquez (1967)
   A multi-generational story of the Buendia family in the fictional town of Macondo.
```

3. You can also search for specific books

```txt
Search for books by Orwell
```

Note:

- MCP servers run as separate processes and communicate with Claude Code via stdio
- You can create more complex MCP servers that connect to databases, APIs, or other services
- MCP tools are discovered automatically and can be used like any other tool in Claude Code
