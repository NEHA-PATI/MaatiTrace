from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Index

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from geoalchemy2 import Geometry

from core.database.base import Base

# =====================================================
# H3 CELL MODEL
# =====================================================


class H3Cell(Base):

    __tablename__ = "h3_cells"

    # =================================================
    # PRIMARY KEY
    # =================================================

    h3_index: Mapped[str] = mapped_column(
        String,
        primary_key=True,
    )

    # =================================================
    # METADATA
    # =================================================

    resolution: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    # =================================================
    # GEOMETRY
    # =================================================

    geometry = mapped_column(
        Geometry(
            geometry_type="POLYGON",
            srid=4326,
            spatial_index=False,
        ),
        nullable=False,
    )

    geometry_3857 = mapped_column(
        Geometry(
            geometry_type="POLYGON",
            srid=3857,
            spatial_index=False,
        ),
        nullable=True,
    )


Index(
    "idx_h3_cells_geometry",
    H3Cell.geometry,
    postgresql_using="gist",
)

Index(
    "idx_h3_cells_geometry_3857",
    H3Cell.geometry_3857,
    postgresql_using="gist",
)
