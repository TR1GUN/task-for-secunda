from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas.handbook import AddressModel
from database.database_transactions.building import get_first_building_by_address
from database.models import database_models as models
from database.setup_db import DataBase


async def get_building_by_address(address: AddressModel, session: AsyncSession = Depends(DataBase.scoped_session_dependency)) -> models.Buildings:
    building = await get_first_building_by_address(session=session, address=address)
    if not building:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'There is no building with this address:'
                   f'{address.address_city},{address.address_street},{address.address_number}'
        )
    return building


async def get_building_id(address: AddressModel, session: AsyncSession = Depends(DataBase.scoped_session_dependency)) -> int:
    building_record = await get_building_by_address(session=session, address=address)
    return building_record.id
