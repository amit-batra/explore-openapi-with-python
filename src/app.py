from __future__ import annotations

from fastapi import FastAPI, status

from src.generated.models.models import Book, BookInput

app = FastAPI(title="Book Store", version="1.0.0")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/books")
def list_books(genre: str | None = None, page: int = 1) -> dict:
    raise NotImplementedError("list_books not implemented yet")


@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(body: BookInput) -> Book:
    raise NotImplementedError("create_book not implemented yet")


@app.get("/books/{book_id}")
def get_book(book_id: int) -> Book:
    raise NotImplementedError("get_book not implemented yet")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int) -> None:
    raise NotImplementedError("delete_book not implemented yet")
