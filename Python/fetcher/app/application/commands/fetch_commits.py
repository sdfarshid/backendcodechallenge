from pydantic import BaseModel


class FetchCommitsCommand(BaseModel):
    count: int