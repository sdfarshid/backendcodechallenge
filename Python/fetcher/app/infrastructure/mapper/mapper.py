
from app.domain.aggregates.author import Author
from app.domain.entities.commit import Commit
from app.infrastructure.database.models.author import AuthorModel
from app.infrastructure.database.models.commit import CommitModel


class mapper:

    @staticmethod
    def author_db_to_domain_model(author_db : AuthorModel):
        return Author(
            id=author_db.id,
            name=author_db.name,
        )
    @staticmethod
    def author_model_to_db_model(author : Author):
        return AuthorModel(
            id=author.id,
            name=author.name,
        )

    @staticmethod
    def commit_db_to_domain_model(commit_db: CommitModel):
        return Commit(
            id=commit_db.id,
            hash=commit_db.hash,
            author_id=commit_db.author_id,
            created_at = commit_db.created_at
        )
