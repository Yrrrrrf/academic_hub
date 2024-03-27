from fastapi import Depends
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session, relationship

from src.database import Base, get_db, get_resource_generic
from src.routes.library_routes import by_attribute


class Author(Base):
    __tablename__ = "author"
    __table_args__ = {"schema": "library_management"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    # libros = relationship("Book", secondary="libro_autor", back_populates="autores")


# ? CRUD Methods ------------------------------------------------------------------------------
# * CREATE (.post)

@by_attribute.get("/authors/dt/", tags=['Author'])
def get_columns():
    return [c.name for c in Author.__table__.columns]

@by_attribute.get("/authors/", tags=['Author'])
def get_all_authors(db: Session = Depends(get_db)):
    return get_resource_generic(db, Author)

@by_attribute.get("/author/id={id}", tags=['Author'])
def get_author_by_id(id: int, db: Session = Depends(get_db)):
    return get_resource_generic(db, Author, Author.id == id)

@by_attribute.get("/author/name={name}", tags=['Author'])
def get_author_by_name(name: str, db: Session = Depends(get_db)):
    return get_resource_generic(db, Author, Author.name == name)


# * UPDATE (.put)

# # * DELETE (.delete)
# # Delete all authors
# @by_attribute.delete('/authors', tags=['author'])
# def delete_all_authors(db: Session = Depends(get_db)):
#     db.query(Author).delete()
#     db.commit()
#     return {"message": "All authors deleted successfully"}

# @by_attribute.delete('/author/id/{author_id}', tags=['author'])
# def delete_author(author_id: int, db: Session = Depends(get_db)):
#     author = db.query(Author).filter(Author.id == author_id).first()
#     db.delete(author)
#     db.commit()
#     return {"message": "Author deleted successfully"}

# @by_attribute.delete('/author/name/{author_name}', tags=['author'])
# def delete_author_by_name(author_name: str, db: Session = Depends(get_db)):
#     author = db.query(Author).filter(Author.nombre == author_name).first()
#     db.delete(author)
#     db.commit()
#     return {"message": "Author deleted successfully"}



# # create author
# @by_attribute.post('/author', tags=['author'])
# def create_author(author: Author, db: Session = Depends(get_db)):
#     db.add(author)
#     db.commit()
#     db.refresh(author)
#     return author
