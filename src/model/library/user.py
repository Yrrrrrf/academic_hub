from fastapi import Depends
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from src.database import Base, get_db, get_resource_generic
from src.routes.library_routes import by_attribute


class AcademicMember(Base):
    __tablename__ = "academic_member"
    __table_args__ = {"schema": "library_management"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)

# get_operations(AcademicMember, by_attribute)

@by_attribute.get("/users/dt/", tags=['AcademicMember'])
def get_columns():
    return [c.name for c in AcademicMember.__table__.columns]

@by_attribute.get("/users/", tags=['AcademicMember'])
def get_all_users(db: Session = Depends(get_db)):
    return get_resource_generic(db, AcademicMember)

@by_attribute.get("/user/id={id}", tags=['AcademicMember'])
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    return get_resource_generic(db, AcademicMember, AcademicMember.id == id)

@by_attribute.get("/user/name={name}", tags=['AcademicMember'])
def get_user_by_name(name: str, db: Session = Depends(get_db)):
    return get_resource_generic(db, AcademicMember, AcademicMember.name == name)
