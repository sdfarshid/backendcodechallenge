from typing import List, Dict
from app.utilities.helper import call_api


class GithubFetcher:
    async def fetch_raw_commits(self, token: str, repo: str, per_page: int, page: int) -> List[Dict]:
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }
        endpoint = f"https://api.github.com/repos/{repo}/commits"
        params = {"per_page": per_page, "page": page}
        return await call_api("GET", endpoint, params=params, headers=headers)