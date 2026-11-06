from __future__ import annotations

import json
import os
from typing import Any

from src.generated.client.api.books import (
    create_book,
    delete_book,
    get_book,
    list_books,
)
from src.generated.client.api.default import health_check
from src.generated.client.client import AuthenticatedClient
from src.generated.client.models import BookInput, BookInputGenre
from src.generated.client.types import Response


def _print_response(label: str, response: Response[Any]) -> None:
    # `sync_detailed` exposes the status code and parsed model for each call.
    print(f"\n{label} -> {response.status_code.value} {response.status_code.phrase}")
    # A 204 response has no body, so there is nothing to parse or display.
    if not response.content:
        print("<no content>")
        return

    parsed = response.parsed
    if parsed is None:
        print("<no parsed response>")
    elif hasattr(parsed, "to_dict"):
        # Generated models expose `to_dict`, which also turns enums into strings.
        print(json.dumps(parsed.to_dict(), indent=2))
    else:
        print(parsed)


def main() -> None:
    # Allow pointing the same demo at another server or token without edits.
    base_url = os.environ.get("BOOK_STORE_URL", "http://127.0.0.1:8000")
    token = os.environ.get("BOOK_STORE_TOKEN", "demo-token")

    # The context manager closes the underlying httpx client on exit.
    with AuthenticatedClient(base_url=base_url, token=token) as client:
        # Read-only endpoints first.
        _print_response(
            "GET /health",
            health_check.sync_detailed(client=client),
        )
        _print_response(
            "GET /books?page=1",
            list_books.sync_detailed(client=client, page=1),
        )

        # Create a book so the following calls have a known id to work with.
        created = create_book.sync_detailed(
            client=client,
            body=BookInput(
                title="The Left Hand of Darkness",
                genre=BookInputGenre.SCI_FI,
                author="Ursula K. Le Guin",
            ),
        )
        _print_response("POST /books", created)

        # If creation failed, `parsed` is a ProblemDetail (or None) without an id.
        book_id = getattr(created.parsed, "id", None)
        if book_id is None:
            print("\nCreate failed; skipping GET and DELETE.")
            return

        # Remove the book again so the demo leaves the data file unchanged.
        _print_response(
            f"GET /books/{book_id}",
            get_book.sync_detailed(book_id, client=client),
        )
        _print_response(
            f"DELETE /books/{book_id}",
            delete_book.sync_detailed(book_id, client=client),
        )


if __name__ == "__main__":
    main()
