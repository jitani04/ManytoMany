from orm_base import Base
from sqlalchemy import Integer, UniqueConstraint, ForeignKey, ForeignKeyConstraint
from sqlalchemy import String, Integer, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Identity
from datetime import time
from Course import Course
from Enrollment import Enrollment
from typing import List


class Section(Base):
    """
    A class in where students are enrolled in to learn a particular subject via meeting as a group, learning, working,
    and getting tested.
    """

    __tablename__ = "sections"
    section_id: Mapped[int] = mapped_column('section_id', Integer, Identity(start=1, cycle=True), nullable=False, primary_key=True)
    departmentAbbreviation: Mapped[str] = mapped_column('department_abbreviation', String(10), nullable=False)
    courseNumber: Mapped[int] = mapped_column('course_number', Integer, nullable=False)
    sectionNumber: Mapped[int] = mapped_column('section_number', Integer, nullable=False)
    semester: Mapped[str] = mapped_column('semester', String(10), nullable=False)
    sectionYear: Mapped[int] = mapped_column('section_year', Integer, nullable=False)
    building: Mapped[str] = mapped_column('building', String(6), nullable=False)
    room: Mapped[int] = mapped_column('room', Integer, nullable=False)
    schedule: Mapped[str] = mapped_column('schedule', String(6), nullable=False)
    startTime: Mapped[time] = mapped_column('start_time', Time, nullable=False)
    instructor: Mapped[str] = mapped_column('instructor', String(80), nullable=False)

    course: Mapped["Course"] = relationship(back_populates="sections")
    students: Mapped[List["Enrollment"]] = relationship(back_populates="section", cascade="all, save-update, delete-orphan")

    __table_args__ = (UniqueConstraint('section_year', 'semester', 'schedule', 'start_time', 'building', 'room',
                                       name='sections_uk_01'), UniqueConstraint('section_year', 'semester', 'schedule',
                                       'start_time', 'instructor', name='sections_uk_02'), UniqueConstraint(
                                       'department_abbreviation', 'course_number', 'section_number', 'semester',
                                       'section_year', name='sections_uk_03'),ForeignKeyConstraint([
                                       departmentAbbreviation, courseNumber], [Course.departmentAbbreviation,
                                       Course.courseNumber]))

    def __init__(self, course: Course, sectionNumber: int, semester: str, sectionYear: int, building: str, room: int, schedule: str, startTime: time, instructor: str):
        self.set_course(course)
        self.sectionNumber = sectionNumber
        self.semester = semester
        self.sectionYear = sectionYear
        self.building = building
        self.room = room
        self.schedule = schedule
        self.startTime = startTime
        self.instructor = instructor

    def set_course(self, course: Course):
        """
        Initializes values that were migrated.
        :param course: The new course for the section.
        :return: None
        """
        self.course = course
        self.departmentAbbreviation = course.departmentAbbreviation
        self.courseNumber = course.courseNumber

    def add_student(self, student):
        for next_student in self.students:
            if next_student.student == student:
                return
        enrollment = Enrollment(self, student)

    def remove_student(self, student):
        for next_student in self.students:
            if next_student.student == student:
                self.students.remove(next_student)
                return

    def __str__(self):
        return f"Department Abbreviation: {self.departmentAbbreviation}\n" \
               f"Course Number: {self.courseNumber}\n" \
               f"Section Number: {self.sectionNumber}\n" \
               f"Semester: {self.semester}\n" \
               f"Section Year: {self.sectionYear}\n" \
               f"Building: {self.building}\n" \
               f"Room: {self.room}\n" \
               f"Schedule: {self.schedule}\n" \
               f"Start Time: {self.startTime}\n" \
               f"Instructor: {self.instructor}\n"
