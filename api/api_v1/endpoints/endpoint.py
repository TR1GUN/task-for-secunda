from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import database_models as models
from database.setup_db import DataBase
from api.api_v1.schemas.handbook import (
    CompaniesInfoModel,
    ListCompaniesInBuilding,
    ListCompaniesToActivity,
    CompanyActivitiesModel,
    CoordinatesPlaceModel,
    ListCompaniesToPlacesModel,
    CompaniesInfoWithAddressModel, CompanyModel, FullAddressModel, CoordinateModel, ListCompaniesToActivityModel,
    CompaniesToActivityModel, AddressModel
)
from api.deps.building import get_building_by_address
from api.deps.activity import get_company_activities, get_activities_with_companies
from api.deps.company import get_company_by_name

from database.database_transactions import building as transactions_building, company as transactions_company

organisation_route = APIRouter(prefix='/organisation')


@organisation_route.post('/organisation/building', response_model=ListCompaniesInBuilding)
async def get_organisation_in_building(
        building: models.Buildings = Depends(get_building_by_address),
        session: AsyncSession = Depends(DataBase.scoped_session_dependency)
):
    """
    List of all companies located in the building at a given address
    """
    return ListCompaniesInBuilding(
        address=building.address,
        companies=[
            CompaniesInfoModel(name=company.name, phone_number=company.phone_number) for company in
            await transactions_company.get_company_located_in_building(session=session, building=building)
        ]
    )


@organisation_route.get('organisation/type_activity/{activity}')
async def get_all_organisation_for_activity(
        activity: models.CompanyActivities = Depends(get_company_activities),
        session: AsyncSession = Depends(DataBase.scoped_session_dependency), ) -> ListCompaniesToActivity:
    """
    List of all organizations that are related to the specified type of activity
    """

    return ListCompaniesToActivity(
        company_activities=CompanyActivitiesModel(activity_name=activity.name),
        companies=[
            CompaniesInfoModel(name=company.name, phone_number=company.phone_number) for company in
            await transactions_company.get_company_by_type_activity(session=session, activity=activity)
        ]
    )


@organisation_route.post('organisation/place')
async def get_organisation_in_place(points: CoordinatesPlaceModel, session: AsyncSession = Depends(
    DataBase.scoped_session_dependency)) -> ListCompaniesToPlacesModel:
    """
    список организаций, которые находятся в заданном радиусе/прямоугольной области относительно указанной точки на карте. список зданий
    :return:
    """

    return ListCompaniesToPlacesModel(
        coordinates_place=points,
        companies=[CompaniesInfoWithAddressModel(companies) for companies in
                   await transactions_company.get_company_by_coordinates_place(session=session, points=points)]
    )


@organisation_route.get('organisation/info/{idx}')
async def get_organisation_info(
        idx: int, session: AsyncSession = Depends(DataBase.scoped_session_dependency)
) -> CompaniesInfoModel:
    """
    Вывод информации об организации по её идентификатору
    :return:
    """
    record = await transactions_company.get_company_by_id(session=session, idx=idx)
    return CompaniesInfoModel(
        name=record.name,
        phone_number=record.phone_number
    )


@organisation_route.post('organisation/search/activity/{activity}')
async def search_company_by_activity(company_activities: list[models.CompanyActivities] = Depends(get_activities_with_companies))-> ListCompaniesToActivityModel :
    """
    искать организации по виду деятельности.
    Например, поиск по виду деятельности «Еда», которая находится на первом уровне дерева,
    и чтобы нашлись все организации, которые относятся к видам деятельности, лежащим внутри.
    Т.е. в результатах поиска должны отобразиться организации с видом деятельности
     Еда, Мясная продукция, Молочная продукция.

    :return:
    """
    return ListCompaniesToActivityModel(
        companies_activity=[
            CompaniesToActivityModel(
                activity=activity.name,
                companies=[
                    CompaniesInfoWithAddressModel(
                        name=companies_info.name,
                        phone_number=companies_info.phone_number,
                        address=AddressModel(
                            address_city=companies_info.address.address_city,
                            address_street=companies_info.address.address_street,
                            address_number=companies_info.address.address_number,
                        )
                    )
                    for companies_info in activity.organisations]
            )
            for activity in company_activities
        ]
    )


@organisation_route.post('company/search/name/{name_company}')
async def search_company_by_name(company: models.Company = Depends(get_company_by_name)) -> CompanyModel:
    """
    Search company by name
    """
    return CompanyModel(
        name=company.name,
        phone_number=company.phone_number,
        activities=company.activities.name,
        address=FullAddressModel(
            coordinate=CoordinateModel(
                coordinate_x=company.building.coordinates.coordinate_x,
                coordinate_y=company.building.coordinates.coordinate_y
            ),
            address_city=company.building.address.address_city,
            address_street=company.building.address.address_street,
            address_number=company.building.address.address_number
        )
    )

#
# def get_organisation(session: AsyncSession = Depends(DataBase.scoped_session_dependency)):
#     """
#     ограничить уровень вложенности деятельностей 3 уровням
#     :return:
#     """
