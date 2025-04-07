from uuid import uuid4

from .utils import db, insert
from models import Customer
from repositories import CustomerRepository
from services import CustomerService


database = db


def test_get_random(database):
    first_customer = uuid4()
    second_customer = uuid4()

    insert(*[Customer(customer_uuid=first_customer, age=35),
             Customer(customer_uuid=second_customer, age=35)])

    service = CustomerService(CustomerRepository(database.session))

    seen = {service.get_random_customer().customer_uuid for _ in range(30)}
    assert seen == {first_customer, second_customer}


def test_random_seed(database):
    first_customer = uuid4()
    second_customer = uuid4()

    insert(*[Customer(customer_uuid=first_customer, age=35),
             Customer(customer_uuid=second_customer, age=35)])

    service = CustomerService(CustomerRepository(database.session))

    seen = {service.get_random_customer(42).customer_uuid for _ in range(25)}
    assert len(seen) == 1
