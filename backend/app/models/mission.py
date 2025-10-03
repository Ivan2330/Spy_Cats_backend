from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Boolean, Integer
from app.database.db import Base

class Mission(Base):
    __tablename__ = "missions"

    id: Mapped[int] = mapped_column(primary_key=True)
    cat_id: Mapped[int | None] = mapped_column(ForeignKey("cats.id", ondelete="SET NULL"), nullable=True)
    complete: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    cat: Mapped["Cat"] = relationship(back_populates="mission", lazy="selectin")
    targets: Mapped[list["Target"]] = relationship(
        back_populates="mission",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
