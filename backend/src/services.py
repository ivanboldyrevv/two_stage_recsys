from typing import Generic, TypeVar, Iterable, Optional
from uuid import UUID

from repositories import CustomerRepository, ArticleRepository
from s3interface import S3interface

from models import Customer, Article

import random
import requests

T = TypeVar("T")


class BaseService(Generic[T]):
    def __init__(self, repository: T) -> None:
        self.repository = repository


class ImageService:
    def __init__(self, s3_interface: S3interface):
        self.s3 = s3_interface

    def get_image(self, image_id: int) -> bytes:
        return self.s3.get_image(image_id)


class CustomerService(BaseService):
    def __init__(self, repository: CustomerRepository) -> None:
        super().__init__(repository)

    def get_random_customer(self, random_seed: Optional[int] = None) -> Customer:
        if random_seed:
            random.seed(random_seed)
        customers = self.repository.get_all()
        return random.choice(customers)


class ArticleService(BaseService):
    def __init__(self, repository: ArticleRepository) -> None:
        super().__init__(repository)

    def get_article_by_uuid(self, article_uuid: UUID) -> Article:
        return self.repository.get_by_uuid(article_uuid, "article_uuid")

    def get_articles(self,
                     page: int,
                     size: int,
                     type_name: Optional[str] = None,
                     group_name: Optional[str] = None) -> Iterable[Article]:
        return self.repository.get_articles(
            limit=size,
            offset=page * size,
            type_name=type_name,
            group_name=group_name
        )


class RecommendationService(BaseService):
    def __init__(self, repository: ArticleRepository, model_url: str) -> None:
        super().__init__(repository)
        self.model_url = model_url

    def get_recommendation(self, customer_uuid: UUID):
        response = requests.get(f"{self.model_url}/{customer_uuid}")
        uuids = response.json()["articles"]

        detailed = []

        for uuid in uuids:
            article = self.get_article_by_uuid(uuid)
            article.image_bytes = self.image_service.get_image(article.image_id)
            detailed.append(article)

        return detailed
