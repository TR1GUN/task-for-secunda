from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas.handbook import AddressModel
from database.database_transactions.company import get_company_by_name as db_get_company_by_name
from database import models


async def get_company_by_name(session: AsyncSession, name_company: str) -> models.Company:
    company = await db_get_company_by_name(session=session, name=name_company)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'There company with name: {name_company}is not exist'
        )
    return company
