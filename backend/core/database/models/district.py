# from sqlalchemy import Integer, String
# from sqlalchemy.orm import Mapped, mapped_column

# from geoalchemy2 import Geometry

# from core.database.base import Base


# class District(Base):

#     __tablename__ = "districts"

#     id: Mapped[int] = mapped_column(
#         Integer,
#         primary_key=True,
#         autoincrement=True,
#     )

#     name: Mapped[str] = mapped_column(
#         String,
#         nullable=False,
#         unique=True,
#     )

#     state: Mapped[str] = mapped_column(
#         String,
#         nullable=False,
#     )

#     geometry = mapped_column(
#         Geometry(
#             geometry_type="MULTIPOLYGON",
#             srid=4326,
#         ),
#         nullable=False,
#     )


from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Index

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from geoalchemy2 import Geometry

from core.database.base import Base

# =====================================================
# DISTRICT MODEL
# =====================================================


class District(Base):

    __tablename__ = "districts"

    # =================================================
    # COLUMNS
    # =================================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    state_id: Mapped[int] = mapped_column(
        ForeignKey("states.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    # TEMPORARY
    # backward compatibility

    code: Mapped[str] = mapped_column(
        String,
        nullable=True,
        unique=True,
    )

    geometry = mapped_column(
        Geometry(
            geometry_type="MULTIPOLYGON",
            srid=4326,
            spatial_index=False,
        ),
        nullable=True,
    )

    # =================================================
    # RELATIONSHIPS
    # =================================================

    state_rel = relationship(
        "State",
        back_populates="districts",
    )

    blocks = relationship(
        "Block",
        back_populates="district",
        cascade="all, delete-orphan",
    )


# =====================================================
# INDEXES
# =====================================================

Index(
    "idx_districts_geometry",
    District.geometry,
    postgresql_using="gist",
)
