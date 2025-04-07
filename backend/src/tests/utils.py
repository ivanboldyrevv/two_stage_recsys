from database import Database

import pytest


@pytest.fixture()
def db():
    db = Database("postgresql+psycopg2://admin:admin@localhost:5432/test_db")
    db.create_database()
    yield db
    db.drop_all()


def insert(*args) -> None:
    db = Database("postgresql+psycopg2://admin:admin@localhost:5432/test_db")

    with db.session() as sess:
        sess.add_all([*args])
        sess.commit()
