from typing import List, Dict
from github import Github, Auth, GithubException
import asyncio

from app.utilities.log import commit_logger


class GithubFetcher:

    DEFAULT_PER_PAGE = 100


    def __init__(self, token: str, per_page: int ):
        auth = Auth.Token(token)
        self.github = Github(auth=auth, per_page=per_page)
        self.logger = commit_logger



    async def fetch_raw_commits(self, repo: str, page: int) -> List[Dict]:
        def sync_fetch_raw_commits():
            try:
                gitHub_repository = self.github.get_repo(repo)
                commits = gitHub_repository.get_commits().get_page(page - 1)
                return [commit.raw_data for commit in commits]
            except GithubException as ge:
                self.logger.error(f"GitHub API Error (page {page}): {ge}")
                raise
            except Exception as e:
                self.logger.error(f"Unexpected error while fetching page {page}: {e}")
                raise

        return await asyncio.to_thread(sync_fetch_raw_commits)



