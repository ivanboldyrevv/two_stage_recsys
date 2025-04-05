import pytest
from uuid import UUID
from unittest.mock import Mock
import pandas as pd
from feature_store import LocalFeatureStore

# TODO: 1/10 methods are covered by tests


@pytest.fixture
def mock_db():
    db = Mock()
    db.session = Mock()
    db.get_text = Mock(return_value="mocked_query")
    return db


@pytest.fixture
def feature_store(mock_db):
    return LocalFeatureStore(mock_db)


def test_get_online_features(feature_store, mock_db):
    customer_uuid = UUID("123e4567-e89b-12d3-a456-426614174000")
    articles_uuids = [UUID("223e4567-e89b-12d3-a456-426614174000")]

    mock_customer = pd.DataFrame({
        "customer_uuid": [UUID("b9577fed-6e1b-4549-bb58-38f929b5108c")],
        "age": [44],
        "customer_id": [0]
    })

    mock_articles = pd.DataFrame({
         "article_uuid": [UUID("e865690b-d898-48c5-a1fd-03b0b361c3c7")],
         "article_freq": [50],
         "product_type_no": [253],
         "product_group_no": [0],
         "department_no": [1676],
         "index_code": ["A"],
         "index_group_no": [1],
         "section_no": [16],
         "garment_group_no": [1002],
         "article_id": [0]
    })

    mock_freq = pd.DataFrame({
        "customer_uuid": [UUID("b9577fed-6e1b-4549-bb58-38f929b5108c")],
        "customer_id": [0],
        "product_group_no": [0],
        "index_code": ["A"],
        "product_group_freq": [10],
        "garment_group_no": [1002],
        "index_freq": [100],
        "garment_group_freq": [1000]
    })

    feature_store.get_customer_features = Mock(return_value=mock_customer)
    feature_store.get_articles_features = Mock(return_value=mock_articles)
    feature_store._get_frequency_features = Mock(return_value=mock_freq)

    result = feature_store.get_online_features(customer_uuid, articles_uuids)

    customers_columns = ["customer_id", "age"]

    article_columns = [
        "article_id", "product_type_no", "product_group_no", "department_no", "index_group_no",
        "index_code", "section_no", "garment_group_no", "article_freq"
    ]

    freq_columns = ["product_group_freq", "index_freq", "garment_group_freq"]

    expected_columns = set(customers_columns + article_columns + freq_columns)

    assert not result.empty
    assert expected_columns == set(result.columns.tolist())
    feature_store.get_customer_features.assert_called_once_with(customer_uuid)
    feature_store.get_articles_features.assert_called_once_with(articles_uuids)
