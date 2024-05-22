"""
    Some routes are common to all tables, such as getting the columns of a table or getting all the data from a table.

    Other routes are specific to each table, such as creating, reading, updating, and deleting resources.
"""
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import Integer, String, text
from pydantic import BaseModel, create_model

from typing import List, Optional, Type, Callable, Any

from src.api.database import Base


# * Data Table Routes (get columns & get all data)
def dt_routes(
    sqlalchemy_model: Type[Base],  # type: ignore
    pydantic_model: Type[BaseModel],
    router: APIRouter,
    db_dependency: Callable
):
    # * Get the columns of the table
    @router.get(f"/{sqlalchemy_model.__tablename__.lower()}/dt", tags=[sqlalchemy_model.__name__], response_model=List[str])
    def get_columns():
        return [c.name for c in sqlalchemy_model.__table__.columns]

    QueryParamsModel = create_model(  # Dynamically create a Pydantic model for query parameters
        f"{sqlalchemy_model.__name__}QueryParams",  # Model name
        **{attr: (Optional[column.type.python_type], None)  # Extract model attributes and their types
            for attr, column in sqlalchemy_model.__table__.columns.items()  # * Iterate over the table columns
        }  # * Create a dictionary of attributes & unpack it as keyword arguments (create_model)
    )

    # * Define the route to get all resources
    @router.get(f"/{sqlalchemy_model.__tablename__.lower()}s", tags=[sqlalchemy_model.__name__], response_model=List[pydantic_model])
    def get_all_resources(
        db: Session = Depends(db_dependency),
        filters: QueryParamsModel = Depends()  # take the query parameters as a dependency  # type: ignore
    ):
        query = db.query(sqlalchemy_model)
        for attr, value in filters.dict().items():
            if value is not None:
                query = query.filter(getattr(sqlalchemy_model, attr) == value)
        return query.all()

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
        db_resource: Base = sqlalchemy_model(**resource.dict())  # Create a new resource instance
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

# * View Routes (get views)
def view_routes(
    schema: str,
    router: APIRouter,
    db_dependency: Callable
):
    @router.get(f"/{schema.lower()}/views", tags=['Views'], response_model=List[str])
    def get_views(db: Session = Depends(db_dependency)):
        query = text("SELECT table_name FROM information_schema.views WHERE table_schema = :schema")
        result = db.execute(query, {'schema': f'{schema}_management'}).fetchall()
        return [row[0] for row in result]

    def create_view_route(view: str):
        # Get the column metadata for the view from information_schema.columns
        query = text("""
            SELECT column_name, is_nullable, data_type 
            FROM information_schema.columns 
            WHERE table_schema = :schema AND table_name = :view
        """)
        columns = next(db_dependency()).execute(query, {'schema': f'{schema}_management', 'view': view}).fetchall()
        QueryParamsModel = create_model(  # Create a Pydantic model for query parameters
            f"{view}QueryParams",
            **{col[0]: (Optional[Any], None) for col in columns}
        )

        @router.get(f"/{schema.lower()}/view/{view}", tags=["Views"])
        def get_view(
            db: Session = Depends(db_dependency),
            filters: QueryParamsModel = Depends()  # Use the Pydantic model as a dependency
        ):
            base_query = f"SELECT * FROM {schema}_management.{view}"
            filter_clauses = [
                f"{key} = :{key}" for key, value in filters.dict().items() if value is not None
            ]
            if filter_clauses: base_query += " WHERE " + " AND ".join(filter_clauses)
            return [dict(row._mapping) for row in db.execute(text(base_query), filters.dict()).fetchall()]

    views = next(db_dependency()).execute(
        text("SELECT table_name FROM information_schema.views WHERE table_schema = :schema"), 
        {'schema': f'{schema}_management'}
    ).fetchall()

    [create_view_route(view) for view in [row[0] for row in views]]

