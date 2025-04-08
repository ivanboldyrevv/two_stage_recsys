from typing import Generic, TypeVar, List, Optional
from uuid import UUID

from repositories import (CustomerRepository,
                          ArticleRepository,
                          TransactionRepository)

from s3interface import S3interface

from models import Customer, Article, Transaction

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


class CustomerService(BaseService[CustomerRepository]):
    def __init__(self, repository: CustomerRepository) -> None:
        super().__init__(repository)

    def get_random_customer(self, random_seed: Optional[int] = None) -> Customer:
        if random_seed:
            random.seed(random_seed)
        customers = self.repository.get_all()
        return random.choice(customers)


class ArticleService(BaseService[ArticleRepository]):
    def __init__(self, repository: ArticleRepository) -> None:
        super().__init__(repository)

    def get_article_by_uuid(self, article_uuid: UUID) -> Article:
        return self.repository.get_by_uuid(article_uuid, "article_uuid")

    def get_articles(self,
                     page: int,
                     size: int,
                     type_name: Optional[str] = None,
                     group_name: Optional[str] = None) -> List[Article]:
        return self.repository.get_articles(
            limit=size,
            offset=page * size,
            type_name=type_name,
            group_name=group_name
        )

    def get_product_types(self) -> List[str]:
        return self.repository.get_product_types()

    def get_product_groups(self) -> List[str]:
        return self.repository.get_product_groups()

    def get_total_articles(self) -> int:
        return len(self.repository.get_all())


class RecommendationService(BaseService[ArticleRepository]):
    def __init__(self, repository: ArticleRepository, model_url: str) -> None:
        super().__init__(repository)
        self.model_url = model_url

    def get_recommendation(self, customer_uuid: UUID) -> List[Article]:
        response = requests.get(f"{self.model_url}/get_recommendations/{customer_uuid}")
        uuids = response.json()["articles"]

        result = []

        for uuid in uuids:
            article = self.get_article_by_uuid(uuid)
            result.append(article)

        return result

    def get_article_by_uuid(self, article_uuid: UUID) -> Article:
        return self.repository.get_by_uuid(article_uuid, "article_uuid")


class TransactionService(BaseService[TransactionRepository]):
    def __init__(self, repository: TransactionRepository) -> None:
        super().__init__(repository)

    def insert_transaction(self, customer_uuid: UUID, article_uuid: UUID) -> Transaction:
        return self.repository.insert_transaction(customer_uuid, article_uuid)

    def get_customer_transactions(self, customer_uuid: UUID) -> List[Transaction]:
        return self.repository.get_customer_transaction(customer_uuid)
