from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Depends

from dependency_injector.wiring import Provide, inject

from containers import Container
from services import Service


recs = APIRouter()


@recs.get("/get_recommendations/{customer_uuid}")
@inject
def get_recommendations(customer_uuid: UUID,
                        recommendation_service: Annotated[Service, Depends(Provide[Container.service])]):
    return recommendation_service.get_recommendation(customer_uuid)
