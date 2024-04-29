from sqlalchemy import Column, String

from src.database import *


SchemaBaseModel, IDBaseModel, NamedBaseModel = base_model(schema='general_dt')


class GeneralUser(NamedBaseModel):
    user_type = Column(String(50), index=True, nullable=False)
    # academic_members = relationship("AcademicMember", back_populates="user", cascade="all, delete")


general_classes: list = [obj for _, obj in globals().items() if isinstance(obj, type) and obj.__module__ == __name__]

print(f"\033[0;30;43mACADEMIC HUB - General\033[m")
[print(f"\t\033[3m{gen_c.__name__}\033[m") for gen_c in general_classes]
