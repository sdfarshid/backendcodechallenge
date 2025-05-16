from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


from app.infrastructure.database.session import Base


class CommitModel(Base):
    __tablename__ = "commits"
    id = Column(PG_UUID(as_uuid=True), primary_key=True)
    hash = Column(String, unique=True, nullable=False)
    author_id = Column(PG_UUID(as_uuid=True), ForeignKey("authors.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now)

    author = relationship("AuthorModel", backref="commits")