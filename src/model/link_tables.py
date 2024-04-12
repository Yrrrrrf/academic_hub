#
# * This file is not being used in the current version of the project.
# * Old file with some possible features that could be implemented in the future...

# from fastapi import Depends, HTTPException
# from sqlalchemy import Column, ForeignKey, Integer
# from sqlalchemy.orm import Session

# from src.database import Base, get_db_library, get_resource_generic
# from routes.library import by_attribute



# # libro_autor = Table('libro_autor', Base.metadata,
# #     Column('libro_id', ForeignKey('libro.id'), primary_key=True),
# #     Column('autor_id', ForeignKey('autor.id'), primary_key=True)
# # )

# # libro_tema = Table('libro_tema', Base.metadata,
# #     Column('libro_id', ForeignKey('libro.id'), primary_key=True),
# #     Column('tema_id', ForeignKey('tema.id'), primary_key=True)
# # )

# # libro_biblioteca = Table('libro_biblioteca', Base.metadata,
# #     Column('libro_id', ForeignKey('libro.id'), primary_key=True),
# #     Column('biblioteca_id', ForeignKey('biblioteca.id'), primary_key=True)
# # )


# class BookAuthor(Base):
#     __tablename__ = "book_author"
#     __table_args__ = {"schema": "library_management"}

#     book_id = Column(Integer, ForeignKey('book.id'), primary_key=True)
#     author_id = Column(Integer, ForeignKey('author.id'), primary_key=True)

# # @by_attribute.get("/book/author_id/{author_id}", tags=['book'])
# # def get_books_by_author(author_id: int, db: Session = Depends(get_db_library)):
# #     autor = db.query(Author).filter(Author.id == author_id).first()
# #     if autor is None:
# #         raise HTTPException(status_code=404, detail="Author not found")
# #     return autor.libros


# class BookTopic(Base):
#     __tablename__ = "libro_topic"
#     __table_args__ = {"schema": "library_management"}

#     book_id = Column(Integer, ForeignKey('book.id'), primary_key=True)
#     topic_id = Column(Integer, ForeignKey('topic.id'), primary_key=True)  


# class BookLibrary(Base):
#     __tablename__ = "libro_library"
#     __table_args__ = {"schema": "library_management"}

#     book_serie_id = Column(Integer, primary_key=True)
#     book_id = Column(Integer, ForeignKey('book.id'), primary_key=True)
#     library_id = Column(Integer, ForeignKey('library.id'), primary_key=True)


# @by_attribute.get('/book/library={library_id}')
# def get_books_by_library(library_id: int, db: Session = Depends(get_db_library)):
#     library = db.query(BookLibrary).filter(BookLibrary.library_id == library_id).all()
#     # PRINT THE TOTAL NUMBER OF BOOKS IN THE LIBRARY
#     # print(len(library))


#     # impl a view that returns the total number of books in each library
#     # print the total of books in each library
#     # library = db.query(BookLibrary).all()

#     # # do the same as above in a for loop
#     # for i in range(1, 6):
#     #     count = 0
#     #     for j in library:
#     #         if j.biblioteca_id == i:
#     #             count += 1
#     #     print(count)

#     # if library is None:
#     #     raise HTTPException(status_code=404, detail="Library not found")
#     return library
