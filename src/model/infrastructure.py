from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, JSON, ForeignKeyConstraint
from src.database import base_model, get_classes_from_globals


SchemaBaseModel, IDBaseModel, NamedBaseModel = base_model(schema='infrastructure_management')


class Building(NamedBaseModel):
    address = Column(Text)
    total_floors = Column(Integer)
    accessibility_features = Column(Boolean, default=False)

class RoomType(NamedBaseModel):
    name = Column(String(32), unique=True, nullable=False)

class Room(IDBaseModel):
    room_type = Column(Integer, ForeignKey('infrastructure_management.room_type.id'), nullable=False)
    name = Column(String(32))
    building_id = Column(Integer, ForeignKey('infrastructure_management.building.id'), nullable=False)
    capacity = Column(Integer)
    equipment_details = Column(JSON)

class Faculty(NamedBaseModel):
    name = Column(String(255), nullable=False)
    # coordinates = Column(Geography('POINT', srid=4326))  # Uncomment if using PostGIS

class FacultyBuilding(SchemaBaseModel):
    faculty_id = Column(Integer, ForeignKey('infrastructure_management.faculty.id'), primary_key=True, nullable=False)
    building_id = Column(Integer, ForeignKey('infrastructure_management.building.id'), primary_key=True, nullable=False)

class Library(IDBaseModel):
    faculty_id = Column(Integer, ForeignKey('infrastructure_management.faculty.id'), nullable=False)
    building_id = Column(Integer, ForeignKey('infrastructure_management.building.id'), nullable=False)

# Collect all the infrastructure management classes
infra_classes: list = get_classes_from_globals(globals())
