from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base import Base

# =====================================================
# BLOCK MODEL
# =====================================================


class Block(Base):

    __tablename__ = "blocks"

    # =================================================
    # COLUMNS
    # =====================================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    district_id: Mapped[int] = mapped_column(
        ForeignKey("districts.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String,
        nullable=True,
        unique=True,
    )

    # =================================================
    # RELATIONSHIPS
    # =====================================================

    district = relationship(
        "District",
        back_populates="blocks",
    )

    villages = relationship(
        "Village",
        back_populates="block",
        cascade="all, delete-orphan",
    )
