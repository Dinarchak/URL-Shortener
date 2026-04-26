from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from datetime import datetime

class RedirectEvent(Base):
    __tablename__ = 'redirect_events'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    time: Mapped[datetime] = mapped_column(nullable=False)
    slug: Mapped[str] = mapped_column(String(10), nullable=False)
    userinfo: Mapped[str] = mapped_column(String(512), nullable=False)


class CreateEvent(Base):
    __tablename__ = 'create_events'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)
    time: Mapped[datetime] = mapped_column(nullable=False)
    slug: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    userinfo: Mapped[str] = mapped_column(String(512), nullable=True)
