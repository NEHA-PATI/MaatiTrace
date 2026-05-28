from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import Index

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base import Base

# =====================================================
# FARM H3 CELL MODEL
# =====================================================


class FarmH3Cell(Base):

    __tablename__ = "farm_h3_cells"

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

    farm_id: Mapped[int] = mapped_column(
        ForeignKey("farms.id"),
        nullable=False,
        index=True,
    )

    h3_index: Mapped[str] = mapped_column(
        nullable=False,
        index=True,
    )

    # =================================================
    # SPATIAL METADATA
    # =================================================

    resolution: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    coverage_ratio: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # =================================================
    # TIMESTAMPS
    # =================================================

    created_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # =================================================
    # RELATIONSHIPS
    # =================================================

    farm = relationship(
        "Farm",
    )


# =====================================================
# INDEXES
# =====================================================

Index(
    "idx_farm_h3_farm_resolution",
    FarmH3Cell.farm_id,
    FarmH3Cell.resolution,
)

Index(
    "idx_farm_h3_h3_resolution",
    FarmH3Cell.h3_index,
    FarmH3Cell.resolution,
)
