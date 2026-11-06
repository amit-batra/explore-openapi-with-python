from enum import StrEnum


class ProblemDetailType(StrEnum):
    INVALID_REQUEST = "invalid_request"
    RESOURCE_NOT_FOUND = "resource_not_found"

    def __str__(self) -> str:
        return str(self.value)
