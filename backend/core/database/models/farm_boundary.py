from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import Index

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from geoalchemy2 import Geometry

from core.database.base import Base

# =====================================================
# FARM BOUNDARY MODEL
# =====================================================


class FarmBoundary(Base):

    __tablename__ = "farm_boundaries"

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
    )

    # =================================================
    # GEOMETRY
    # =================================================

    boundary = mapped_column(
        Geometry(
            geometry_type="POLYGON",
            srid=4326,
            spatial_index=False,
        ),
        nullable=False,
    )

    # =================================================
    # METADATA
    # =================================================

    boundary_hash: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    area_m2: Mapped[float] = mapped_column(
        Float,
        nullable=True,
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

    farm = relationship(
        "Farm",
        back_populates="boundaries",
    )


# =====================================================
# INDEXES
# =====================================================

Index(
    "idx_farm_boundaries_geometry",
    FarmBoundary.boundary,
    postgresql_using="gist",
)
