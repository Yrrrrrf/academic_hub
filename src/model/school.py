from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, Numeric
from src.database import base_model


SchemaBaseModel, IDBaseModel, NamedBaseModel = base_model(schema='school_management')


# * For each model, create a class that inherits from the appropriate base class
for model in [
    'School', 
    'Instructor', 
    'Subject', 
    'AcademicPeriod', 
    'ExamType'
    'Classroom',
    ]:
    exec(f'class {model}(NamedBaseModel): pass')

class Student(IDBaseModel):
    # todo: check if this is correct! Declaring again the id column...
    id = Column(Integer, ForeignKey('general_dt.general_user.id'), primary_key=True)
    program_id = Column(Integer, ForeignKey('school_management.program.id'), nullable=False)
    # program = relationship("Program", back_populates="students")

class Program(NamedBaseModel):
    school_id = Column(Integer, ForeignKey('school_management.school.id'), nullable=False)
    # school = relationship("School", back_populates="programs")

class ClassGroup(IDBaseModel):
    instructor_id = Column(Integer, ForeignKey('school_management.instructor.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('school_management.subject.id'), nullable=False)
    period_id = Column(Integer, ForeignKey('school_management.academic_period.id'), nullable=False)
    # instructor = relationship("Instructor")
    # subject = relationship("Subject")
    # academic_period = relationship("AcademicPeriod")

class StudentEnrollment(IDBaseModel):
    student_id = Column(Integer, ForeignKey('school_management.student.id'), nullable=False)
    # todo: CHANGE THE class_group_id TO BE A STRING!!!
    class_group_id = Column(Integer, ForeignKey('school_management.class_group.id'), nullable=False)
    enrollment_date = Column(Date, nullable=False)

class Grade(IDBaseModel):
    student_enrollment_id = Column(Integer, ForeignKey('school_management.student_enrollment.id'), nullable=False)
    exam_type_id = Column(Integer, ForeignKey('school_management.exam_type.id'), nullable=False)
    grade = Column(Numeric, nullable=False)
    grading_date = Column(Date, nullable=False)

class Attendance(IDBaseModel):
    student_enrollment_id = Column(Integer, ForeignKey('school_management.student_enrollment.id'), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String(10), nullable=False)

class ClassSchedule(IDBaseModel):
    class_group_id = Column(Integer, ForeignKey('school_management.class_group.id'), nullable=False)
    classroom_id = Column(Integer, ForeignKey('school_management.classroom.id'), nullable=False)
    day_of_week = Column(String(10), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)


# * Look for all the classes defined in this module and store them in a list
# * then we can use them to create the routes for the API for each model
school_classes: list = [obj for _, obj in globals().items() if isinstance(obj, type) and obj.__module__ == __name__]

print(f"\033[0;30;43mACADEMIC HUB - School Management\033[m")
[print(f"\t\033[3m{sch_c.__name__}\033[m") for sch_c in school_classes]
