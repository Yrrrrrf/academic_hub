# 3rd party imports
from fastapi import Depends, HTTPException, APIRouter, Query
from sqlalchemy.orm import Session, Query, aliased
from sqlalchemy import text
from pydantic import BaseModel

# stdlib imports
from typing import Any, Dict, List, Type, Callable
from functools import partial

# local imports
from src.api.database import *
from src.api.route_generators import *
from src.api.auth import *
from src.model.public import *
from src.model.infrastructure import *
from src.model.school import *
from src.model.library import *


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
    return home, basic_dt, crud_attr, views

home, basic_dt, crud_attr, views = define_routes()

# todo: ADD SOME NEW GENERATOR TO CREATE THE SQL_CALSSES USING SOME METADATA FROM THE DATABASE...
# * this will allow to create the routes for each schema dynamically...
# * this will allow to create the routes for each schema dynamically...
# * this will allow to create the routes for each schema dynamically...
# * this will allow to create the routes for each schema dynamically...
# * this will allow to create the routes for each schema dynamically...
# * this will allow to create the routes for each schema dynamically...
# * this will allow to create the routes for each schema dynamically...
# * this will allow to create the routes for each schema dynamically...
# * this will allow to create the routes for each schema dynamically...
# * this will allow to create the routes for each schema dynamically...
# * this will allow to create the routes for each schema dynamically...
# * this will allow to create the routes for each schema dynamically...
# * this will allow to create the routes for each schema dynamically...
# * this will allow to create the routes for each schema dynamically...
# * this will allow to create the routes for each schema dynamically...


def _add_schema_routes(
    schema: str, 
    sql_classes: list[Type[Base]],  # type: ignore
    pydantic_classes: list[Type[BaseModel]],  # type: ignore
    db_dependency: Callable, 
    b_color: str = ""
):
    print(f"\033[0;30;{b_color}m{schema.capitalize()}\033[m")

    # * By Schema (routes for each schema)
    # data table routes
    @basic_dt.get(f"/{schema.lower()}/tables", response_model=List[str], tags=["Tables"])
    def get_tables(): return [sql_class.__tablename__ for sql_class in sql_classes]
    # views routes (all the views of the schema)
    view_routes(schema, views, db_dependency)

    # * By Table (ORM) (routes for each table)
    for sql_class, pydantic_class in zip(sql_classes, pydantic_classes):
        print(f"    \033[3m{sql_class.__name__:25}\033[m{pydantic_class.__name__}")
        dt_routes(sql_class, pydantic_class, basic_dt, db_dependency)
        crud_routes(sql_class, pydantic_class, crud_attr, db_dependency)
    print()


# * Add routes:        SCHEMA            SQL CLASSES         PYDANTIC CLASSES               DB DEPENDENCY
_add_schema_routes(        "public", public_sql_classes, public_pydantic_classes,         partial(get_db, "school"), "43")
_add_schema_routes("infrastructure",  infra_sql_classes,  infra_pydantic_classes, partial(get_db, "infrastructure"), "42")
_add_schema_routes(        "school", school_sql_classes, school_pydantic_classes,         partial(get_db, "school"), "41")
_add_schema_routes(       "library",    lib_sql_classes,    lib_pydantic_classes,        partial(get_db, "library"), "44")
