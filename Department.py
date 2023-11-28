from orm_base import Base
from sqlalchemy import Column, Integer, UniqueConstraint, Identity
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


class Department(Base):
    """
    A part of a large organization that deals in a particular area of work within said organization. Such as the CECS
    Department in CSULB or a finance department in a corporate entity.
    """

    __tablename__ = "departments"   # Table namef

    # Columnsb
    name: Mapped[str] = mapped_column('name', String(50), nullable=False)
    abbreviation: Mapped[str] = mapped_column('abbreviation', String(6), nullable=False, primary_key=True)
    chairName: Mapped[str] = mapped_column('chair_name', String(80), nullable=False)
    building: Mapped[str] = mapped_column('building', String(10), nullable=False)
    office: Mapped[int] = mapped_column('office', Integer, nullable=False)
    description: Mapped[str] = mapped_column('description', String(80), nullable=False)

    courses: Mapped[List["Course"]] = relationship(back_populates="department")

    # Uniqueness constraints
    __table_args__ = (UniqueConstraint('name', name='department_uk_01'), UniqueConstraint('chair_name',
                        name='department_uk_02'), UniqueConstraint('building', 'office',
                        name='department_uk_03'), UniqueConstraint('description', name='department_uk_04'))

    def __init__(self, name: str, abbreviation: str, chair_name: str, building: str, office: int, description: str):

        self.name = name
        self.abbreviation = abbreviation
        self.chairName = chair_name
        self.building = building
        self.office = office
        self.description = description

    def add_course(self, course):
        if course not in self.courses:
            self.courses.add(course)

    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)

    def get_courses(self):
        return self.courses

    def __str__(self):
        return f'Name: {self.name}\n   Abbreviation: {self.abbreviation}\n   Chair Name: {self.chairName}' \
               f'\n   Building: {self.building}\n   Office: {self.office}\n   Description: {self.description}'