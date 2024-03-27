from fastapi import Depends

from sqlalchemy.orm import Session
from sqlalchemy import Column, ForeignKey, Integer, String, text

from src.database import Base, get_db, get_resource_generic
from src.routes.library_routes import by_attribute


class Loan(Base):
    __tablename__ = "loan"
    
    __table_args__ = {"schema": "library_management"}


    id = Column(Integer, primary_key=True, index=True)

    academic_member_id = Column(Integer, ForeignKey('academic_member.id'), index=True)  # REFERENCES usuario(id)
    book_library_id = Column(Integer, ForeignKey('book_library.book_series_id'), index=True)  # REFERENCES libro_biblioteca(libro_no_serie_id)
    loan_date = Column(String(255), index=True)
    return_date = Column(String(255), index=True, nullable=True)


#  get_operations(Loan, by_attribute)
@by_attribute.get("/loans/dt/", tags=['Loan'])
def get_columns():
    return [c.name for c in Loan.__table__.columns]

@by_attribute.get("/loans/", tags=['Loan'])
def get_all_loans(db: Session = Depends(get_db)):
    return get_resource_generic(db, Loan)

@by_attribute.get("/loan/id={id}", tags=['Loan'])
def get_loan_by_id(id: int, db: Session = Depends(get_db)):
    return get_resource_generic(db, Loan, Loan.id == id)

@by_attribute.get("/loan/academic_member_id={academic_member_id}", tags=['Loan'])
def get_loan_by_academic_member_id(academic_member_id: int, db: Session = Depends(get_db)):
    return get_resource_generic(db, Loan, Loan.academic_member_id == academic_member_id)

@by_attribute.get("/loan/book_library_id={book_id}", tags=['Loan'])
def get_loan_by_book_id(book_id: int, db: Session = Depends(get_db)):
    return get_resource_generic(db, Loan, Loan.book_library_id == book_id)

@by_attribute.get("/loan/loan_date={loan_date}", tags=['Loan'])
def get_loan_by_loan_date(loan_date: str, db: Session = Depends(get_db)):
    return get_resource_generic(db, Loan, Loan.loan_date == loan_date)

@by_attribute.get("/loan/return_date={return_date}", tags=['Loan'])
def get_loan_by_return_date(return_date: str, db: Session = Depends(get_db)):
    return get_resource_generic(db, Loan, Loan.return_date == return_date)
