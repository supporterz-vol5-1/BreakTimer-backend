from datetime import date, timedelta
from typing import Dict, Optional, Union

import sqlalchemy
from sqlalchemy.engine import create
from sqlalchemy.orm import sessionmaker

from models import Base, Language


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
    return sqlalchemy.create_engine(url, echo=echo)


def initialize(engine) -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def create_session(engine):
    return sessionmaker(bind=engine)()


def update(engine, user_id, request_body: Dict[str, str], day=date):
    session = create_session(engine)
    registerd_data = Language.query.filter_by(
        user_id=user_id, lang=request_body["language"]
    ).first()

    if registerd_data:
        registerd_data.work_time = registerd_data.work_time + request_body["work_time"]
    else:
        work_time = Language(user_id=user_id, lang=request_body["language"], day=day)
        work_time.work_time = request_body["work_time"]
        session.add(work_time)

    session.commit()


def get_recent_week(engine, user_id):
    one_week_ago = date.today() - timedelta(days=7)
    data = Language.query.filter(
        user_id == user_id, Language.day >= one_week_ago
    ).order_by(Language.day)

    seven_days: List[Dict[str, Union[str, float]]] = [{} for _ in range(7)]
    for d in data:
        seven_days[(d.day - one_week_ago).days][d.lang] = d.worktime
    return seven_days
