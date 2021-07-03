from typing import Optional, Union

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import Base


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
    Base.metadata.create_all(bind_engine)


def create_session(engine):
    return sessionmaker(bind=engine)()
