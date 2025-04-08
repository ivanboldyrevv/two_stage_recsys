from uuid import uuid4

from services import ArticleService
from repositories import ArticleRepository
from models import Article

from .utils import db, insert

import pytest


database = db


@pytest.fixture()
def service(database):
    return ArticleService(ArticleRepository(database.session))


@pytest.fixture()
def article_dict():
    return {
        "article_uuid": uuid4(),
        "prod_name": "test_name",
        "product_type_name": "test_type",
        "product_group_name": "test_group",
        "detail_desc": "test_desc",
        "image_id": 0
    }


def test_get_types(service, article_dict):
    data = article_dict
    insert(Article(**data))

    result = service.get_product_types()
    assert ["test_type"] == result


def test_get_group(service, article_dict):
    data = article_dict
    insert(Article(**data))

    result = service.get_product_groups()
    assert ["test_group"] == result


def test_get_article_by_uuid(service, article_dict):
    data = article_dict
    insert(Article(**data))

    result = service.get_article_by_uuid(article_dict["article_uuid"])

    assert result.article_uuid == article_dict["article_uuid"]
    assert result.prod_name == article_dict["prod_name"]


def test_get_articles(service, article_dict):
    data = article_dict
    insert(Article(**data))

    result = service.get_articles(0, 15)

    assert isinstance(result, list)

    assert result[0].article_uuid == article_dict["article_uuid"]
    assert result[0].prod_name == article_dict["prod_name"]


def test_get_filtred_articles(service):
    insert(*[

        Article(**{
            "article_uuid": uuid4(),
            "prod_name": "test_name",
            "product_type_name": "test_type",
            "product_group_name": "test_group",
            "detail_desc": "test_desc",
            "image_id": 0
        }),

        Article(**{
            "article_uuid": uuid4(),
            "prod_name": "filtred_prod",
            "product_type_name": "filtred_type",
            "product_group_name": "filtred_group",
            "detail_desc": "test_desc",
            "image_id": 1
        })
    ])

    result = service.get_articles(0, 15, "filtred_type", "filtred_group")

    assert len(result) == 1
    assert result[0].product_group_name == "filtred_group"
    assert result[0].product_type_name == "filtred_type"

    result = service.get_articles(0, 15, type_name="filtred_type")

    assert len(result) == 1
    assert result[0].product_type_name == "filtred_type"

    result = service.get_articles(0, 15, group_name="filtred_group")

    assert len(result) == 1
    assert result[0].product_group_name == "filtred_group"


def test_total_articles(service, article_dict):
    data = article_dict
    insert(Article(**data))

    result = service.get_total_articles()
    assert result == 1
