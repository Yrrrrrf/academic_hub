from src.model.general import *
from src.database import *


basic_dt: APIRouter = APIRouter()
by_attr: APIRouter = APIRouter()
views: APIRouter = APIRouter()


for t_type in general_classes:
    # * post (create)

    # * get (read)
    dt_route(t_type, basic_dt, get_db_school)
    get_all_attr_route(t_type, by_attr, get_db_school)

    # * put (update)

    # * delete (delete)



