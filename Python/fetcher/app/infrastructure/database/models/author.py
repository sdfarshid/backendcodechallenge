from sqlalchemy import Column,String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.infrastructure.database.session import Base




class AuthorModel(Base):
    __tablename__ = "authors"
    id = Column(PG_UUID(as_uuid=True), primary_key=True)
    name = Column(String(255), unique=True, nullable=False, index=True)