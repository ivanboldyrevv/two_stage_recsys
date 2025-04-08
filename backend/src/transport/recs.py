from uuid import UUID
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from services import RecommendationService
from containers import Container

from fastapi import APIRouter, Depends


recs = APIRouter()


@recs.get("/two_stage")
@inject
def get_recommendation(service: Annotated[RecommendationService, Depends(Provide[Container.recs_service])],
                       customer_uuid: UUID):
    return service.get_recommendation(customer_uuid)
