from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.database_transactions.activity import get_first_company_activities_by_name, \
    get_companys_by_name_activities
from database import models


async def get_company_activities(session: AsyncSession, activity: str) -> models.CompanyActivities:
    company_activities = await get_first_company_activities_by_name(session=session, name=activity)
    if not company_activities:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'this company activity: {activity} does not exist'
        )
    return company_activities


async def get_activities_with_companies(session: AsyncSession, activity: str) -> list[models.CompanyActivities]:
    company_activities = await get_companys_by_name_activities(session=session, activity_name=activity)
    if not company_activities:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'this company activity: {activity} does not exist'
        )
    return company_activities
