from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from data import Base  


class Station(Base):
    __tablename__ = "stations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128))
    ville: Mapped[str] = mapped_column(String(128))
    status: Mapped[str] = mapped_column(String(32), default="open")