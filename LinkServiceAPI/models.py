from database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String
from datetime import datetime

class Slug(Base):
    __tablename__ = 'slugs'
    slug: Mapped[str] = mapped_column(String(10), unique=True, primary_key=True)
    url: Mapped[str] = mapped_column(String(1024), nullable=False, unique=True)
