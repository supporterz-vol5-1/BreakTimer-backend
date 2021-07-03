from datetime import datetime
from typing import Dict, Union

from sqlalchemy import REAL, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(String(64), nullable=False, primary_key=True)

    @property
    def serialize(self) -> Dict[str, str]:
        return {"id": self.id}


class WorkTime(Base):
    __tablename__ = "work_times"
    user_id = Column(String(64), nullable=False, primary_key=True)
    filetype= Column(String(32), nullable=False, primary_key=True)
    work_time = Column(REAL, nullable=False)
    day = Column(Date, nullable=False, primary_key=True)

    @property
    def serialize(self) -> Dict[str, Union[str, float, datetime]]:
        return {
            "user_id": self.id,
            "filetype": self.lang,
            "work_time": self.work_time,
            "day": self.day,
        }
