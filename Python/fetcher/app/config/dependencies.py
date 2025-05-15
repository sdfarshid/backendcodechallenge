from app.config.config import settings


def get_github_token() -> str:
    return settings.GITHUB_TOKEN


def get_github_repo() -> str:
    return settings.GITHUB_REPO
