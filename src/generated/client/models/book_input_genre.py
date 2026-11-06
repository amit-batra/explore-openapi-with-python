from enum import StrEnum


class BookInputGenre(StrEnum):
    FICTION = "fiction"
    NONFICTION = "nonfiction"
    POETRY = "poetry"
    SCI_FI = "sci-fi"

    def __str__(self) -> str:
        return str(self.value)
