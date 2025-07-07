from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas.handbook import AddressModel
from database import models


async def get_first_building_by_address(session: AsyncSession, address: AddressModel) -> models.Buildings | None:
    _query = (select(models.Buildings,
                     models.Address).
        where(
        models.Address.address_city == address.address_city,
        models.Address.address_street == address.address_street,
        models.Address.address_number == address.address_number,
    ))
    result: Result = await session.execute(_query)
    return result.scalars().first()
