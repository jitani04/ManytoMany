from orm_base import Base
from sqlalchemy import Column, Integer, UniqueConstraint, Identity
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from Enrollment import Enrollment

class Student(Base):
    """An individual who is currently enrolled or has explicitly stated an intent
    to enroll in one or more classes.  Said individuals may or may not be admitted
    to the university.  For instance, open enrollment students have not (yet) been
    admitted to the university, but they are still students."""
    __tablename__ = "students"  # Give SQLAlchemy tht name of the table.
    studentId: Mapped[int] = mapped_column('student_id', Integer, Identity(start=1, cycle=True),
                                           nullable=False, primary_key=True)
    lastName: Mapped[str] = mapped_column('last_name', String(50), nullable=False)
    firstName: Mapped[str] = mapped_column('first_name', String(50), nullable=False)
    eMail: Mapped[str] = mapped_column('e_mail', String(80), nullable=False)

    sections: Mapped[List["Enrollment"]] = relationship(back_populates="student", cascade="all, save-update, delete-orphan")

    # __table_args__ can best be viewed as directives that we ask SQLAlchemy to
    # send to the database.  In this case, that we want two separate uniqueness
    # constraints (ccandidate keys).
    __table_args__ = (UniqueConstraint("last_name", "first_name", name="students_uk_01"),
                      UniqueConstraint("e_mail", name="students_uk_02"))

    def __init__(self, last_name: str, first_name: str, e_mail: str):
        self.lastName = last_name
        self.firstName = first_name
        self.eMail = e_mail

    def add_section(self, section):
        for next_section in self.sections:
            if next_section.section == section:
                return

        enrollment = Enrollment(section, self)

    def remove_section(self, section):
        for next_section in self.sections:
            if next_section.section == section:
                self.sections.remove(next_section)
                return

    def __str__(self):
        return f"Student id: {self.studentId} name: {self.lastName}, {self.firstName}\nEmail Address: {self.eMail}"
