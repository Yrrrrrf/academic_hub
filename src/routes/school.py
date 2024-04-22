from src.model.school import *
from src.database import *


basic_dt: APIRouter = APIRouter()
by_attr: APIRouter = APIRouter()
views: APIRouter = APIRouter()

some_routes = APIRouter()


basic_dt.include_router(some_routes)


for t_type in school_classes:
    pass

    dt_route(t_type, basic_dt, get_db_school)

    # * CRUD

    # * Create Read(get) Update Delete
    # & create is on testing phase (not yet working)
    create_all_attr_route(t_type, by_attr, get_db_school)

    # #  * get is already done!
    get_all_attr_route(t_type, by_attr, get_db_school)

    # ^ update still has some issues...
    update_all_attr_route(t_type, basic_dt, get_db_school)

    # * delete is already done!
    delete_all_attr_route(t_type, by_attr, get_db_school)
