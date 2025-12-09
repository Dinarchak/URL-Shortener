from database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String
from datetime import datetime

class Link(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    short_url: Mapped[str] = mapped_column(String(10), unique=True)
    url: Mapped[str] = mapped_column(String(1024), nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
