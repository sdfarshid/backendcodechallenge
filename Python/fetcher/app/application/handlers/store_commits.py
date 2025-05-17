from fastapi import Depends

from app.application.commands.store_commits import StoreCommitsCommand
from app.domain.entities.commit import Commit
from app.domain.interface.Icommit_repository import ICommitRepository
from app.infrastructure.repositories.commit_repository import CommitRepository
from app.utilities.log import commit_logger


class StoreCommitsCommandHandler:

    def __init__(self, commit_repository: ICommitRepository = Depends(CommitRepository)):
        self.commit_repository = commit_repository
        self.logger = commit_logger

    async def handle(self, command: StoreCommitsCommand) -> int:
        seen_hashes = set()
        commits_to_store = []

        for author_id, commits in command.grouped_commits.items():
            for commit in commits:
                if commit["hash"] not in seen_hashes:
                    seen_hashes.add(commit["hash"])
                    commits_to_store.append(
                        Commit(
                            hash=commit["hash"],
                            author_id=author_id
                        )
                    )

        try:
          return  await self.commit_repository.add_commits_batch(commits_to_store)
        except Exception as e:
            self.logger.error(f"Failed to store  StoreCommitsCommandHandler : {e}")
            raise RuntimeError(f"Failed to store commits: {e}")

