# from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, Numeric
# from src.database import base_model


# ID_BaseModel, Named_BaseModel = base_model(schema='school_management')

# class School(Named_BaseModel):
#     __tablename__ = 'school'

# class Instructor(Named_BaseModel):
#     __tablename__ = 'instructor'

# class Subject(Named_BaseModel):
#     __tablename__ = 'subject'

# class AcademicPeriod(Named_BaseModel):
#     __tablename__ = 'academic_period'

# class ExamType(Named_BaseModel):
#     __tablename__ = 'exam_type'

# class Student(ID_BaseModel):
#     __tablename__ = 'student'

#     # todo: check if this is correct! Declaring again the id column...
#     id = Column(Integer, ForeignKey('general_dt.general_user.id'), primary_key=True)
#     program_id = Column(Integer, ForeignKey('school_management.program.id'), nullable=False)
#     # program = relationship("Program", back_populates="students")

# class Program(Named_BaseModel):
#     __tablename__ = 'program'
#     school_id = Column(Integer, ForeignKey('school_management.school.id'), nullable=False)
#     # school = relationship("School", back_populates="programs")

# class ClassGroup(ID_BaseModel):
#     __tablename__ = 'class_group'
    
#     instructor_id = Column(Integer, ForeignKey('school_management.instructor.id'), nullable=False)
#     subject_id = Column(Integer, ForeignKey('school_management.subject.id'), nullable=False)
#     period_id = Column(Integer, ForeignKey('school_management.academic_period.id'), nullable=False)
#     # instructor = relationship("Instructor")
#     # subject = relationship("Subject")
#     # academic_period = relationship("AcademicPeriod")

# class StudentEnrollment(ID_BaseModel):
#     __tablename__ = 'student_enrollment'
    
#     student_id = Column(Integer, ForeignKey('school_management.student.id'), nullable=False)
#     class_group_id = Column(Integer, ForeignKey('school_management.class_group.id'), nullable=False)
#     enrollment_date = Column(Date, nullable=False)

# class Grade(ID_BaseModel):
#     __tablename__ = 'grade'
    
#     student_enrollment_id = Column(Integer, ForeignKey('school_management.student_enrollment.id'), nullable=False)
#     exam_type_id = Column(Integer, ForeignKey('school_management.exam_type.id'), nullable=False)
#     grade = Column(Numeric, nullable=False)
#     grading_date = Column(Date, nullable=False)

# class Attendance(ID_BaseModel):
#     __tablename__ = 'attendance'
    
#     student_enrollment_id = Column(Integer, ForeignKey('school_management.student_enrollment.id'), nullable=False)
#     date = Column(Date, nullable=False)
#     status = Column(String(10), nullable=False)

# class ClassSchedule(ID_BaseModel):
#     __tablename__ = 'class_schedule'
    
#     class_group_id = Column(Integer, ForeignKey('school_management.class_group.id'), nullable=False)
#     day_of_week = Column(String(10), nullable=False)
#     start_time = Column(Time, nullable=False)
#     end_time = Column(Time, nullable=False)
