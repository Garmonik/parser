from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ParseUrl:
    url: str


@dataclass(frozen=True, slots=True)
class DataUrls:
    urls: list[str]
