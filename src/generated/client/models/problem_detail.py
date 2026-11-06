from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.problem_detail_type import ProblemDetailType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProblemDetail")


@_attrs_define
class ProblemDetail:
    """
    Attributes:
        title (str):
        detail (str):
        type_ (ProblemDetailType | Unset):
    """

    title: str
    detail: str
    type_: ProblemDetailType | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        detail = self.detail

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "detail": detail,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        title = d.pop("title")

        detail = d.pop("detail")

        _type_ = d.pop("type", UNSET)
        type_: ProblemDetailType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = ProblemDetailType(_type_)

        problem_detail = cls(
            title=title,
            detail=detail,
            type_=type_,
        )

        problem_detail.additional_properties = d
        return problem_detail

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
