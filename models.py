from datetime import datetime
from typing import Dict, Union

from sqlalchemy import Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column

Base = declarative_base()


class User(Base):
    __tablename__ = "items"
    id = Column(String(64), nullable=False, primary_key=True)

    @property
    def serialize(self) -> Dict[str, str]:
        return {"id": self.id}


class Language(Base):
    __talbename__ = "languages"
    user_id = Column(String(64), nullable=False, primary_key=True)
    lang = Column(String(32), nullable=False, primary_key=True)
    work_time = Column(Integer, nullalbe=False)
    day = Column(Date, nullalbe=False, primary_key=True)

    @property
    def serialize(self) -> Dict[str, Union[str, str, datetime]]:
        return {
            "user_id": self.id,
            "language": self.lang,
            "work_time": self.work_time,
            "day": self.day,
        }
