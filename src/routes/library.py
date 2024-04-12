from fastapi import APIRouter

from src.model.library import *
from src.database import *


basic_dt: APIRouter = APIRouter()
by_attr: APIRouter = APIRouter()
views: APIRouter = APIRouter()


for t_type in [
    Author,
    Library,
    Publisher,
    Topic,
    Book,
    BookAuthor,
    BookTopic,
    BookLibrary,
    AcademicMember,
    Loan
    ]:
    dt_route(t_type, basic_dt, get_db_library, CRUDBase(t_type))
    all_attr_route(t_type, by_attr, get_db_library)
