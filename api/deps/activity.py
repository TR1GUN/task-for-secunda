from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.database_transactions.activity import get_first_company_activities_by_name, \
    get_companys_by_name_activities

from database.models import database_models as models
from database.setup_db import DataBase


async def get_company_activities(activity: str, session: AsyncSession = Depends(DataBase.scoped_session_dependency)) -> models.CompanyActivities:
    company_activities = await get_first_company_activities_by_name(session=session, name=activity)
    if not company_activities:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'this company activity: {activity} does not exist'
        )
    return company_activities


async def get_activities_with_companies(activity: str, session: AsyncSession = Depends(DataBase.scoped_session_dependency)) -> list[models.CompanyActivities]:
    company_activities = await get_companys_by_name_activities(session=session, activity_name=activity)
    if not company_activities:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'this company activity: {activity} does not exist'
        )
    return company_activities
