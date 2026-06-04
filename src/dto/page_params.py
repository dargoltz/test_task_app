from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PageParameters:
    page: int
    limit: int

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit
