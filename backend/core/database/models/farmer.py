from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import func

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base import Base

# =====================================================
# FARMER MODEL
# =====================================================


class Farmer(Base):

    __tablename__ = "farmers"

    # =================================================
    # PRIMARY KEY
    # =================================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # =================================================
    # BASIC INFO
    # =================================================

    full_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    mobile_number: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
        index=True,
    )

    aadhaar_reference: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    farmer_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="individual",
    )

    # =================================================
    # STATUS
    # =================================================

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    # =================================================
    # TIMESTAMPS
    # =================================================

    created_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # =================================================
    # RELATIONSHIPS
    # =================================================

    farms = relationship(
        "Farm",
        back_populates="farmer",
        cascade="all, delete-orphan",
    )
