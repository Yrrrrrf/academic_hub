from fastapi import Depends
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from src.database import Base, get_db, get_resource_generic
from src.routes.library_routes import by_attribute


class Publisher(Base):
    __tablename__ = "publisher"
    __table_args__ = {"schema": "library_management"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)

# get_operations(Publisher, by_attribute)

@by_attribute.get("/publishers/dt/", tags=['Publisher'])
def get_columns():
    return [c.name for c in Publisher.__table__.columns]

@by_attribute.get("/publishers/", tags=['Publisher'])
def get_all_publishers(db: Session = Depends(get_db)):
    return get_resource_generic(db, Publisher)

@by_attribute.get("/publisher/id={id}", tags=['Publisher'])
def get_publisher_by_id(id: int, db: Session = Depends(get_db)):
    return get_resource_generic(db, Publisher, Publisher.id == id)

# by name
@by_attribute.get("/publisher/name={name}", tags=['Publisher'])
def get_publisher_by_name(name: str, db: Session = Depends(get_db)):
    return get_resource_generic(db, Publisher, Publisher.name == name)