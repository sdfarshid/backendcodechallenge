from typing import List, Dict
from github import Github, Auth
import asyncio

class GithubFetcher:

    def __init__(self, token: str, per_page: int=100 ):
        auth = Auth.Token(token)
        self.github = Github(auth=auth, per_page=per_page)


    async def fetch_raw_commits(self, repo: str, page: int) -> List[Dict]:

        def sync_fetch_raw_commits():
            gitHub_repository = self.github.get_repo(repo)
            commits = gitHub_repository.get_commits().get_page(page - 1)
            return [commit.raw_data for commit in commits ]

        return await asyncio.to_thread(sync_fetch_raw_commits)