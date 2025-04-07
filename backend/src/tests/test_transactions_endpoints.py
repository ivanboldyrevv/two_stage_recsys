from uuid import uuid4
from unittest import mock

from datetime import date

import pytest
from fastapi.testclient import TestClient

from models import Transaction
from services import TransactionService
from main import app


@pytest.fixture()
def client():
    yield TestClient(app)


def test_get_transactions(client):
    today = date(2025, 4, 8)
    transaction_uuid = uuid4()
    article_uuid = uuid4()
    customer_uuid = uuid4()

    service_mock = mock.Mock(spec=TransactionService)
    service_mock.get_customer_transactions.return_value = [
        Transaction(
            transaction_uuid=transaction_uuid,
            t_dat=today,
            article_uuid=article_uuid,
            customer_uuid=customer_uuid
        )
    ]

    with app.container.transaction_service.override(service_mock):
        response = client.get(f"transaction/{customer_uuid}")

    content = response.json()
    data = content["data"][0]

    assert response.status_code == 200

    assert data["transaction_uuid"] == str(transaction_uuid)
    assert data["t_dat"] == str(today)
    assert data["article_uuid"] == str(article_uuid)
    assert data["customer_uuid"] == str(customer_uuid)


def test_insert_transaction(client):
    today = date(2025, 4, 8)
    transaction_uuid = uuid4()
    article_uuid = uuid4()
    customer_uuid = uuid4()

    service_mock = mock.Mock(spec=TransactionService)
    service_mock.insert_transaction.return_value = (
        Transaction(
            transaction_uuid=transaction_uuid,
            t_dat=today,
            article_uuid=article_uuid,
            customer_uuid=customer_uuid
        )
    )

    with app.container.transaction_service.override(service_mock):
        response = client.post(f"transaction/{customer_uuid}", params={"article_uuid": article_uuid})

    data = response.json()

    assert response.status_code == 200

    assert data["transaction_uuid"] == str(transaction_uuid)
    assert data["t_dat"] == str(today)
    assert data["article_uuid"] == str(article_uuid)
    assert data["customer_uuid"] == str(customer_uuid)
