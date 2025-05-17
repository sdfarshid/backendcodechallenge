from unittest.mock import AsyncMock, patch, MagicMock

import pytest

from app.infrastructure.fetchers.github.github_fetcher import GithubFetcher


@pytest.mark.asyncio
async def test_github_fetcher_fetch_raw_commits():
    token = "fake-token"
    repo = "test_owner/test_repo"
    page = 1
    per_page = 5

    fake_commit_data = [ {
                        "url": "https://api.github.com/repos/octocat/Hello-World/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
                        "sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
                        "node_id": "MDY6Q29tbWl0NmRjYjA5YjViNTc4NzVmMzM0ZjYxYWViZWQ2OTVlMmU0MTkzZGI1ZQ==",
                        "html_url": "https://github.com/octocat/Hello-World/commit/6dcb09b5b57875f334f61aebed695e2e4193db5e",
                        "comments_url": "https://api.github.com/repos/octocat/Hello-World/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e/comments",
                        "commit": {
                          "url": "https://api.github.com/repos/octocat/Hello-World/git/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
                          "author": {
                            "name": "Monalisa Octocat",
                            "email": "support@github.com",
                            "date": "2011-04-14T16:00:49Z"
                          },
                          "committer": {
                            "name": "Monalisa Octocat",
                            "email": "support@github.com",
                            "date": "2011-04-14T16:00:49Z"
                          },
                          "message": "Fix all the bugs",
                          "tree": {
                            "url": "https://api.github.com/repos/octocat/Hello-World/tree/6dcb09b5b57875f334f61aebed695e2e4193db5e",
                            "sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e"
                          },
                          "comment_count": 0,
                          "verification": {
                            "reason": "unsigned",
                          }
                        },
                        "author": {
                          "login": "octocat",
                          "id": 1,
                          "node_id": "MDQ6VXNlcjE=",
                          "avatar_url": "https://github.com/images/error/octocat_happy.gif",
                          "gravatar_id": "",
                          "url": "https://api.github.com/users/octocat",
                          "html_url": "https://github.com/octocat",
                          "followers_url": "https://api.github.com/users/octocat/followers",
                          "following_url": "https://api.github.com/users/octocat/following{/other_user}",
                          "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
                          "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
                          "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
                          "organizations_url": "https://api.github.com/users/octocat/orgs",
                          "repos_url": "https://api.github.com/users/octocat/repos",
                          "events_url": "https://api.github.com/users/octocat/events{/privacy}",
                          "received_events_url": "https://api.github.com/users/octocat/received_events",
                          "type": "User",
                        },
                        "committer": {
                          "login": "octocat",
                          "id": 1,
                          "node_id": "MDQ6VXNlcjE=",
                          "avatar_url": "https://github.com/images/error/octocat_happy.gif",
                          "gravatar_id": "",
                          "url": "https://api.github.com/users/octocat",
                          "html_url": "https://github.com/octocat",
                          "followers_url": "https://api.github.com/users/octocat/followers",
                          "following_url": "https://api.github.com/users/octocat/following{/other_user}",
                          "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
                          "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
                          "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
                          "organizations_url": "https://api.github.com/users/octocat/orgs",
                          "repos_url": "https://api.github.com/users/octocat/repos",
                          "events_url": "https://api.github.com/users/octocat/events{/privacy}",
                          "received_events_url": "https://api.github.com/users/octocat/received_events",
                          "type": "User",
                        },
                        "parents": [
                          {
                            "url": "https://api.github.com/repos/octocat/Hello-World/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
                            "sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e"
                          }
                        ]
                      } ]


    with patch("app.infrastructure.fetchers.github.github_fetcher.Github") as MockGithub, \
         patch("app.infrastructure.fetchers.github.github_fetcher.Auth.Token") as MockToken:

        MockToken.return_value = "mocked-token"

        mock_instance = MagicMock()
        mock_repo = MagicMock()
        mock_commits = MagicMock()
        mock_commit_objs = [MagicMock(raw_data=commit) for commit in fake_commit_data]

        mock_commits.get_page.return_value = mock_commit_objs
        mock_repo.get_commits.return_value = mock_commits
        mock_instance.get_repo.return_value = mock_repo
        MockGithub.return_value = mock_instance

        fetcher = GithubFetcher(token=token, per_page=per_page)

        result = await fetcher.fetch_raw_commits(repo, page)

    assert result == fake_commit_data
    mock_instance.get_repo.assert_called_once_with(repo)
    mock_commits.get_page.assert_called_once_with(page - 1)
