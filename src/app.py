from __future__ import annotations

import json
from pathlib import Path
from threading import Lock

from fastapi import FastAPI, HTTPException, status

from src.generated.models.models import Book, BookInput, Genre
from src.generated.models.models import Type as ProblemType

app = FastAPI(title="Book Store", version="1.0.0")

# Resolve relative to this file so the server works regardless of the CWD.
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "books.json"
# The OpenAPI contract exposes only a page number, so the page size is fixed.
PAGE_SIZE = 2

# Serialize writes so concurrent requests cannot overwrite each other's changes.
_file_lock = Lock()


def _load_books() -> list[dict]:
    # Treat a missing data file as an empty store rather than crashing.
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def _save_books(books: list[dict]) -> None:
    # Create the data directory on first run, then persist the full collection.
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(books, file, indent=2)
        file.write("\n")


def _problem(
    status_code: int,
    problem_type: ProblemType,
    title: str,
    detail: str,
) -> HTTPException:
    # Keep every error response on the RFC 9457 shape declared in openapi.yaml.
    return HTTPException(
        status_code=status_code,
        detail={
            "type": problem_type.value,
            "title": title,
            "detail": detail,
        },
    )


def _not_found(book_id: int) -> HTTPException:
    return _problem(
        status.HTTP_404_NOT_FOUND,
        ProblemType.resource_not_found,
        "Book not found",
        f"Book with id {book_id} does not exist.",
    )


@app.get("/health")
def health_check() -> dict[str, str]:
    # Public liveness probe; it never touches the data file.
    return {"status": "ok"}


@app.get("/books")
def list_books(genre: str | None = None, page: int = 1) -> dict:
    # Validate manually so invalid input returns the contract's 400, not FastAPI's 422.
    if page < 1:
        raise _problem(
            status.HTTP_400_BAD_REQUEST,
            ProblemType.invalid_request,
            "Invalid page",
            "The page query parameter must be greater than or equal to 1.",
        )

    if genre is not None and genre not in Genre:
        raise _problem(
            status.HTTP_400_BAD_REQUEST,
            ProblemType.invalid_request,
            "Invalid genre",
            f"Unknown genre '{genre}'.",
        )

    # Apply the optional genre filter before paginating; `total` is the
    # number of matching books, not the number on this page.
    books = _load_books()
    if genre is not None:
        books = [book for book in books if book.get("genre") == genre]

    # Convert the 1-based page number into a slice of the filtered collection.
    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    items = [Book(**book) for book in books[start:end]]
    return {"items": items, "total": len(books)}


@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(body: BookInput) -> Book:
    # Hold the lock across the read-modify-write so IDs remain unique.
    with _file_lock:
        books = _load_books()
        # The server owns the id; clients cannot supply or influence it.
        next_id = max((book["id"] for book in books), default=0) + 1
        book = {
            "id": next_id,
            # `mode="json"` turns the Genre enum into a plain string for storage.
            **body.model_dump(mode="json"),
        }
        books.append(book)
        _save_books(books)

    return Book(**book)


@app.get("/books/{book_id}")
def get_book(book_id: int) -> Book:
    # A linear scan is fine for this small file-backed demo store.
    books = _load_books()
    for book in books:
        if book["id"] == book_id:
            return Book(**book)
    raise _not_found(book_id)


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int) -> None:
    # As with creation, lock the whole read-modify-write cycle.
    with _file_lock:
        books = _load_books()
        for index, book in enumerate(books):
            if book["id"] == book_id:
                del books[index]
                _save_books(books)
                return
    raise _not_found(book_id)
