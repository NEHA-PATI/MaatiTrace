from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base import Base

# =====================================================
# STATE MODEL
# =====================================================


class State(Base):

    __tablename__ = "states"

    # =================================================
    # COLUMNS
    # =================================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )

    code: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )

    # =================================================
    # RELATIONSHIPS
    # =================================================

    districts = relationship(
        "District",
        back_populates="state_rel",
        cascade="all, delete-orphan",
    )
