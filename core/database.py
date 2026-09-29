from collections.abc import Generator
import os

from sqlalchemy import inspect, text
from sqlmodel import Session, SQLModel, create_engine

from elbicho.models import User

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://osuna:admin123@localhost:5432/osunadb",
)
engine_kwargs = {"echo": False}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, **engine_kwargs)
SQLModel.metadata.create_all(engine)


def migrate_user_columns() -> None:
    existing_columns = {
        column["name"] for column in inspect(engine).get_columns("user")
    }
    new_columns = {
        "first_name": "VARCHAR NOT NULL DEFAULT ''",
        "last_name": "VARCHAR",
        "phone": "VARCHAR",
    }

    with engine.begin() as connection:
        for column_name, column_definition in new_columns.items():
            if column_name not in existing_columns:
                connection.execute(
                    text(
                        f'ALTER TABLE "user" ADD COLUMN {column_name} '
                        f"{column_definition}"
                    )
                )


migrate_user_columns()


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session