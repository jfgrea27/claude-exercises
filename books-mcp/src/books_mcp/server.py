"""MCP Server that provides information about available books."""

from mcp.server.fastmcp import FastMCP

from books_mcp.data import BOOKS

mcp = FastMCP("books")


@mcp.tool()
def get_books() -> list[dict]:
    """Get all available books in the library."""
    return BOOKS


@mcp.tool()
def get_book_by_id(book_id: int) -> dict | None:
    """Get a specific book by its ID.

    Args:
        book_id: The ID of the book to retrieve.

    Returns:
        The book information if found, None otherwise.
    """
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    return None


@mcp.tool()
def search_books(query: str) -> list[dict]:
    """Search for books by title or author.

    Args:
        query: The search term to look for in book titles and authors.

    Returns:
        List of books matching the search query.
    """
    query_lower = query.lower()
    return [
        book
        for book in BOOKS
        if query_lower in book["title"].lower() or query_lower in book["author"].lower()
    ]
