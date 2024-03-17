"""
    This file will contain the SQLAlchemy models and the database connection

    The database connection is created using SQLAlchemy. The database URL is read from the environment variables and used to create a new SQLAlchemy engine.

    The SessionLocal object is a sessionmaker that will be used to create a new session for each request. The get_db function is a dependency that will be used to get a new session for each request.
"""
import inspect
from fastapi import Depends, HTTPException
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import BinaryExpression, create_engine
from typing import Any, Type
from dotenv import load_dotenv
import os

# * Read the environment variables
load_dotenv()
# # DB_URL_EXAMPLE = "postgresql://user:password@localhost/dbname"
# DB_URL: str = f"postgresql://{os.environ.get('USER')}:{os.environ.get('PASSWORD')}@{os.environ.get('HOST')}/{os.environ.get('DB_NAME')}"

# ahub_library@localhost
DB_URL: str = f"postgresql://library_admin:secure_password_for_library@localhost/academic_hub"




# * Create a new SQLAlchemy engine, sessionmaker, and a Base class for the ORM models
engine = create_engine(DB_URL)
SessionLocal: sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    This function will be used to get a new session for each request.
    
    The session is a dependency that will be used in the path operation functions to get a new session for each request.

    The yield keyword is used to create a context manager that will return the db session to the path operation function and close the session when the path operation function finishes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# * GET method (Read)
def get_resource_generic(db: Session, model: Type[Base], condition: BinaryExpression = True) -> Any: # type: ignore
    """
    This method will be used to get a resource from the database based on a model and a condition.

    Args:
        - db (Session): The database session
        - model (Type[Base]): The model to use
    - condition (BinaryExpression): The condition to use to filter the resources
            - if no condition is provided, all the resources will be returned
    """
    # resource = db.query(model).filter(condition).all()
    # if not resource:
    #     raise HTTPException(status_code=404, detail=f"{model.__tablename__.capitalize()} not found")
    # return resource
    # ^ Just check this code... it's the same as the one below but without the if statement :3
    return db.query(model).filter(condition).all() or \
        (_ for _ in ()).throw(HTTPException(status_code=404, detail=f"{model.__name__.capitalize()} not found"))
        # (_ for _ in ()).throw(HTTPException(status_code=404, detail=f"{model.__tablename__.capitalize()} not found"))


# def // get_operations(model, any):
#     """
#     Wrapper function to create endpoints for fetching column names and all records of a model.
#     Uses the class name in lowercase for the endpoint paths.
#     """
    
#     @any.get(f"/{model.__name__.lower()}s/dt/", tags=[model.__name__])
#     def get_model_column_names():
#         """
#         Endpoint to fetch column names of the model.
#         """
#         return [c.name for c in model.__table__.columns]

# # PUT NAME USING ONLY THE FIRST LETTER AS UPPERCASE
#     @any.get(f"/{model.__name__.lower()}s/", tags=[model.__name__])    
#     def get_all_model_records(db: Session = Depends(get_db)):
#         """
#         Endpoint to fetch all records of the model.
#         """
#         return get_resource_generic(db, model)

#     @any.get(f"/{model.__name__.lower()}/id={id}", tags=[model.__name__])
#     def get_user_by_id(id: int, db: Session = Depends(get_db)):
#         return get_resource_generic(db, model, model.id == id)
    

# ? TEST --------------------------------------------------------------------------------------

# todo: Test this method
# * POST method (Create)
def create_resource_generic(db: Session, model: Type[Base], data: dict) -> Any:  # type: ignore
    """
    This method will be used to create a new resource in the database based on a model and some data.

    Args:
        - db (Session): The database session
        - model (Type[Base]): The model to use
        - data (dict): The data to use to create the new resource
    """
    new_resource = model(**data)
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
    return new_resource
