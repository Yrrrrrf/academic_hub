# 3rd party imports
from fastapi import Depends, HTTPException, APIRouter

# stdlib imports
from typing import List, Type, Callable
from functools import partial

from sqlalchemy import text

# local imports
from src.database import *
from src.model.auth import *
from src.model.infrastructure import *
from src.model.library import *
from src.model.school import *


# * (17..=82) The code below is really a redundant code
# * The code inside the method should declared directly in the main file
# * It's on a method to make it easier to read & minimize the view in the `code editor`
# * todo: I'm going to create a function that will create the routes for each schema
def define_routes():
    home: APIRouter = APIRouter()  # for home routes
    """
    # Home Route

    This route contains the main methods that will be used to display the home page of the application.

    ## Example
    - Get the home page
    - Get the about page
    - Get the contact page
    - Get the help page
    """

    @home.get("/", tags=["Main"])  # todo: Make this rout a redirect to the main web interface (svelte app) on the future...
    def _home_route(): return {"The interface for Academic Hub API is on: 127.0.0.1:8000/docs"}

    auth: APIRouter = APIRouter()  # for authentication routes
    """
    # Authentication Routes

    This route contains the main methods that will be used to authenticate users.

    """

    basic_dt: APIRouter = APIRouter()  # for data table routes
    """
    # Data Table Routes

    This routes contains some basic useful methods for the data tables.

    ## Example
    - Get the attributes of a table (all the columns)
    - Get all the resources of a table (all the rows)
    """

    crud_attr: APIRouter = APIRouter()  # crud routes for each attribute
    """
    # CRUD Routes

    This route contains the main methods that will be used to create, read, update and delete resources.

    todo: UPDATE THIS EXAMPLES TO MATCH THE NEW ROUTES...
    todo: Add the respective examples for each method
    ## Example
    - Create a new resource
    - Get all resources
    - Get a resource by ID
    - Update a resource by ID
    - Delete a resource by ID
    """

    views: APIRouter = APIRouter()  # todo: views routes... for views xd
    """
    # Views Routes

    This route contains the main methods that will be used to display the views of the application.

    ## Example
    - Get some useful view data to display on the application (for each schema)
    """

    print(f"\n\033[0;30;47mACADEMIC HUB\033[m\n")  # WHITE
    return home, auth, basic_dt, crud_attr, views

home, auth, basic_dt, crud_attr, views = define_routes()


def _add_schema_routes(schema: str, schema_classes: list[Type[Base]], db_dependency: Callable, b_color: str = ""):  # type: ignore
    print(f"\033[0;30;{b_color}m{schema.capitalize()}\033[m")  # YELLOW
    # print(f"\033[0;30;{b_color}mACADEMIC HUB - {schema.capitalize()}\033[m")  # YELLOW
    for schema_class in schema_classes:
        print(f"    \033[3m{schema_class.__name__}\033[m")
        dt_routes(schema_class, basic_dt, db_dependency)  # this is available for any db user
        # crud_routes(schema_class, crud_attr, db_dependency)  # this is available for any db user
    print()

# * Declare all the routes for each schema (in dependency order)
# * The Auth schema must be declared first (not really, but it's the most important one)
_add_schema_routes("auth", auth_classes, partial(get_db, "school"), "43")  # yellow
_add_schema_routes("infrastructure", infra_classes, partial(get_db, "infrastructure"), "44")  # blue
_add_schema_routes("library", lib_classes, partial(get_db, "library"), "41")  # red
# _add_schema_routes("school", school_classes, partial(get_db, "school"), "42")  # green


# ? TEST --------------------------------------------------------------------------------------

# * Pydantic (for dynamic routes)

# todo: CHECK THIS PYDANTIC STUFF
# todo: TO ALLOW THE 'DYNCAMIC' CREATION OF ROUTES
# todo: This means that the routes will be created based on the model's attributes
# todo: It allow the creation of routes for any model without having to write the routes manually... (I think!... I'm not sure xd)


# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from typing import List

# def get_building(db: Session, building_id: int):
#     return db.query(Building).filter(Building.id == building_id).first()

# # def get_buildings(db: Session, skip: int = 0, limit: int = 10):
# def get_buildings(db: Session):
# # def get_buildings(db: Session):
#     return db.query(Building).all()


# @home.get("/building/id={building_id}", tags=["Building"])
# def read_building(building_id: int, db: Session = Depends(partial(get_db, "infrastructure"))):
#     db_building = get_building(db, building_id=building_id)
#     if db_building is None:
#         raise HTTPException(status_code=404, detail="Building not found")
#     return db_building

# @home.get("/buildings/", tags=["Building"])
# # def read_buildings(skip: int = 0, limit: int = 10, db: Session = Depends(partial(get_db, "infrastructure"))):
# def read_buildings(db: Session = Depends(partial(get_db, "infrastructure"))):
#     buildings = get_buildings(db)
#     return buildings




# * Authentication Routes (test routes) -------------------------------------------------------

@auth.post("/token", tags=["Auth"])
def get_test_token(): return {"access_token": create_token(DEFAULT_USER)}

@auth.get("/protected", tags=["Auth"], dependencies=[Depends(JWTBearer())])
def protected_route(): return {"message": "You are viewing a protected route"}


# todo: Add the respective views for each schema! ------------------------------------------------
# * views routes
def _views_routes(
    router: APIRouter, 
    db_dependency: Callable,
):
    """
    Creates views routes for a given model and home.

    Args:
        router (APIRouter): The FastAPI router to which the endpoints will be added.
        db_dependency (Callable): Dependency that provides a DB session.
    """
    @home.get("/views/{view_name}/", tags=["views"])  # Decorate the route function with the GET route for getting all resources
    def get_view(view_name: str, db: Session = Depends(db_dependency)):  # Route function to get all resources
        view = db.execute(f"SELECT * FROM {view_name}").fetchall()  # Execute a raw SQL query to get the view data
        if not view:  # If the view is empty
            raise HTTPException(
                status_code=404,
                detail=f"No view named '{view_name}' found."
            )
        return view  # Return the view data

    # todo: SET THE AUTH FOR EACH USER (ADMIN or USER)
    # todo: ADMIN must be able to see all the tables for his schema (FOR EACH SCHEMA)
    # todo: USER can just see the data associated to him (school & library) 

