from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import func

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base import Base

# =====================================================
# FARM MODEL
# =====================================================


class Farm(Base):

    __tablename__ = "farms"

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

    farmer_id: Mapped[int] = mapped_column(
        ForeignKey("farmers.id"),
        nullable=False,
    )

    block_id: Mapped[int] = mapped_column(
        ForeignKey("blocks.id"),
        nullable=False,
    )

    village_id: Mapped[int | None] = mapped_column(
        ForeignKey("villages.id"),
        nullable=True,
    )

    village_name: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    # =================================================
    # BASIC INFO
    # =================================================

    farm_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    total_area_hectares: Mapped[float] = mapped_column(
        Float,
        nullable=True,
    )

    primary_crop: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    irrigation_type: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    soil_type: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    ownership_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="owned",
    )

    # =================================================
    # STATUS
    # =================================================

    registration_status: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="pending",
    )

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

    farmer = relationship(
        "Farmer",
        back_populates="farms",
    )

    village = relationship(
        "Village",
    )

    boundaries = relationship(
        "FarmBoundary",
        back_populates="farm",
        cascade="all, delete-orphan",
    )

    block = relationship(
        "Block",
    )
