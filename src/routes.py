# 3rd party imports
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import Integer, String

# stdlib imports
from typing import List, Type, Callable, Any
from functools import partial


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

    # @home.get("/", tags=["Main"])  # todo: Make this rout a redirect to the main web interface (svelte app) on the future...
    # def _home_route(): return {"The interface for Academic Hub API is on: 127.0.0.1:8000/docs"}

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
        # dt_routes(schema_class, basic_dt, db_dependency)  # this is available for any db user
        # crud_routes(schema_class, crud_attr, db_dependency)  # this is available for any db user
    print()

# * Declare all the routes for each schema (in dependency order)
# * The Auth schema must be declared first (not really, but it's the most important one)
# _add_schema_routes("auth", auth_classes, partial(get_db, "school"), "43")  # yellow
# _add_schema_routes("infrastructure", infra_classes, partial(get_db, "infrastructure"), "44")  # blue
# _add_schema_routes("library", lib_classes, partial(get_db, "library"), "41")  # red
# _add_schema_routes("school", school_classes, partial(get_db, "school"), "42")  # green


# ? TEST --------------------------------------------------------------------------------------

# * Pydantic (for dynamic routes)

# todo: CHECK THIS PYDANTIC STUFF
# todo: TO ALLOW THE 'DYNCAMIC' CREATION OF ROUTES
# todo: This means that the routes will be created based on the model's attributes
# todo: It allow the creation of routes for any model without having to write the routes manually... (I think!... I'm not sure xd)


def crud_operations(
    model: Type[Base],  # type: ignore
    create_model: Type[BaseModel],
    update_model: Type[BaseModel],
    response_model: Type[BaseModel],
    router: APIRouter,
    db_dependency: Callable,
    excluded_attributes: List[str] = ["id", "created_at", "password_hash", "additional_info"]
):
    """
    Creates CRUD routes for a given model.

    Args:
        model (Type[Base]): The SQLAlchemy model class.
        create_model (Type[BaseModel]): The Pydantic model class for request validation (POST).
        update_model (Type[BaseModel]): The Pydantic model class for request validation (PUT).
        response_model (Type[BaseModel]): The Pydantic model class for response formatting.
        router (APIRouter): The FastAPI router to which the endpoints will be added.
        db_dependency (Callable): Dependency that provides a DB session.
        excluded_attributes (List[str]): List of attributes to exclude from CRUD operations (default: ["id"]).
    """

    # @router.get(f"/{model.__tablename__.lower()}/dt", tags=[model.__name__], response_model=List[str])
    @router.get(f"/{model.__tablename__.lower()}/dt", tags=[model.__name__])
    def get_columns():
        return [c.name for c in model.__table__.columns]

    @router.get(f"/{model.__tablename__.lower()}s", tags=[model.__name__], response_model=List[response_model])
    def get_all(db: Session = Depends(db_dependency)):
        return db.query(model).all()

    # * GET (Read)
    def _get_route(attribute: str, attribute_type: Any):
        if attribute_type == Integer:
            param_type = int
        elif attribute_type == String:
            param_type = str
        else:
            param_type = str  # Default to str if type is unknown

        @router.get(f"/{model.__tablename__.lower()}/{attribute}={{value}}", tags=[model.__name__], response_model=List[response_model])
        def get_resource(value: param_type, db: Session = Depends(db_dependency)):
            result = db.query(model).filter(getattr(model, attribute) == value).all()
            if not result:
                raise HTTPException(status_code=404, detail=f"No {model.__name__} with {attribute} '{value}' found.")
            return result

    # # * POST (Create)
    # @router.post(f"/{model.__tablename__.lower()}/", tags=[model.__name__], response_model=response_model)
    # def create_resource(resource: create_model, db: Session = Depends(db_dependency)):
    #     db_resource: Base = model(**resource.dict())  # Create a new resource instance
    #     db.add(db_resource)
    #     try:
    #         db.commit()
    #         db.refresh(db_resource)
    #     except Exception as e:
    #         db.rollback()  # Rollback the transaction
    #         raise e  # Raise the exception
    #     return db_resource  # Return the resource data

    # * PUT (Update)
    def _put_route(attribute: str, attribute_type: Any):
        if attribute_type == Integer:
            param_type = int
        elif attribute_type == String:
            param_type = str
        else:
            param_type = str  # Default to str if type is unknown

        @router.put(f"/{model.__tablename__.lower()}/{attribute}={{value}}", tags=[model.__name__], response_model=response_model)
        def update_resource(value: param_type, resource: update_model, db: Session = Depends(db_dependency)):
            condition = getattr(model, attribute) == value
            db_resource = db.query(model).filter(condition).first()
            if not db_resource:
                raise HTTPException(status_code=404, detail=f"No {model.__name__} with {attribute} '{value}' found.")

            for key, value in resource.dict(exclude_unset=True).items():
                setattr(db_resource, key, value)

            try:
                db.commit()
                db.refresh(db_resource)
            except Exception as e:
                db.rollback()
                raise e

            return db_resource

    # * DELETE (Delete)
    def _delete_route(attribute: str, attribute_type: Any):
        if attribute_type == Integer:
            param_type = int
        elif attribute_type == String:
            param_type = str
        else:
            param_type = str  # Default to str if type is unknown

        @router.delete(f"/{model.__tablename__.lower()}/{attribute}={{value}}", tags=[model.__name__])
        def delete_resource(value: param_type, db: Session = Depends(db_dependency)):
            condition = getattr(model, attribute) == value
            db_resource = db.query(model).filter(condition).first()
            if not db_resource:
                raise HTTPException(status_code=404, detail=f"No {model.__name__} with {attribute} '{value}' found.")

            try:
                db.delete(db_resource)
                db.commit()
            except Exception as e:
                db.rollback()
                raise e

            # return the deleted resource
            return {
                "message": f"Successfully deleted {model.__name__} with {attribute} '{value}'",
                "resource": db_resource
                }

    included_attributes = [
        (attr, col.type.__class__)
        for attr, col in model.__table__.columns.items()
        # if attr not in excluded_attributes
    ]

    for attr, attr_type in included_attributes:
        _get_route(attr, attr_type)
        _put_route(attr, attr_type)
        _delete_route(attr, attr_type)


crud_operations(
    model=GeneralUser,
    create_model=UserCreate,
    update_model=UserCreate,
    response_model=UserResponse,
    router=basic_dt,
    db_dependency=partial(get_db, "school")
)

# * Authentication Routes (test routes) -------------------------------------------------------

@home.post("/auth/register", tags=["Auth"], response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(partial(get_db, "school"))):
    user_dict = user.model_dump()
    user_dict["password_hash"] = hash_password(user.password_hash)
    db_user = GeneralUser(**user_dict)
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise e
    return db_user

@home.post("/auth/login", tags=["Auth"], response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(GeneralUser).filter(GeneralUser.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@home.get("/users/me", tags=["Auth"], response_model=UserResponse)
def read_users_me(current_user: GeneralUser = Depends(get_current_user)):
    return current_user



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

