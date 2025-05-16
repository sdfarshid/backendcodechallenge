from app.config.config import get_settings


def get_github_token() -> str:
    token = get_settings().GITHUB_TOKEN
    if not token or not isinstance(token, str):
        raise ValueError("GITHUB_TOKEN is not set or invalid")
    return token

def get_github_repo() -> str:
    return get_settings().GITHUB_REPO
