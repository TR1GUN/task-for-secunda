from typing import Any, Sequence

from sqlalchemy import select, Result, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas.handbook import CoordinatesPlaceModel, CompanyModelWithActivities, CompanyActivities, \
    CompanyModel
from database.database_transactions.activity import get_or_create_company_activities
from database.database_transactions.building import get_or_create_building
from database.models import database_models as models


async def added_company(
        session: AsyncSession,
        company: CompanyModelWithActivities,
        building: models.Buildings,
        activities: CompanyActivities
):
    company_record = models.Company(
        name=company.name,
        phone_number=company.phone_number,
        building=building,
        activities=activities
    )
    session.add(company_record)
    await session.commit()
    return company_record


async def get_company_located_in_building_id(session: AsyncSession, building_id: int) -> Sequence[
    Row[Any] | RowMapping | Any]:
    _query = (
        select(models.Company).
        where(
            models.Company.building_id == building_id
        )
    )
    result: Result = await session.execute(_query)
    return result.scalars().all()


async def get_company_located_in_building(session: AsyncSession, building: models.Buildings) -> Sequence[
    Row[Any] | RowMapping | Any]:
    _query = (
        select(models.Company).
        where(
            models.Company.building == building
        )
    )
    result: Result = await session.execute(_query)
    return result.scalars().all()


async def get_company_by_type_activity_id(session: AsyncSession, activity_id: int) -> Sequence[
    Row[Any] | RowMapping | Any]:
    _query = (
        select(models.Company).
        where(
            models.Company.activities_id == activity_id
        )
    )
    result: Result = await session.execute(_query)
    return result.scalars().all()


async def get_company_by_type_activity_name(session: AsyncSession, activity: str) -> Sequence[
    Row[Any] | RowMapping | Any]:
    _query = (
        select(models.Company).
        join(models.CompanyActivities, models.Company.activities_id == models.CompanyActivities.id).
        where(
            models.Company.activities.name == activity,
        )
    )
    result: Result = await session.execute(_query)
    return result.scalars().all()


async def get_company_by_type_activity(session: AsyncSession, activity: models.CompanyActivities) -> Sequence[
    Row[Any] | RowMapping | Any]:
    _query = (
        select(models.Company).
        join(models.CompanyActivities, models.Company.activities_id == models.CompanyActivities.id).
        where(
            models.Company.activities == activity
        )
    )
    result: Result = await session.execute(_query)
    return result.scalars().all()


async def get_company_by_coordinates_place(session: AsyncSession, points: CoordinatesPlaceModel) -> Sequence[
    Row[Any] | RowMapping | Any]:
    _query = (
        select(models.Company).
        join(models.Buildings, models.Company.building_id == models.Buildings.id).
        join(models.ObjectCoordinates, models.Buildings.coordinates_id == models.ObjectCoordinates.id).
        where(
            (models.ObjectCoordinates.coordinate_x >= points.a1.coordinate_x) &
            (models.ObjectCoordinates.coordinate_x <= points.a2.coordinate_x) &
            (models.ObjectCoordinates.coordinate_y >= points.a2.coordinate_y) &
            (models.ObjectCoordinates.coordinate_y <= points.a4.coordinate_y)
        )
    )
    result: Result = await session.execute(_query)
    return result.scalars().all()


async def get_company_by_id(session: AsyncSession, idx: int):
    _query = (
        select(models.Company).
        where(models.Company.id == idx)
    )
    result: Result = await session.execute(_query)
    return result.scalars().first()


async def get_company_by_name(session: AsyncSession, name: str) -> models.Company | None:
    _query = (
        select(models.Company).
        where(models.Company.name == name)
    )
    result: Result = await session.execute(_query)
    return result.scalars().first()


async def added_company_by_full_model(session: AsyncSession, company: CompanyModelWithActivities):
    # Проверка на сущестование Здания и Адресса
    building = await get_or_create_building(session=session, building=company.building)
    company_activities = await get_or_create_company_activities(session=session, company_activities=company.activities)
    # добавление самой записи
    return added_company(session=session,company=company,building=building,activities=company_activities)
