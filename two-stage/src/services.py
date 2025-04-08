from uuid import UUID
from typing import List, Dict

from feature_store import LocalFeatureStore

import mlflow.pyfunc
import mlflow.catboost

import numpy as np
import pandas as pd


class Service:
    def __init__(self,
                 selection_model: mlflow.pyfunc.PythonModel,
                 rerank_model: mlflow.catboost._CatboostModelWrapper,
                 feature_store: LocalFeatureStore) -> None:
        self.feature_store = feature_store

        self.rerank_model = rerank_model

        unwrapped_selection_model = selection_model.unwrap_python_model()
        self.selection_model = unwrapped_selection_model.get_raw_model()
        self.sparse_matrix = unwrapped_selection_model.sparse_matrix

    def get_recommendation(self, customer_uuid: UUID, N: int = 10):
        # TEST N CANDIDATES
        n_candidates = 1000
        # Step 1: match candidates
        candidates = self._select_candidates(customer_uuid, n_candidates)
        # Step 2: prepare data for rerank inference
        candidates_features = self._prepare_reranking_features(customer_uuid, candidates)
        # Step 3: rerank candidates
        reranked_candidates = self._rerank_and_select(candidates_features, N)

        return self._format_results(reranked_candidates)

    def _select_candidates(self, customer_uuid: UUID, N: int = 10):
        customer_features = self.feature_store.get_customer_features(customer_uuid)
        customer_id = customer_features["customer_id"]

        articles, _ = self.selection_model.recommend(
            customer_id,
            self.sparse_matrix[customer_id],
            N=N
        )

        return self._convert_article_ids(articles)

    def _convert_article_ids(self, article_ids: np.ndarray) -> List[int]:
        return article_ids.squeeze().astype(int).tolist()

    def _prepare_reranking_features(self, customer_uuid: UUID, article_ids: List[int]) -> pd.DataFrame:
        raw_article_ids = self.feature_store.get_raw_article_id(article_ids)
        articles_info = self.feature_store.get_articles_features(raw_article_ids["article_uuid"].tolist())
        features_data = self.feature_store.get_online_features(
            customer_uuid,
            articles_info["article_uuid"].tolist()
        )
        return features_data

    def _rerank_and_select(self,  features_data: pd.DataFrame, top_n: int) -> pd.DataFrame:
        features_data["prediction_score"] = self.rerank_model.predict(
            features_data,
            prediction_type="Probability"
        )[:, 1]

        return features_data.sort_values("prediction_score", ascending=False).head(top_n)

    def _format_results(self, ranked_articles: pd.DataFrame) -> Dict[str, List[UUID]]:
        customer_uuid = self.feature_store.get_raw_customer_id(
            int(ranked_articles["customer_id"].iloc[0])
        )
        article_uuids = self.feature_store.get_raw_article_id(
            ranked_articles["article_id"].tolist()
        )

        return {
            "customer_uuid": customer_uuid["customer_uuid"].iloc[0],
            "articles": article_uuids["article_uuid"].tolist()
        }

    def _get_fallback_recommendations(self) -> Dict[str, List[UUID]]:
        pass
