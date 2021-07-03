from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Dict, Union

from sqlalchemy import REAL, Date, String
from sqlalchemy.orm import Mapped, declarative_base, registry
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.sql.schema import Column, Table
from sqlalchemy.util.compat import dataclass_fields

mapper_registry = registry()


@mapper_registry.mapped
@dataclass
class User:
    __table__ = Table(
        "users",
        mapper_registry.metadata,
        Column("name", String(64), nullable=False, primary_key=True),
        Column("token", String(128), nullable=False),
    )
    name: str
    token: str


#
# class User(Base):
#     __tablename__ = "users"
#     name: Mapped[str] = Mapped._special_method(
#         Column(String(64), nullable=False, primary_key=True)
#     )
#     token: Mapped[str] = Mapped._special_method(
#         Column(String(128), nullable=False),
#     )
#
#     def __init__(self, name: str, token: str) -> None:
#         self.name = name
#         self.token = token
#
#     @property
#     def serialize(self) -> Dict[str, str]:
#         return {
#             "id": self.name,
#             "token": self.token,
#         }
#
#


@mapper_registry.mapped
@dataclass
class WorkTime:
    __table__ = Table(
        "work_times",
        mapper_registry.metadata,
        Column("user_name", String(64), nullable=False, primary_key=True),
        Column("filetype", String(32), nullable=False, primary_key=True),
        Column("work_time", REAL, nullable=False),
        Column("day", Date, nullable=False, primary_key=True),
    )
    user_name: str
    filetype: str
    work_time: float
    day: date


# class WorkTime(Base):
#     __tablename__ = "work_times"
#     user_name: Mapped[str] = Mapped._special_method(
#         Column(String(64), nullable=False, primary_key=True)
#     )
#     filetype: Mapped[str] = Mapped._special_method(
#         Column(String(32), nullable=False, primary_key=True)
#     )
#     work_time: Mapped[float] = Mapped._special_method(Column(REAL, nullable=False))
#     day: Mapped[date] = Mapped._special_method(
#         Column(Date, nullable=False, primary_key=True)
#     )
#
#     def __init__(
#         self, user_name: str, filetype: str, work_time: float, day: date
#     ) -> None:
#         self.user_name = user_name
#         self.filetype = filetype
#         self.work_time = work_time
#         self.day = day
#
#     @property
#     def serialize(self) -> Dict[str, Union[str, float, date]]:
#         return {
#             "user_name": self.user_name,
#             "filetype": self.filetype,
#             "work_time": self.work_time,
#             "day": self.day,
#         }
#


@mapper_registry.mapped
@dataclass
class Work:
    __table__ = Table(
        "works",
        mapper_registry.metadata,
        Column("user_name", String(64), nullable=False, primary_key=True),
        Column("filetype", String(32), nullable=False, primary_key=True),
        Column("start", Date, nullable=False),
    )
    user_name: str
    filetype: str
    start: datetime


#
# class Work(Base):
#     __tablename__ = "works"
#     user_name: Mapped[str] = Mapped._special_methods(
#         Column(String(64), nullable=False, primary_key=True)
#     )
#     filetype: Mapped[str] = Mapped._special_methods(
#         Column(String(32), nullable=False, primary_key=True)
#     )
#     start: Mapped[datetime] = Mapped._special_methods(Column(Date, nullable=False))
#
#     def __init__(self, user_name: str, filetype: str, start: datetime) -> None:
#         self.user_name = user_name
#         self.filetype = filetype
#         self.start = start
#
#     @property
#     def serialize(self) -> Dict[str, Union[str, datetime]]:
#         return {
#             "user_name": self.user_name,
#             "filetype": self.filetype,
#             "start": self.start,
#         }
