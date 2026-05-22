from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from geoalchemy2 import Geometry

from core.database.base import Base


class District(Base):

    __tablename__ = "districts"

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

    state: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    geometry = mapped_column(
        Geometry(
            geometry_type="MULTIPOLYGON",
            srid=4326,
        ),
        nullable=False,
    )
