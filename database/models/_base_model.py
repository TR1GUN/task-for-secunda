from sqlalchemy.orm import DeclarativeBase, declared_attr


class _BaseModel(DeclarativeBase):
    """
    Base model class, that creates connection with DataBase
    """
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
