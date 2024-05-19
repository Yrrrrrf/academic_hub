from sqlalchemy import *
from sqlalchemy.orm import relationship

from src.api.database import *


SchemaBaseModel, IDBaseModel, NamedBaseModel = base_model(schema='infrastructure_management')


class Building(NamedBaseModel):
    address = Column(Text)
    total_floors = Column(Integer)
    accessibility_features = Column(Boolean, default=False)

    rooms = relationship('Room', back_populates='building')

class RoomType(NamedBaseModel):
    name = Column(String(32), unique=True, nullable=False)

class Room(IDBaseModel):
    room_type = Column(Integer, ForeignKey('infrastructure_management.room_type.id'), nullable=False)
    name = Column(String(32))
    building_id = Column(Integer, ForeignKey('infrastructure_management.building.id'), nullable=False)
    capacity = Column(Integer)
    equipment_details = Column(JSON, default={})

    building = relationship('Building', back_populates='rooms')

class Faculty(NamedBaseModel):
    name = Column(String(255), nullable=False)

class FacultyBuilding(SchemaBaseModel):
    faculty_id = Column(Integer, ForeignKey('infrastructure_management.faculty.id'), primary_key=True, nullable=False)
    building_id = Column(Integer, ForeignKey('infrastructure_management.building.id'), primary_key=True, nullable=False)

class Library(IDBaseModel):
    faculty_id = Column(Integer, ForeignKey('infrastructure_management.faculty.id'), nullable=False)
    building_id = Column(Integer, ForeignKey('infrastructure_management.building.id'), nullable=False)


infra_sql_classes: List[Type[Base]] = get_classes_from_globals(globals())  # type: ignore
infra_pydantic_classes = [create_pydantic_model(sql_class, BaseModel) for sql_class in infra_sql_classes]
