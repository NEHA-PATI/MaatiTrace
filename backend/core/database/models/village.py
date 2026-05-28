from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base import Base

# =====================================================
# VILLAGE MODEL
# =====================================================


class Village(Base):

    __tablename__ = "villages"

    # =================================================
    # PRIMARY KEY
    # =================================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # =================================================
    # RELATIONS
    # =================================================

    block_id: Mapped[int] = mapped_column(
        ForeignKey("blocks.id"),
        nullable=False,
    )

    # =================================================
    # DATA
    # =================================================

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
    # =================================================

    block = relationship(
        "Block",
        back_populates="villages",
    )

    farms = relationship(
        "Farm",
        back_populates="village",
    )
