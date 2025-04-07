from typing import List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class Article(BaseModel):
    article_uuid: UUID
    prod_name: str
    product_type_name: str
    product_group_name: str
    detail_desc: str
    image_id: int


class Articles(BaseModel):
    data: List[Article]
    total_pages: int
    current_page: int
    page_size: int


class Transaction(BaseModel):
    transaction_uuid: UUID
    customer_uuid: UUID
    article_uuid: UUID
    t_dat: datetime


class Transactions(BaseModel):
    data: List[Transaction]
