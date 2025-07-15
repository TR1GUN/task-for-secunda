from typing import List

from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.models._base_model import _BaseModel


class Address(_BaseModel):
    """
    Building address table
    """
    id: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True)
    address_city: Mapped[str]
    address_street: Mapped[str]
    address_number: Mapped[str] = mapped_column(String(), unique=True)

    building: Mapped["Buildings"] = relationship(back_populates="address")
    # organisations: Mapped[List["Company"]] = relationship(back_populates="building")


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


class Buildings(_BaseModel):
    """
    Buildings table
    """
    id: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True)
    # Решил проблему с адресом - Теперь он уникальный
    address_id: Mapped[int] = mapped_column(Integer, ForeignKey(Address.id), unique=True)
    coordinates_id: Mapped[int] = mapped_column(Integer, ForeignKey(ObjectCoordinates.id), unique=True)

    address: Mapped["Address"] = relationship(back_populates="building")
    coordinates: Mapped["ObjectCoordinates"] = relationship(back_populates="building")

    organisations: Mapped[List["Company"]] = relationship(back_populates="building")


# class CompanyActivitiesName(_BaseModel):
#     """
#     Company name table
#     """
#     id: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True)
#     name: Mapped[str]


class CompanyActivities(_BaseModel):
    """
    Company activities table
    """
    id: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True)
    # name_company: Mapped["CompanyActivitiesName"] = relationship(back_populates="id")
    name: Mapped[str]
    organisations: Mapped[List["Company"]] = relationship(back_populates="activities")
    # Решение проблемы вложенности компаний - теперь есть родительский ID деятельности компании.
    # Если это первый уровень, то значение 0.
    parent_activity_id: Mapped[int] = mapped_column(Integer, default=0)


class Company(_BaseModel):
    """
    Companies table
    """
    id: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True)
    name: Mapped[str]
    phone_number: Mapped[str]
    building_id: Mapped[int] = mapped_column(Integer, ForeignKey(Buildings.id))
    activities_id: Mapped[int] = mapped_column(Integer, ForeignKey(CompanyActivities.id))

    building: Mapped['Buildings'] = relationship(back_populates="organisations")
    activities: Mapped['CompanyActivities'] = relationship(back_populates="organisations")

