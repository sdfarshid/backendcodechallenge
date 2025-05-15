from enum import Enum


class FetcherSource(str, Enum):
    GITHUB = "github"

    @classmethod
    def values(cls) -> list[str]:
        return [status.value for status in cls]


