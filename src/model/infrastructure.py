from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, Numeric
from src.database import base_model


SchemaBaseModel, IDBaseModel, NamedBaseModel = base_model(schema='infrastructure_management')

