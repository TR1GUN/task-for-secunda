# В этом файле мы добавляем нужные нам данные в базу данных

from datetime import datetime, timedelta
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
import pydantic

from api.api_v1.schemas.handbook import CompanyModelWithActivities, BuildingsModel, AddressModel, CoordinateModel, \
    CompanyActivities
from database.database_initialization import DataBase
from database.database_transactions.company import added_company_by_full_model


async def demo(session: AsyncSession):
    company = CompanyModelWithActivities(
        name='Company Name awdad',
        phone_number='phone_number 2',
        building=BuildingsModel(
            address=AddressModel(
                address_city='city',
                address_street='street',
                address_number='2к32'
            ),
            coordinates=CoordinateModel(
                coordinate_x=2233.2323,
                coordinate_y=22.228
            )
        ),
        activities=CompanyActivities(name='Activites LOL', parent_activity_id=0)
    )

    company = await added_company_by_full_model(session=session, company=company)


async def main():
    async with DataBase.session_factory() as session:
        await demo(session=session)


if __name__ == "__main__":
    asyncio.run(main())
