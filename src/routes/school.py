from fastapi import APIRouter

from src.model.school import *
from src.database import *


basic_dt: APIRouter = APIRouter()
by_attr: APIRouter = APIRouter()
views: APIRouter = APIRouter()

for t_type in [
    School,
    Program,
    Student,
    Instructor,
    Subject,
    AcademicPeriod,
    ClassGroup,
    StudentEnrollment,
    ExamType,
    Grades,
    Attendance,
    ClassSchedule
    ]:
    dt_route(t_type, basic_dt, get_db_school, CRUDBase(t_type))
    all_attr_route(t_type, by_attr, get_db_school)
