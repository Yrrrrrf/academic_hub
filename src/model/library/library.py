from fastapi import Depends
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session, relationship

from src.database import Base, get_db, get_resource_generic
from src.routes.library_routes import by_attribute

# from .link_tables import libro_biblioteca
# from .link_tables import LibroBiblioteca


class Library(Base):
    __tablename__ = "library"
    __table_args__ = {"schema": "library_management"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)

    # ^ relationships <link_tables>
    # libros = relationship("Book", secondary="libro_biblioteca", back_populates="bibliotecas")

# get_operations(Library, by_attribute)

# ? CRUD Methods -----------------------------------------------------------------------

# * CREATE (.post)
@by_attribute.get("/librarys/dt/", tags=['Library'])
def get_columns():
    return [c.name for c in Library.__table__.columns]

@by_attribute.get("/librarys/", tags=['Library'])
def get_all_libraries(db: Session = Depends(get_db)):
    return get_resource_generic(db, Library)

@by_attribute.get("/library/id={id}", tags=['Library'])
def get_library_by_id(id: int, db: Session = Depends(get_db)):
    return get_resource_generic(db, Library, Library.id == id)

@by_attribute.get("/library/name={name}", tags=['Library'])
def get_library_by_name(name: str, db: Session = Depends(get_db)):
    return get_resource_generic(db, Library, Library.name == name)


# # list all the books inside a library (with repeated books)
# @by_attribute.get('/library/books/all/{library_id}', tags=['library'])
# def get_all_books_in_library(library_id: int, db: Session = Depends(get_db)):
#     library = db.query(Library).filter(Library.id == library_id).first()
#     return library.libros


# # create library
# @by_attribute.post('/library', tags=['library'])
# def create_library(library: Library, db: Session = Depends(get_db)):
#     db.add(library)
#     db.commit()
#     db.refresh(library)
#     return library

