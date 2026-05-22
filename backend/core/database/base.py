from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from core.database.models.district import District
