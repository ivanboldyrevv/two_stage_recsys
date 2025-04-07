from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends
from .responses import Transactions, Transaction

from services import TransactionService
from containers import Container
from dependency_injector.wiring import Provide, inject


transaction = APIRouter()


@transaction.get("/{customer_uuid}", response_model=Transactions)
@inject
def get_transactions(service: Annotated[TransactionService, Depends(Provide[Container.transaction_service])],
                     customer_uuid: UUID):
    return {"data": service.get_customer_transactions(customer_uuid)}


@transaction.post("/{customer_uuid}", response_model=Transaction)
@inject
def insert_transactions(service: Annotated[TransactionService, Depends(Provide[Container.transaction_service])],
                        customer_uuid: UUID,
                        article_uuid: UUID):
    return service.insert_transaction(customer_uuid, article_uuid)
