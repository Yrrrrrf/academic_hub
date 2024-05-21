from sqlalchemy import *

from src.api.database import *


SchemaBaseModel, IDBaseModel, NamedBaseModel = base_model(schema='library_management')


for model in [
    'Author', 
    'Publisher', 
    'Topic'
    ]:
    exec(f'class {model}(NamedBaseModel): pass')

class Book(NamedBaseModel):
    publisher_id = Column(Integer, ForeignKey('library_management.publisher.id'))
    isbn = Column(String(13))

class BookAuthor(SchemaBaseModel):
    book_id = Column(Integer, ForeignKey('library_management.book.id'), primary_key=True)
    author_id = Column(Integer, ForeignKey('library_management.author.id'), primary_key=True)

class BookTopic(SchemaBaseModel):
    book_id = Column(Integer, ForeignKey('library_management.book.id'), primary_key=True)
    topic_id = Column(Integer, ForeignKey('library_management.topic.id'), primary_key=True)

class BookLibrary(SchemaBaseModel):
    book_series_id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('library_management.book.id'))
    library_id = Column(Integer, ForeignKey('library_management.library.id'))

class Loan(IDBaseModel):
    student_id = Column(Integer, ForeignKey('school_management.student.id'))
    book_library_id = Column(Integer, ForeignKey('library_management.book_library.book_series_id'))
    loan_date = Column(Date)
    return_date = Column(Date)


lib_sql_classes: List[Type[Base]] = get_classes_from_globals(globals())  # type: ignore
lib_pydantic_classes = [create_pydantic_model(sql_class, BaseModel) for sql_class in lib_sql_classes]
