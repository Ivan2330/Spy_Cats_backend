from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Numeric
from app.database.db import Base

class Cat(Base):
    __tablename__ = "cats"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    years_experience: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    breed: Mapped[str] = mapped_column(String(120), nullable=False)
    salary: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    # one cat -> one mission
    mission: Mapped["Mission"] = relationship(back_populates="cat", uselist=False, lazy="selectin")
