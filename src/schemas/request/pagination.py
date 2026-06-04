from pydantic import BaseModel, Field


class PaginationQueryParameters(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=100, ge=1)
