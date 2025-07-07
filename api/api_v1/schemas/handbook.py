import pydantic


class AddressModel(pydantic.BaseModel):
    address_city: str
    address_street: str
    address_number: str


class CompaniesInfoModel(pydantic.BaseModel):
    name: str
    phone_number: str
    # address: Mapped['Buildings']
    # activities: Mapped['CompanyActivities']


class ListCompaniesInBuilding(pydantic.BaseModel):
    address: AddressModel
    companies:list[CompaniesInfoModel]


class CompanyActivitiesModel(pydantic.BaseModel):
    activity_name:str


class ListCompaniesToActivity(pydantic.BaseModel):
    company_activities:CompanyActivitiesModel
    companies: list[CompaniesInfoModel]


class CoordinateModel(pydantic.BaseModel):
    """
    Coordinate Object
    """
    coordinate_x: float
    coordinate_y: float


class CoordinatesPlaceModel(pydantic.BaseModel):
    a1: CoordinateModel
    a2: CoordinateModel
    a3: CoordinateModel
    a4: CoordinateModel


class FullAddressModel(AddressModel):
    coordinate: CoordinateModel


class CompaniesInfoWithAddressModel(pydantic.BaseModel):
    name: str
    phone_number: str
    address: AddressModel


class ListCompaniesToPlacesModel(pydantic.BaseModel):
    coordinates_place: CoordinatesPlaceModel
    companies: list[CompaniesInfoWithAddressModel]


class CompaniesToActivityModel(pydantic.BaseModel):
    activity: str
    companies: list[CompaniesInfoWithAddressModel]


class ListCompaniesToActivityModel(pydantic.BaseModel):
    companies_activity: list[CompaniesToActivityModel]


class CompanyModel(pydantic.BaseModel):
    name: str
    phone_number: str
    address: FullAddressModel
    activities: str

