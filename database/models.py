from typing import List

from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column, Mapped, relationship


class _BaseModel(DeclarativeBase):
    """
    Base model class, that creates connection with DataBase
    """
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Company(_BaseModel):
    """
    Организации
    """
    id: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True)
    name: Mapped[str]
    phone_number: Mapped[str]
    building: Mapped['Buildings'] = relationship(back_populates="organisations")
    activities: Mapped['CompanyActivities'] = relationship(back_populates="organisations")


class Buildings(_BaseModel):
    """
    Здание
    """
    id: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True)
    address: Mapped["Address"] = relationship(back_populates="building")
    coordinates: Mapped["ObjectCoordinates"] = relationship(back_populates="building")
    organisations: Mapped[List["Company"]] = relationship(back_populates="building")


class Address(_BaseModel):
    """
    Адресс
    """
    id: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True)
    address_city: Mapped[str]
    address_street: Mapped[str]
    address_number: Mapped[str] = Column(String(), unique=True)
    building: Mapped[str] = relationship(back_populates="address")


class ObjectCoordinates(_BaseModel):
    """
    Coordinates model table
    - Coordinate х
    - Coordinate у
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    coordinate_x: Mapped[float]
    coordinate_y: Mapped[float]
    building: Mapped["Buildings"] = relationship(back_populates="coordinates")


class CompanyActivities(_BaseModel):
    """
    Деятельность компании
    """
    id: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True)
    name: Mapped[str]
    organisations: Mapped[List["Company"]] = relationship(back_populates="activities")
