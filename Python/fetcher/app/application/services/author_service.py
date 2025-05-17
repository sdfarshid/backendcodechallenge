from typing import List, Dict


from app.application.commands.crete_author import CreateAuthorCommand
from app.application.queries.get_authors_by_name import GetAuthorsByNamesQuery
from app.application.queries.list_authors import ListAuthorsQuery
from app.domain.aggregates.author import Author


class AuthorService:
    def __init__(self,
                 get_author_by_name_handler,
                 get_list_authors_handler,
                 create_author_handler):
        self.get_author_by_name_handler = get_author_by_name_handler
        self.create_author_handler = create_author_handler
        self.list_handler = get_list_authors_handler

    async def manage_authors(self, all_commits: list) -> Dict:
        unique_author_names = list(set(commit["author"].strip() for commit in all_commits))
        existing_author_map = await self.get_authors_by_names(unique_author_names)
        return await self.create_authors(unique_author_names, existing_author_map)


    async def get_authors_by_names(self, names: List[str]):
        query = GetAuthorsByNamesQuery(unique_author_names=names)
        return await self.get_author_by_name_handler.handle(query)

    async def create_authors(self, names: List[str], existing_author_map: Dict):
        command = CreateAuthorCommand(unique_author_names=names, existing_author_map=existing_author_map)
        return await self.create_author_handler.handle(command)


    async def list_authors(self, query: ListAuthorsQuery) -> List[Author]:
        return await self.list_handler.handle(query)

