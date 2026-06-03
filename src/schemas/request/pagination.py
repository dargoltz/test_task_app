from pydantic import BaseModel, Field, computed_field


class PaginationParameters(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=100, ge=1)

    @computed_field
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit
