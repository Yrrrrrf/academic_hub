"""
    Some routes are common to all tables, such as getting the columns of a table or getting all the data from a table.

    Other routes are specific to each table, such as creating, reading, updating, and deleting resources.
"""
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import Integer, String, inspect, text
from pydantic import BaseModel, create_model

from typing import Dict, List, Optional, Type, Callable, Any

from src.api.database import Base, all_models, create_pydantic_model


# * Add `get_tables` for a schema to the router & `get_columns` for each table
def schema_dt_routes(
    schema: str,
    db_dependency: Callable, 
    router: APIRouter
):
    """
    Add routes for the tables of a schema to the basic_dt router.

    Args:
        schema (str): The schema name.
        db_dependency (Callable): The dependency function to get the database session.
    """
    @router.get(f"/{schema.lower()}/tables", response_model=List[str], tags=[schema])
    def get_tables():
        all_tables = [model.__tablename__ for model in all_models.values()]
        # todo: Improve this filter to get only the tables of the schema...
        schema_tables = [table for table in all_tables if table.split('.')[0] == f'{schema.lower()}']
        schema_tables = [table.split('.')[1] for table in schema_tables]
        return schema_tables

    def create_column_route(model):
        @router.get(f"/{model.__tablename__.split('.')[-1]}/columns", response_model=List[str], tags=[schema])
        def get_columns(): 
            return [c.name for c in model.__table__.columns]
        return get_columns


    def get_all_resources_route(model, db_dependency):
        QueryParamModel: Type[BaseModel] = create_pydantic_model(
            next(db_dependency()), schema, model.__tablename__.split('.')[-1],
            f"{model.__tablename__.split('.')[-1]}QueryParams"
        )

        @router.get(f"/{model.__tablename__.split('.')[-1]}/all", tags=[schema], response_model=List[QueryParamModel])
        def get_all(
            db: Session = Depends(db_dependency),
            filters: QueryParamModel = Depends()
        ):
            query = db.query(model)
            for attr, value in filters.dict().items():
                if value is not None:
                    # query = query.filter(getattr(model, attr) == value)
                    query = query
            return query.all()

        return get_all

    for model in [model for model in all_models.values() if model.__tablename__.split('.')[0] == f'{schema.lower()}']:
        get_all_resources_route(model, db_dependency)
        pass
        # create_column_route(model)


# * Add all views of a schema to the router
def schema_view_routes(
    schema: str,
    db_dependency: Callable,
    router: APIRouter,
):
    @router.get(f"/{schema.lower()}/views", tags=['Views'], response_model=List[str])
    def get_views(db: Session = Depends(db_dependency)):
        query = text("SELECT table_name FROM information_schema.views WHERE table_schema = :schema")
        result = db.execute(query, {'schema': f'{schema}'}).fetchall()
        print(result)
        return [row[0] for row in result]

    def create_view_route(view: str):
        QueryParamModel: Type[BaseModel] = create_pydantic_model(
            next(db_dependency()), schema, view, 
            f"{view}QueryParams"
        )

        @router.get(f"/{schema.lower()}/view/{view}", tags=["Views"], response_model=List[QueryParamModel])
        def get_view(
            db: Session = Depends(db_dependency),
            filters: QueryParamModel = Depends()
        ):
            base_query: str = f"SELECT * FROM {schema}.{view}"
            filter_clauses: list[str] = [f"{key} = :{key}" for key in filters.dict().keys() if filters.dict()[key] is not None]
            if filter_clauses: base_query += " WHERE " + " AND ".join(filter_clauses)
            return [dict(row._mapping) for row in db.execute(text(base_query), filters.dict()).fetchall()]

    views = next(db_dependency()).execute(
        text("SELECT table_name FROM information_schema.views WHERE table_schema = :schema"), 
        {'schema': f'{schema}'}
    ).fetchall()

    [create_view_route(view) for view in [row[0] for row in views]]



