import hashlib
import random
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Union

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import Base, User, WorkTime


def create_engine(
    dialect: str,
    password: str,
    host: str,
    username: str,
    port: Union[str, int],
    dbname: str,
    driver: str = "",
    echo: Optional[bool] = None,
):
    if driver != "":
        driver = "+" + driver
    url = f"{dialect}{driver}://{username}:{password}@{host}:{port}/{dbname}"
    if dialect == "sqlite":
        url = f"sqlite:///{str(Path(dbname).resolve())}"
    return sqlalchemy.create_engine(url, echo=echo)


def initialize(engine) -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def create_session(engine):
    return sessionmaker(bind=engine)()


def update(engine, user_name, request_body: Dict[str, str], day=date):
    session = create_session(engine)
    is_valid = bool(session.query(User).filter(User.name == user_name).first())
    if not is_valid:
        raise UserNotFoundError
    is_valid = bool(
        session.query(User)
        .filter(User.name == user_name, User.token == request_body["token"])
        .first()
    )
    if not is_valid:
        raise InvalidTokenError

    registerd_data = (
        session.query(WorkTime)
        .filter(
            WorkTime.user_name == user_name,
            WorkTime.filetype == request_body["filetype"],
        )
        .first()
    )

    if registerd_data:
        registerd_data.work_time = registerd_data.work_time + request_body["work_time"]
    else:
        work_time = WorkTime(
            user_name=user_name,
            filetype=request_body["filetype"],
            work_time=request_body["work_time"],
            day=day,
        )
        session.add(work_time)

    session.commit()


class UserNotFoundError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


def register_user(engine, user_name: str) -> Optional[str]:
    session = create_session(engine)
    if session.query(User).filter(User.name == user_name).first():
        return None
    else:
        now = datetime.now().strftime("%y%m%d%H%M%S")
        s = list(user_name + now)
        random.shuffle(s)
        shuffled = "".join(s)
        hashed = hashlib.md5(shuffled.encode()).hexdigest()
        user = User(name=user_name, token=hashed)
        session.add(user)
        session.commit()
        return hashed


def get_recent_week(engine, user_name):
    session = create_session(engine)
    one_week_ago = date.today() - timedelta(days=6)
    data = (
        session.query(WorkTime)
        .filter(
            WorkTime.user_name == user_name,
            WorkTime.day >= one_week_ago,
        )
        .order_by(WorkTime.day)
    )

    seven_days: List[Dict[str, Union[str, float]]] = [{} for _ in range(7)]
    for d in data:
        seven_days[(d.day - one_week_ago).days][d.filetype] = d.work_time
    return seven_days
