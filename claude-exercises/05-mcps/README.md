# MCPs

> **Note:** To replay this exercise, please `git checkout 05-mcps`.

[MCP (Model Context Protocol)](https://modelcontextprotocol.io/) servers allow Claude Code to interact with external tools and data sources. This exercise demonstrates how to create and configure a simple MCP server using HTTP/SSE transport.

We have created a `books-mcp` server that provides information about available books. The server exposes three tools:

- `get_books` - Get all available books
- `get_book_by_id` - Get a specific book by ID
- `search_books` - Search books by title or author

For the context of this exercise, we will simulate a real world example of usage of an MCP that holds context that we want to add to our Claude Code session. We want to add books to the db and these are available in the MCP. The feature is to use the resources in the MCP and the context of the server and add these to the db.

## Setup

1. Start the MCP server using HTTP/SSE transport:

```sh
just mcp
```

This will start the MCP server on `http://localhost:8080/sse`.

2. The MCP is configured in [.mcp.json](../../.mcp.json) to connect via SSE:

```json
{
  "mcpServers": {
    "books": {
      "type": "sse",
      "url": "http://localhost:8080/sse"
    }
  }
}
```

3. Start the MCP in a terminal

```
just mcp
```

4. (Re)Start Claude Code in a separate terminal to load the MCP server:

```sh
claude
```

5. To check that the mcp is connected, you can run `/mcp` in your Claude Code session. Here is the output

```
 Manage MCP servers
 1 server

   Project MCPs (.../claude-exercises/.mcp.json)
 ❯ books · ✔ connected

 https://code.claude.com/docs/en/mcp for help

 ↑↓ to navigate · Enter to confirm · escape to cancel
```

5. Claude Code prompt

```txt
What books are available in the books-mcp?
You are not allowed read books-mcp/src/db.py directly
Can you add them to our books-api?
Can you then use the api to list the books?
You can assume that the books-api is running on localhost:8000
```

Claude Code output

```txt
I'll help you with this. Let me first load the MCP tools to get the books, then add them to the books-api.
...
MCPSearch(Search MCP tools: "select:mcp__books__get_books")
...
I found 5 books in the books-mcp:
  ┌───────────────────────────────┬────────────────────────┬──────┐
  │             Title             │         Author         │ Year │
  ├───────────────────────────────┼────────────────────────┼──────┤
  │ To Kill a Mockingbird         │ Harper Lee             │ 1960 │
  ├───────────────────────────────┼────────────────────────┼──────┤
  │ 1984                          │ George Orwell          │ 1949 │
  ├───────────────────────────────┼────────────────────────┼──────┤
  │ Pride and Prejudice           │ Jane Austen            │ 1813 │
  ├───────────────────────────────┼────────────────────────┼──────┤
  │ The Great Gatsby              │ F. Scott Fitzgerald    │ 1925 │
  ├───────────────────────────────┼────────────────────────┼──────┤
  │ One Hundred Years of Solitude │ Gabriel Garcia Marquez │ 1967 │
  └───────────────────────────────┴────────────────────────┴──────┘
...
Now let me explore the books-api to understand how to add these books.
...
Now let me add all the books from the MCP to the API.
...
Bash(curl -s http://localhost:8000/books | python3 -m json.tool)
...
Done. I:

  1. Queried the books-mcp using the MCP tool and found 5 books
  2. Added all 5 books to the books-api via POST requests to http://localhost:8000/books
  3. Listed the books from the API - all 5 books are now available with IDs 1-5

  The books-api now contains all the books from the MCP: To Kill a Mockingbird, 1984, Pride and Prejudice, The Great Gatsby, and One Hundred Years of Solitude.
```

Note:

- MCP tools are discovered automatically and can be used like any other tool in Claude Code
- MCPs can provide context to Claude Code. They can also provide a standard and discoverable way to perform actions (e.g. create Jira tickets using [Atlassian MCP](https://www.atlassian.com/platform/remote-mcp-server)).
