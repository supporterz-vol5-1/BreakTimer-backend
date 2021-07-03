from datetime import date, datetime
from typing import Dict, Union

from sqlalchemy import REAL, Date, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.sql.schema import Column


class Base(metaclass=DeclarativeMeta):
    __abstruct__ = True


class User(Base):
    __tablename__ = "users"
    name: Mapped[str] = Mapped._special_method(
        Column(String(64), nullable=False, primary_key=True)
    )
    token: Mapped[str] = Mapped._special_method(
        Column(String(128), nullable=False),
    )

    def __init__(self, name: str, token: str) -> None:
        self.name = name
        self.token = token

    @property
    def serialize(self) -> Dict[str, str]:
        return {
            "id": self.name,
            "token": self.token,
        }


class WorkTime(Base):
    __tablename__ = "work_times"
    user_name: Mapped[str] = Mapped._special_method(
        Column(String(64), nullable=False, primary_key=True)
    )
    filetype: Mapped[str] = Mapped._special_method(
        Column(String(32), nullable=False, primary_key=True)
    )
    work_time: Mapped[float] = Mapped._special_method(Column(REAL, nullable=False))
    day: Mapped[date] = Mapped._special_method(
        Column(Date, nullable=False, primary_key=True)
    )

    def __init__(
        self, user_name: str, filetype: str, work_time: float, day: date
    ) -> None:
        self.user_name = user_name
        self.filetype = filetype
        self.work_time = work_time
        self.day = day

    @property
    def serialize(self) -> Dict[str, Union[str, float, date]]:
        return {
            "user_name": self.user_name,
            "filetype": self.filetype,
            "work_time": self.work_time,
            "day": self.day,
        }


class Work(Base):
    __tablename__ = "works"
    user_name: Mapped[str] = Mapped._special_methods(
        Column(String(64), nullable=False, primary_key=True)
    )
    filetype: Mapped[str] = Mapped._special_methods(
        Column(String(32), nullable=False, primary_key=True)
    )
    start: Mapped[datetime] = Mapped._special_methods(Column(Date, nullable=False))

    def __init__(self, user_name: str, filetype: str, start: datetime) -> None:
        self.user_name = user_name
        self.filetype = filetype
        self.start = start

    @property
    def serialize(self) -> Dict[str, Union[str, datetime]]:
        return {
            "user_name": self.user_name,
            "filetype": self.filetype,
            "start": self.start,
        }
