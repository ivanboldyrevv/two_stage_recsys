from typing import Annotated, Optional

from dependency_injector.wiring import Provide, inject
from services import CustomerService
from containers import Container
from fastapi import APIRouter, Depends


customer = APIRouter()


@customer.get("/random")
@inject
def get_random_user(service: Annotated[CustomerService, Depends(Provide[Container.customer_service])],
                    random_seed: Optional[int] = None):
    return service.get_random_customer(random_seed)
