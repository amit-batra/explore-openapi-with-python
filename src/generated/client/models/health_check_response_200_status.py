from enum import StrEnum


class HealthCheckResponse200Status(StrEnum):
    OK = "ok"

    def __str__(self) -> str:
        return str(self.value)
