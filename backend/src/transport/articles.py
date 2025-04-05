from typing import Optional, Annotated
from services import ArticleService, ImageService

from dependency_injector.wiring import Provide, inject
from containers import Container

from fastapi import APIRouter, Depends, Response


article = APIRouter()


@article.get("/{page}/{size}")
@inject
def get_articles(service: Annotated[ArticleService, Depends(Provide[Container.article_service])],
                 page: int,
                 size: int,
                 type_name: Optional[str] = None,
                 group_name: Optional[str] = None):
    return service.get_articles(page, size, type_name, group_name)


@article.get("/{image_id}")
@inject
def get_image(service: Annotated[ImageService, Depends(Provide[Container.image_service])],
              image_id: int):
    image_bytes = service.get_image(image_id)
    return Response(content=image_bytes, media_type="image/jpg")
