from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.book_input_genre import BookInputGenre
from ..types import UNSET, Unset

T = TypeVar("T", bound="BookInput")


@_attrs_define
class BookInput:
    """
    Attributes:
        title (str):
        genre (BookInputGenre | Unset):
        author (str | Unset):
    """

    title: str
    genre: BookInputGenre | Unset = UNSET
    author: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        genre: str | Unset = UNSET
        if not isinstance(self.genre, Unset):
            genre = self.genre.value

        author = self.author

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
            }
        )
        if genre is not UNSET:
            field_dict["genre"] = genre
        if author is not UNSET:
            field_dict["author"] = author

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        title = d.pop("title")

        _genre = d.pop("genre", UNSET)
        genre: BookInputGenre | Unset
        if isinstance(_genre, Unset):
            genre = UNSET
        else:
            genre = BookInputGenre(_genre)

        author = d.pop("author", UNSET)

        book_input = cls(
            title=title,
            genre=genre,
            author=author,
        )

        book_input.additional_properties = d
        return book_input

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
