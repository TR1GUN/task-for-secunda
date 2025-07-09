from typing import List

from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.models._base_model import _BaseModel


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


class CompanyName(_BaseModel):
    """
    Company name table
    """
    id: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True)
    name: Mapped[str]


class CompanyActivities(_BaseModel):
    """
    Company activities table
    """
    id: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True)
    name_id: Mapped["CompanyName"] = relationship(back_populates="id")
    organisations: Mapped[List["Company"]] = relationship(back_populates="activities")
    # Решение проблемы вложенности компаний - теперь есть родительский ID деятельности компании.
    # Если это первый уровень, то значение 0.
    parent_activity_id: Mapped[int] = mapped_column(Integer, default=0)



