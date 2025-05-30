from datetime import datetime
from uuid import uuid4

from models import Transaction, Article, Customer
from .utils import db, insert
from repositories import TransactionRepository
from services import TransactionService


database = db


def test_get_transactions(database):
    transaction_uuid = uuid4()
    t_dat = datetime.now().date()
    article_uuid = uuid4()
    customer_uuid = uuid4()

    test_article = Article(article_uuid=article_uuid)
    test_customer = Customer(customer_uuid=customer_uuid)
    test_transaction = Transaction(
        transaction_uuid=transaction_uuid,
        t_dat=t_dat,
        customer_uuid=customer_uuid,
        article_uuid=article_uuid
    )

    insert(test_transaction, test_article, test_customer)
    service = TransactionService(TransactionRepository(database.session))

    result = service.get_customer_transactions(customer_uuid)[0]

    assert transaction_uuid == result.transaction_uuid
    assert str(t_dat) == str(result.t_dat.strftime("%Y-%m-%d"))
    assert article_uuid == result.article_uuid
    assert customer_uuid == result.customer_uuid


def test_insert_transactions(database):
    today = datetime.now().strftime("%Y-%m-%d")
    article_uuid = uuid4()
    customer_uuid = uuid4()

    test_article = Article(article_uuid=article_uuid)
    test_customer = Customer(customer_uuid=customer_uuid)

    insert(test_article, test_customer)

    service = TransactionService(TransactionRepository(database.session))
    result = service.insert_transaction(customer_uuid, article_uuid)

    assert today == result.t_dat.strftime("%Y-%m-%d")
    assert article_uuid == result.article_uuid
    assert customer_uuid == result.customer_uuid
