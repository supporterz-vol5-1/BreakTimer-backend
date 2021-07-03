from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Union

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import Base, WorkTime


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


def update(engine, user_id, request_body: Dict[str, str], day=date):
    session = create_session(engine)
    registerd_data = (
        session.query(WorkTime)
        .filter_by(user_id=user_id, lang=request_body["filetype"])
        .first()
    )

    if registerd_data:
        registerd_data.work_time = registerd_data.work_time + request_body["work_time"]
    else:
        work_time = WorkTime(
            user_id=user_id,
            lang=request_body["filetype"],
            work_time=request_body["work_time"],
            day=day,
        )
        session.add(work_time)

    session.commit()


def get_recent_week(engine, user_id):
    session = create_session(engine)
    one_week_ago = date.today() - timedelta(days=6)
    data = (
        session.query(WorkTime)
        .filter(
            user_id == user_id,
            WorkTime.day >= one_week_ago,
        )
        .order_by(WorkTime.day)
    )

    seven_days: List[Dict[str, Union[str, float]]] = [{} for _ in range(7)]
    for d in data:
        seven_days[(d.day - one_week_ago).days][d.lang] = d.work_time
    return seven_days
