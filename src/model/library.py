from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from src.database import base_model, Base


SchemaBaseModel, IDBaseModel, NamedBaseModel = base_model(schema='library_management')


# * For each model, create a class that inherits from the appropriate base class
for model in ['Author', 'Library', 'Publisher', 'Topic']:
    exec(f'class {model}(NamedBaseModel): pass')

class Book(NamedBaseModel):
    publisher_id = Column(Integer, ForeignKey('library_management.publisher.id'))
    ISBN = Column(String(13))

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

class AcademicMember(IDBaseModel):
    user_id = Column(Integer, ForeignKey('general_user.id', ondelete='CASCADE'))
    # user = relationship("GeneralUser", back_populates="academic_members")


class Loan(IDBaseModel):
    academic_member_id = Column(Integer, ForeignKey('library_management.academic_member.id'))
    book_library_id = Column(Integer, ForeignKey('library_management.book_library.book_series_id'))
    loan_date = Column(Date)
    return_date = Column(Date)


lib_classes = [obj for _, obj in globals().items() if isinstance(obj, type) and obj.__module__ == __name__]


print(f"\033[0;30;43mACADEMIC HUB - Library Management\033[m")
[print(f"\t\033[3m{lib_c.__name__}\033[m") for lib_c in lib_classes]
