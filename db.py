from datetime import date, timedelta
from pathlib import Path
from typing import Dict, Optional, Union, List

import sqlalchemy
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
    if dialect == "sqlite":
        proj = str(Path(__file__).resolve().parent)
        url = f"sqlite:////{proj}/sample.db"
    return sqlalchemy.create_engine(url, echo=echo)


def initialize(engine) -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def create_session(engine):
    return sessionmaker(bind=engine)()


def update(engine, user_id, request_body: Dict[str, str], day=date):
    session = create_session(engine)
    registerd_data = (
        session.query(Language)
        .filter_by(user_id=user_id, lang=request_body["language"])
        .first()
    )

    if registerd_data:
        registerd_data.work_time = registerd_data.work_time + request_body["work_time"]
    else:
        work_time = Language(user_id=user_id, lang=request_body["language"], day=day)
        work_time.work_time = request_body["work_time"]
        session.add(work_time)

    session.commit()


def get_recent_week(engine, user_id):
    session = create_session(engine)
    one_week_ago = date.today() - timedelta(days=6)
    data = (
        session.query(Language)
        .filter(
            user_id == user_id,
            Language.day >= one_week_ago,
        )
        .order_by(Language.day)
    )

    seven_days: List[Dict[str, Union[str, float]]] = [{} for _ in range(7)]
    for d in data:
        seven_days[(d.day - one_week_ago).days][d.lang] = d.work_time
    return seven_days
