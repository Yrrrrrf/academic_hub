from fastapi import Depends
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session, relationship

from src.database import Base, get_db, get_resource_generic
from src.routes.library_routes import by_attribute


class Topic(Base):
    __tablename__ = "topic"
    __table_args__ = {"schema": "library_management"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)

    # libros = relationship("Book", secondary="libro_tema", back_populates="temas")


@by_attribute.get("/topics/dt/", tags=['Topic'])
def get_columns():
    return [c.name for c in Topic.__table__.columns]

@by_attribute.get("/topics/", tags=['Topic'])
def get_all_topics(db: Session = Depends(get_db)):
    return get_resource_generic(db, Topic, Topic.id > 0)

@by_attribute.get("/topic/id={id}", tags=['Topic'])
def get_topic_by_id(id: int, db: Session = Depends(get_db)):
    return get_resource_generic(db, Topic, Topic.id == id)

@by_attribute.get("/topic/name={name}", tags=['Topic'])
def get_topic_by_name(name: str, db: Session = Depends(get_db)):
    return get_resource_generic(db, Topic, Topic.name == name)
