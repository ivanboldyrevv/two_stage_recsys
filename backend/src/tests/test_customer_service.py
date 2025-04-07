from uuid import uuid4

from database import Database
from models import Customer
from repositories import CustomerRepository
from services import CustomerService

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


def test_get_random(db):
    first_customer = uuid4()
    second_customer = uuid4()

    insert(*[Customer(customer_uuid=first_customer, age=35),
             Customer(customer_uuid=second_customer, age=35)])

    service = CustomerService(CustomerRepository(db.session))

    seen = {service.get_random_customer().customer_uuid for _ in range(30)}
    assert seen == {first_customer, second_customer}


def test_random_seed(db):
    first_customer = uuid4()
    second_customer = uuid4()

    insert(*[Customer(customer_uuid=first_customer, age=35),
             Customer(customer_uuid=second_customer, age=35)])

    service = CustomerService(CustomerRepository(db.session))

    seen = {service.get_random_customer(42).customer_uuid for _ in range(25)}
    assert len(seen) == 1
