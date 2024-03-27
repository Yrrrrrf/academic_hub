from cgitb import text
from typing import Any, Type
from fastapi import Depends, HTTPException
from sqlalchemy.inspection import inspect
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Session, relationship

from src.database import *
from src.routes.library_routes import by_attribute


class Book(Base):
    __tablename__ = "book"
    __table_args__ = {"schema": "library_management"}


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    publisher_id = Column(Integer, ForeignKey('publisher.id'), index=True)
    # TODO: CHANGE IT TO HAVE A LENGHT JUST FOR ISBN (13 DIGITS)
    isbn = Column(String(45), index=True, nullable=True)

    # ^ Relationships <link_tables>
    # autores = relationship("Author", secondary="libro_autor")
    # temas = relationship("Topic", secondary="libro_tema")
    # bibliotecas = relationship("Library", secondary="libro_biblioteca")

@by_attribute.get("/books/dt/", tags=['Book'])
def get_columns():
    return [c.name for c in Book.__table__.columns]

@by_attribute.get("/books/", tags=['Book'])
def get_all_books(db: Session = Depends(get_db)):
    return get_resource_generic(db, Book)

@by_attribute.get("/book/id={id}", tags=['Book'])
def get_book_by_id(id: int, db: Session = Depends(get_db)):
    return get_resource_generic(db, Book, Book.id == id)

# by name
@by_attribute.get("/book/name={name}", tags=['Book'])
def get_book_by_name(name: str, db: Session = Depends(get_db)):
    return get_resource_generic(db, Book, Book.name == name)

@by_attribute.get("/book/publisher_id={publisher_id}", tags=['Book'])
def get_user_by_publisher_id(publisher_id: int, db: Session = Depends(get_db)):
    return get_resource_generic(db, Book, Book.publisher_id == publisher_id)

@by_attribute.get("/book/isbn={isbn}", tags=['Book'])
def get_user_by_isbn(isbn: str, db: Session = Depends(get_db)):
    return get_resource_generic(db, Book, Book.isbn == isbn)


# todo: Check the method below (still under development)

# @by_attribute.get("/book/publisher_name/{publisher_name}", tags=['book'])
# def get_book_by_publisher_name(publis her_name: str, db: Session = Depends(get_db)):
#     return db.query(Book).filter(Book.editorial_id == db.query(Publisher).filter(Publisher.nombre == publisher_name).first().id).all()

# # todo: Check if I can improve this query...
# @by_attribute.get("/book/author_id/{author_id}", tags=['book'])
# def get_books_by_author(author_id: int, db: Session = Depends(get_db)):
#     autor = db.query(Author).filter(Author.id == author_id).first()
#     if autor is None:
#         raise HTTPException(status_code=404, detail="Author not found")
#     return autor.libros

# # todo: penchs
# # todo: check for all the books on the LibroBiblioteca table!!!
# @by_attribute.get('/book/library/{library_id}', tags=['book'])
# def get_all_books_in_library(library_id: int, db: Session = Depends(get_db)):
#     # Ensure the library exists first
#     library_exists = db.query(Library).filter(Library.id == library_id).first()
#     if library_exists is None:
#         raise HTTPException(status_code=404, detail="Library not found")

#     # Query for all entries (including duplicates) in libro_biblioteca for this library
#     # This assumes your LibroBiblioteca model has 'libro_id' and 'biblioteca_id' foreign keys
#     libro_biblioteca_entries = db.query(LibroBiblioteca).filter(LibroBiblioteca.biblioteca_id == library_id).all()

#     if not libro_biblioteca_entries:
#         return []

#     # Now, fetch each book using the libro_id found in libro_biblioteca_entries
#     books = [db.query(Book).filter(Book.id == entry.libro_id).first() for entry in libro_biblioteca_entries]

#     return books