# * CRUD Operations Routes (GET, POST, PUT, DELETE)
def crud_routes(
    sqlalchemy_model: Type[Base],  # type: ignore
    pydantic_model: Type[BaseModel],
    router: APIRouter,
    db_dependency: Callable,
    excluded_attributes: List[str] = ["id", "created_at", "password", "additional_info"]
):
    # * POST (Create)
    @router.post(f"/{sqlalchemy_model.__tablename__.lower()}", tags=[sqlalchemy_model.__name__], response_model=pydantic_model)
    def create_resource(resource: pydantic_model, db: Session = Depends(db_dependency)):
        db_resource: Base = sqlalchemy_model(resource.model_dump())  # type: ignore
        db.add(db_resource)
        try:
            db.commit()
            db.refresh(db_resource)
        except Exception as e:
            db.rollback()
            raise e
        return db_resource

    # rest of the CRUD operations...
    def _create_route(attribute: str, attribute_type: Any, route_type: str):
        match route_type:
            case "GET":
                @router.get(f"/{sqlalchemy_model.__tablename__.lower()}/{attribute}={{value}}", tags=[sqlalchemy_model.__name__], response_model=List[pydantic_model])
                def get_resource(value: attribute_type, db: Session = Depends(db_dependency)):  # type: ignore
                    result = db.query(sqlalchemy_model).filter(getattr(sqlalchemy_model, attribute) == value).all()
                    if not result:
                        raise HTTPException(status_code=404, detail=f"No {sqlalchemy_model.__name__} with {attribute} '{value}' found.")
                    return result

            case "PUT":
                @router.put(f"/{sqlalchemy_model.__tablename__.lower()}/{attribute}={{value}}", tags=[sqlalchemy_model.__name__], response_model=pydantic_model)
                def update_resource(value: attribute_type, resource: pydantic_model, db: Session = Depends(db_dependency)):  # type: ignore
                    db_resource = db.query(sqlalchemy_model).filter(getattr(sqlalchemy_model, attribute) == value).first()
                    if not db_resource:
                        raise HTTPException(status_code=404, detail=f"No {sqlalchemy_model.__name__} with {attribute} '{value}' found.")

                    for key, value in resource.dict(exclude_unset=True).items():
                        setattr(db_resource, key, value)

                    try:
                        db.commit()
                        db.refresh(db_resource)
                    except Exception as e:
                        db.rollback()
                        raise e

                    return db_resource

            case "DELETE":
                @router.delete(f"/{sqlalchemy_model.__tablename__.lower()}/{attribute}={{value}}", tags=[sqlalchemy_model.__name__])
                def delete_resource(value: attribute_type, db: Session = Depends(db_dependency)):  # type: ignore
                    db_resource = db.query(sqlalchemy_model).filter(getattr(sqlalchemy_model, attribute) == value).first()
                    if not db_resource:
                        raise HTTPException(status_code=404, detail=f"No {sqlalchemy_model.__name__} with {attribute} '{value}' found.")

                    try:
                        db.delete(db_resource)
                        db.commit()
                    except Exception as e:
                        db.rollback()
                        raise e

                    return {
                        "message": f"Successfully deleted {sqlalchemy_model.__name__} with {attribute} '{value}'",
                        "resource": db_resource
                    }
                
            case _: raise ValueError(f"Invalid route type: {route_type}")

    included_attributes = [(attr, col.type.__class__)
        for attr, col in sqlalchemy_model.__table__.columns.items()
        # if attr not in excluded_attributes  # * exclude certain attributes
    ]

    for attr, attr_type in included_attributes:  # * Iterate over the included attributes
        # param_type = int if attr_type == Integer else str if attr_type == String else str  # Default to str if type is unknown
        # [_create_route(attr, param_type, method) for method in ["GET", "PUT", "DELETE"]]
        # param_type =  if attr_type == String else str  # Default to str if type is unknown
        [_create_route(attr, int if attr_type == Integer else str, method) for method in ["GET", "PUT", "DELETE"]]

