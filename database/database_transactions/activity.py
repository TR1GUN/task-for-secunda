from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas.handbook import CompanyActivities
from database.models import database_models as models


async def added_company_activities(
        session: AsyncSession,
        company_activities: CompanyActivities
) -> models.CompanyActivities:
    company_activities_record = models.CompanyActivities(
        name=company_activities.name,
        parent_activity_id=company_activities.parent_activity_id
    )
    session.add(company_activities_record)
    await session.commit()
    return company_activities_record


async def get_first_company_activities_by_name(session: AsyncSession, name: str) -> models.CompanyActivities | None:
    _query = (
        select(models.CompanyActivities).
        where(models.CompanyActivities.name == name)
    )
    result: Result = await session.execute(_query)
    return result.scalars().first()


async def get_company_by_name_activities(session: AsyncSession, name: str):
    _query = (
        select(models.CompanyActivities).
        where(models.CompanyActivities.name == name)
    )
    result: Result = await session.execute(_query)
    return result.scalars().first()


async def get_company_activities_by_id(session: AsyncSession, company_activities_id: int) -> models.CompanyActivities:
    _query = (
        select(models.CompanyActivities).
        where(
            models.CompanyActivities.id == company_activities_id
        )
    )
    result: Result = await session.execute(_query)
    return result.scalars().first()


async def get_first_company_activities(session: AsyncSession,
                                       company_activities: CompanyActivities) -> models.CompanyActivities | None:
    _query = (
        select(models.CompanyActivities).
        where(
            models.CompanyActivities.name == company_activities.name,
            models.CompanyActivities.parent_activity_id == company_activities.parent_activity_id)
        )
    result: Result = await session.execute(_query)
    return result.scalars().first()


async def get_or_create_company_activities(
        session: AsyncSession,
        company_activities: CompanyActivities
) -> models.CompanyActivities:
    if await get_company_activities_by_id(session=session, company_activities_id=company_activities.parent_activity_id):
        try:
            return await added_company_activities(session=session, company_activities=company_activities)
        except IntegrityError:
            await session.rollback()
            return await get_first_company_activities(session=session, company_activities=company_activities)