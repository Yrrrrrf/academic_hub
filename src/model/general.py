# from fastapi import Depends
# from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import Session

# from src.database import Base, get_resource_generic, get_db_school
# from src.routes.library_routes import by_attribute


# class GeneralUser(Base):
#     __tablename__ = "general_user"
#     __table_args__ = {"schema": "general_dt"}

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255), index=True)
#     user_type = Column(String(50), index=True, nullable=False)


# @by_attribute.get("/g_users/dt/", tags=['General'])
# def get_columns():
#     return [c.name for c in GeneralUser.__table__.columns]

# @by_attribute.get("/g_users/", tags=['General'])
# def get_all_users(db: Session = Depends(get_db_school)):
#     return get_resource_generic(db, GeneralUser)