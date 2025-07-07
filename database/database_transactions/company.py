from typing import Any, Sequence

from sqlalchemy import select, Result, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas.handbook import CoordinatesPlaceModel
from database import models


async def get_company_located_in_building_id(session: AsyncSession, building_id: int) -> Sequence[
    Row[Any] | RowMapping | Any]:
    _query = (select(models.Company).
    where(
        models.Company.building == building_id,
    ))
    result: Result = await session.execute(_query)

    return result.scalars().all()


async def get_company_located_in_building(session: AsyncSession, building: models.Buildings) -> Sequence[
    Row[Any] | RowMapping | Any]:
    _query = (select(models.Company).
    where(
        models.Company.building == building,
    ))
    result: Result = await session.execute(_query)

    return result.scalars().all()


async def get_company_by_type_activity_id(session: AsyncSession, activity_id: int) -> Sequence[
    Row[Any] | RowMapping | Any]:
    _query = (select(models.Company).
    where(
        models.Company.activities == activity_id,
    ))
    result: Result = await session.execute(_query)
    return result.scalars().all()


async def get_company_by_type_activity_name(session: AsyncSession, activity: str) -> Sequence[
    Row[Any] | RowMapping | Any]:
    _query = (select(models.Company).
    where(
        models.Company.activities.name == activity,
    ))
    result: Result = await session.execute(_query)
    return result.scalars().all()


async def get_company_by_type_activity(session: AsyncSession, activity: models.CompanyActivities) -> Sequence[
    Row[Any] | RowMapping | Any]:
    _query = (select(models.Company).
    where(
        models.Company.activities == activity,
    ))
    result: Result = await session.execute(_query)
    return result.scalars().all()


async def get_company_by_coordinates_place(session: AsyncSession, points: CoordinatesPlaceModel) -> Sequence[
    Row[Any] | RowMapping | Any]:
    _query = (select(models.Company).join(
        models.Buildings,
    ).
    where(
        models.ObjectCoordinates.coordinate_x.C == activity,
    ))
    result: Result = await session.execute(_query)
    return result.scalars().all()


async def get_company_by_id(session: AsyncSession, idx: int):
    pass


async def get_company_by_name(session: AsyncSession, name: str) -> models.Company | None:
    _query = (
        select(models.Company).
        where(models.Company.name == name)
    )
    result: Result = await session.execute(_query)
    return result.scalars().first()
