from collections import defaultdict
from typing import Dict

from sqlalchemy.exc import DatabaseError

from app.application.commands.store_commits import StoreCommitsCommand
from app.application.queries.list_commits import ListCommitsQuery
from app.domain.entities.commit import Commit


class CommitService:

    def __init__(self,
                 store_commits_handler,
                 list_commits_handler,
                 logger
                 ):
        self.store_commits_handler = store_commits_handler
        self.list_commits_handler = list_commits_handler
        self.logger = logger


    async def process_and_store_commits(self, all_commits, all_existing_author_map):
        try:
            grouped_commits =  self.group_commits_by_author(all_commits, all_existing_author_map)
            result = await self.store_commits(grouped_commits)
            self.logger.info("Successfully stored commits")
            return result

        except DatabaseError as db_err:
            self.logger.error(f"Database error in store_commits: {db_err}")
            raise
        except Exception as e:
            self.logger.error(f"during manage_commits: {e}")
            raise



    def group_commits_by_author(self, all_commits: list, author_map: Dict) -> Dict:

        try:
            grouped_commits = defaultdict(list)
            for commit in all_commits:
                author_name = commit["author"].strip()
                author_id = author_map.get(author_name)
                if author_id:
                    grouped_commits[author_id].append(commit)
                else:
                    self.logger.warning(f"Unknown author: {author_name}")
            return grouped_commits

        except Exception as e:
            self.logger.error(f"group_commits_by_author have error : {e}")
            raise


    async def store_commits(self, grouped_commits):
        try:
            store_command = StoreCommitsCommand(grouped_commits=grouped_commits)
            return await self.store_commits_handler.handle(store_command)
        except Exception as e:
            self.logger.error(f"store_commits  have error : {e}")
            raise



    async def get_commit(self, query: ListCommitsQuery) -> list[Commit]:

        try:
          return  await self.list_commits_handler.handle(query)

        except Exception as e:
            self.logger.error(f"group_commits_by_author have error : {e}")
            raise
