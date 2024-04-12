from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, Numeric
from src.database import base_model, Base

ID_BaseModel, Named_BaseModel = base_model(schema='library_management')


class Author(Named_BaseModel):
    __tablename__ = 'author'

class Library(Named_BaseModel):
    __tablename__ = 'library'

class Publisher(Named_BaseModel):
    __tablename__ = 'publisher'

class Topic(Named_BaseModel):
    __tablename__ = 'topic'

class Book(Named_BaseModel):
    __tablename__ = 'book'

    publisher_id = Column(Integer, ForeignKey('library_management.publisher.id'))
    ISBN = Column(String(13))
    # publisher = relationship("Publisher", back_populates="books")

class BookAuthor(Base):
    __tablename__ = 'book_author'
    __table_args__ = {'schema': 'library_management'}
    book_id = Column(Integer, ForeignKey('library_management.book.id'), primary_key=True)
    author_id = Column(Integer, ForeignKey('library_management.author.id'), primary_key=True)
    # book = relationship("Book", back_populates="authors")
    # author = relationship("Author", back_populates="books")

class BookTopic(Base):
    __tablename__ = 'book_topic'
    __table_args__ = {'schema': 'library_management'}
    book_id = Column(Integer, ForeignKey('library_management.book.id'), primary_key=True)
    topic_id = Column(Integer, ForeignKey('library_management.topic.id'), primary_key=True)

class BookLibrary(Base):
    __tablename__ = 'book_library'
    __table_args__ = {'schema': 'library_management'}
    book_series_id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('library_management.book.id'))
    library_id = Column(Integer, ForeignKey('library_management.library.id'))

class AcademicMember(ID_BaseModel):
    __tablename__ = 'academic_member'
    __table_args__ = {'schema': 'library_management'}

class Loan(ID_BaseModel):
    __tablename__ = 'loan'
    __table_args__ = {'schema': 'library_management'}
    academic_member_id = Column(Integer, ForeignKey('library_management.academic_member.id'))
    book_library_id = Column(Integer, ForeignKey('library_management.book_library.book_series_id'))
    loan_date = Column(Date)
    return_date = Column(Date)
