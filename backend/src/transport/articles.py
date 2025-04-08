from typing import Optional, Annotated
from services import ArticleService, ImageService

from dependency_injector.wiring import Provide, inject
from containers import Container

from fastapi import APIRouter, Depends, Response

from .responses import Articles


articles = APIRouter()


@articles.get("/", response_model=Articles)
@inject
def get_articles(service: Annotated[ArticleService, Depends(Provide[Container.article_service])],
                 page: int,
                 size: int,
                 type_name: Optional[str] = None,
                 group_name: Optional[str] = None):
    return {
        "data": service.get_articles(page, size, type_name, group_name),
        "total_pages": int(service.get_total_articles(type_name, group_name) / size),
        "current_page": page,
        "page_size": size
    }


@articles.get("/types")
@inject
def get_types(service: Annotated[ArticleService, Depends(Provide[Container.article_service])]):
    return service.get_product_types()


@articles.get("/groups")
@inject
def get_groups(service: Annotated[ArticleService, Depends(Provide[Container.article_service])]):
    return service.get_product_groups()


@articles.get("/image")
@inject
def get_image(service: Annotated[ImageService, Depends(Provide[Container.image_service])],
              image_id: int):
    image_bytes = service.get_image(image_id)
    return Response(content=image_bytes, media_type="image/jpg")
