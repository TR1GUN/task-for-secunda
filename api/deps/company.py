from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas.handbook import AddressModel
from database.database_transactions.company import get_company_by_name as db_get_company_by_name
from database.models import database_models as models
from database.setup_db import DataBase


async def get_company_by_name(name_company: str, session: AsyncSession = Depends(DataBase.scoped_session_dependency)) -> models.Company:
    company = await db_get_company_by_name(session=session, name=name_company)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'There company with name: {name_company}is not exist'
        )
    return company
