from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas.handbook import AddressModel, CoordinateModel, BuildingsModel
from database.models import database_models as models


async def add_address(session: AsyncSession, address: AddressModel) -> models.Address:
    address_record = models.Address(
            address_city=address.address_city,
            address_street=address.address_street,
            address_number=address.address_number,
        )
    session.add(address_record)
    await session.commit()
    return address_record


async def add_coordinates(session: AsyncSession, coordinates: CoordinateModel) -> models.ObjectCoordinates:
    coordinates_record = models.ObjectCoordinates(
            coordinate_x=coordinates.coordinate_x,
            coordinate_y=coordinates.coordinate_y
        )
    session.add(coordinates_record)
    await session.commit()
    return coordinates_record


async def added_building(session: AsyncSession, building: BuildingsModel) -> models.Buildings:
    address_record = await add_address(session=session,address=building.address)
    coordinates_record = await add_coordinates(session=session, coordinates=building.coordinates)
    building_record = models.Buildings(
        address=address_record,
        coordinates=coordinates_record
    )
    session.add(building_record)  # добавляем в бд
    await session.commit()
    return building_record


async def get_first_building_by_address(session: AsyncSession, address: AddressModel) -> models.Buildings | None:
    _query = (
        select(models.Buildings).
        join(models.Address, models.Buildings.address_id == models.Address.id).
        where(
        models.Address.address_city == address.address_city,
            models.Address.address_street == address.address_street,
            models.Address.address_number == address.address_number
        )
    )
    result: Result = await session.execute(_query)
    return result.scalars().first()


async def get_first_building_by_address_and_coordinates(session: AsyncSession,
                                                        building: BuildingsModel) -> models.Buildings | None:
    _query = (select(models.Buildings).
    join(models.ObjectCoordinates, models.Buildings.coordinates_id == models.ObjectCoordinates.id).
    join(models.Address, models.Buildings.address_id == models.Address.id).
    where(
        models.Address.address_city == building.address.address_city,
        models.Address.address_street == building.address.address_street,
        models.Address.address_number == building.address.address_number).
    where(
        models.ObjectCoordinates.coordinate_x == building.coordinates.coordinate_x,
        models.ObjectCoordinates.coordinate_y == building.coordinates.coordinate_y,
    )
    )
    result: Result = await session.execute(_query)
    return result.scalars().first()


async def get_or_create_building(session: AsyncSession, building: BuildingsModel) -> models.Buildings:
    # record = await get_first_building_by_address_and_coordinates(session=session, address=building.address)
    # if record:
    #     return record
    # return await added_building(session=session, building=building)
    # вариант #2
    # пыитаемся записать уникальное, и далее ловим ошибку обрабатывая ветку else
    try:
        return await added_building(session=session, building=building)
    except IntegrityError:
        await session.rollback()
        return await get_first_building_by_address_and_coordinates(session=session, building=building)
