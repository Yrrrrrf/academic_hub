from pydantic import BaseModel
from typing import Optional

from src.database import get_classes_from_globals, Base


class BuildingBase(BaseModel):
    __tablename__ = 'building'
    __table_args__ = {'schema': 'infrastructure_management'}

    name: str


# class BuildingBase(BaseModel):
#     name: str
#     address: Optional[str] = None
#     total_floors: Optional[int] = None
#     accessibility_features: Optional[bool] = False

# class BuildingCreate(BuildingBase):
#     pass

# class BuildingUpdate(BuildingBase):
#     pass

# class BuildingInDB(BuildingBase):
#     id: int

#     class Config:
#         orm_mode = True




# from sqlalchemy import Column, Integer, String, Boolean, Text
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()


# class Building(Base):
#     __tablename__ = 'building'
#     __table_args__ = {'schema': 'infrastructure_management'}
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255), nullable=False)
#     address = Column(Text)
#     total_floors = Column(Integer)
#     accessibility_features = Column(Boolean, default=False)

# # 


infra_classes: list = get_classes_from_globals(globals())
