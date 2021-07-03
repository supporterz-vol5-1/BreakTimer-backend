from datetime import datetime
from typing import Dict, Union

from sqlalchemy import REAL, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    name = Column(String(64), nullable=False, primary_key=True)
    token = Column(String(128), nullable=False)

    @property
    def serialize(self) -> Dict[str, str]:
        return {"id": self.name, "token": self.token}


class WorkTime(Base):
    __tablename__ = "work_times"
    user_name = Column(String(64), nullable=False, primary_key=True)
    filetype = Column(String(32), nullable=False, primary_key=True)
    work_time = Column(REAL, nullable=False)
    day = Column(Date, nullable=False, primary_key=True)

    @property
    def serialize(self) -> Dict[str, Union[str, float, datetime]]:
        return {
            "user_name": self.name,
            "filetype": self.filetype,
            "work_time": self.work_time,
            "day": self.day,
        }


class Work(Base):
    __tablename__ = "works"
    user_name = Column(String(64), nullable=False, primary_key=True)
    filetype = Column(String(32), nullable=False, primary_key=True)
    start = Column(Date, nullable=False)

    @property
    def serialize(self):
        return {
            "user_name": self.user_name,
            "filetype": self.filetype,
            "start": self.start,
        }
