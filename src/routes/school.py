from src.model.school import *
from src.database import *


basic_dt: APIRouter = APIRouter()
by_attr: APIRouter = APIRouter()
views: APIRouter = APIRouter()

some_routes = APIRouter()





@some_routes.delete("/delete/{id}", tags=["delete"])
def delete_by_id(id: int, db: Session = Depends(get_db_school)):
    """
    Delete a record by id
    """
    # db.query(GeneralUser).filter(GeneralUser.id == id).delete()
    # modify it to also delete all the posts associated with the user
    db.query(Student).filter(Student.id == id).delete(synchronize_session=False)
    db.commit()
    return {"message": f"Deleted record with id {id}"}











basic_dt.include_router(some_routes)


for t_type in school_classes:
    dt_route(t_type, basic_dt, get_db_school)
    get_all_attr_route(t_type, by_attr, get_db_school)
    pass


