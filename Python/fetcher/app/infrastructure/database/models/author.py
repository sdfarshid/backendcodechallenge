from sqlalchemy import Column, Integer, String

from app.infrastructure.database.session import Base


class AuthorModel(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False, index=True)