from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from database import models


async def get_first_company_activities_by_name(session: AsyncSession, name: str) -> models.CompanyActivities| None:
    _query = (select(models.CompanyActivities).
        where(
        models.CompanyActivities.name == name,
    ))
    result: Result = await session.execute(_query)
    return result.scalars().first()

async def get_companys_by_name_activities(session: AsyncSession, name: str):
    _query = (select(models.CompanyActivities).join().
        where(
        models.CompanyActivities.name == name,
    ))
    result: Result = await session.execute(_query)
    return result.scalars().first()
