"""
    # Database "ACADEMIC HUB"

    This file will contain the SQLAlchemy models and the database connection

    The database connection is created using SQLAlchemy. The database URL is read from the environment variables and used to create a new SQLAlchemy engine.

    The SessionLocal object is a sessionmaker that will be used to create a new session for each request. The get_db function is a dependency that will be used to get a new session for each request.
"""
from dotenv import load_dotenv

from pydantic import BaseModel, Field, create_model
from sqlalchemy import create_engine, MetaData, Column, Integer, String, Boolean, Numeric, Text, Date, Time, DateTime, JSON, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base, declared_attr

import re
from typing import Callable, Dict, Optional, Type, Any, List


# os.environ.clear()  # * Clear all environment variables (to avoid conflicts with old values)
load_dotenv()  # * Load environment variables from .env file


db_url = f"postgresql://postgres:fire@localhost/academic_hub"
engine=create_engine(db_url) 

def get_db(user_type: str):
    """
        Yields a database session for the specified user type.

        Args:
            user_type (str): The user type for the database connection.
    """
    # db_url = f"postgresql://{os.getenv(f'{user_type}_ADMIN')}:{os.getenv(f'{user_type}_PWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    print(f"Connecting to {user_type} database at {db_url}")
    db: Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    try:
        yield db
    finally:
        db.close()

def get_classes_from_globals(globals_dict) -> list:
    """
    Retrieve a list of classes defined in the given global scope.
    
    :param globals_dict: The globals() dictionary from the calling module.
    :return: A list of class objects defined in the global scope.
    """
    return [obj for name, obj in globals_dict.items() if isinstance(obj, type) and obj.__module__ == globals_dict['__name__']]

Base = declarative_base()

#  * Helper function to create base models (abstract classes) for SQLAlchemy models
def base_model(schema: str = 'public'):
    """
    Create base models for an specific schema.

    They all inherit from the same base class and have the same table arguments.
    """
    class CustomBaseModel:
        @declared_attr
        def __tablename__(cls):
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)).lower()

    class SchemaBaseModel(declarative_base(cls=CustomBaseModel)):
        __abstract__ = True
        __table_args__ = {'schema': schema}

    class IDBaseModel(SchemaBaseModel):
        __abstract__ = True
        id = Column(Integer, primary_key=True, index=True)

    class NamedBaseModel(IDBaseModel):
        __abstract__ = True
        name = Column(String(255), nullable=False)

    return SchemaBaseModel, IDBaseModel, NamedBaseModel

Base = declarative_base()

def generate_sqlalchemy_model_class(table_name: str, columns: list, primary_keys: list, base=Base) -> Type[Base]:
    attrs = {'__tablename__': table_name}

    for column_name, column_type in columns:
        column_kwargs = {}
        if column_name in primary_keys:
            column_kwargs['primary_key'] = True

        match column_type:
            case 'boolean':
                column = Column(Boolean, **column_kwargs)
            case 'integer':
                column = Column(Integer, **column_kwargs)
            case 'numeric':
                column = Column(Numeric, **column_kwargs)
            case 'text':
                column = Column(Text, **column_kwargs)
            case 'varchar':
                column = Column(String, **column_kwargs)
            case 'date':
                column = Column(Date, **column_kwargs)
            case 'time':
                column = Column(Time, **column_kwargs)
            case 'timestamp':
                column = Column(DateTime, **column_kwargs)
            case 'jsonb':
                column = Column(JSON, **column_kwargs)
            case _:
                print(f"Unknown column type '{column_type}' for column '{column_name}'")
                column = Column(String, **column_kwargs)  # Default to String for unknown types

        attrs[column_name] = column

    model_class = type(table_name.capitalize(), (base,), attrs)
    print(f"Generated SQLAlchemy model class for table '{table_name}': {model_class.__dict__}")
    return model_class


def create_models_from_metadata(engine, schema: str, base=Base) -> dict:
    metadata = MetaData()
    metadata.reflect(bind=engine, schema=schema, extend_existing=True)  # Reflect the schema with extend_existing=True

    models: dict = {}
    for table_name, table in metadata.tables.items():
        if table.schema == schema:
            columns = [(col.name, col.type.__class__.__name__.lower()) for col in table.columns]
            primary_keys = [col.name for col in table.columns if col.primary_key]
            model_class = generate_sqlalchemy_model_class(table_name, columns, primary_keys, base)
            models[table_name] = model_class

            # Debugging information
            print(f"Generated model for table {table_name} with columns {columns} and primary keys {primary_keys}")

    return models


# Example usage:
all_models: dict[str, Type[Base]] = {}  # A dictionary to store all generated models  # type: ignore
for schema in ['public', 'school_management', 'library_management', 'infrastructure_management']:
    models = create_models_from_metadata(engine, schema)
    all_models.update(models)
    print(f"\nModels for schema '{schema}':")
    [print(f"\t{name.split('.')[1]}: {model.__table__.columns.keys()}") for name, model in models.items()]


# Mapping of SQL data types to Pydantic (Python) types
SQL_TO_PYTHON_TYPE = {
    'boolean': bool,
    'integer': int,
    'numeric': float,
    'text': str,
    'character varying': str,
    'date': str,  # Dates can be str or datetime.date
    'time': str,  # Times can be str or datetime.time
    'timestamp': str,  # Timestamps can be str or datetime.datetime
    'jsonb': dict
}

def create_pydantic_model(
    db: Session, 
    schema: str, 
    table: str, 
    model_name: str
) -> Type[BaseModel]:
    query = text("""
        SELECT column_name, is_nullable, data_type 
        FROM information_schema.columns
        WHERE table_schema = :schema AND table_name = :table
    """)
    columns = db.execute(query, {'schema': schema, 'table': table}).fetchall()
    
    fields = {}
    for col in columns:
        column_name = col[0]  # column_name is the first field
        data_type = col[2]  # data_type is the third field
        
        python_type = SQL_TO_PYTHON_TYPE.get(data_type, str)  # Default to str if type is unknown
        fields[column_name] = (Optional[python_type], None)  # Make all fields Optional with default None
    
    return create_model(model_name, **fields)