from pydantic import BaseModel


class GetAuthorsByNamesQuery(BaseModel):
    unique_author_names: list[str]