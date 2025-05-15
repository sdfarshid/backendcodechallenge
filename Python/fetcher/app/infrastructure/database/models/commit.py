from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.infrastructure.database.session import Base


class CommitModel(Base):
    __tablename__ = "commits"
    id = Column(Integer, primary_key=True)
    hash = Column(String, unique=True, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    author = relationship("AuthorModel", backref="commits")