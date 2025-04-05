from uuid import UUID
from database import Database
from typing import (List,
                    Dict,
                    Any,
                    Optional)

import pandas as pd


class LocalFeatureStore:
    """
    The class is a buffer between the model and the database.
    (Perhaps should use something like Feast or something like that?)
    args:
        database: Database
    """
    def __init__(self, database: Database) -> None:
        self.database = database

    def get_online_features(self,
                            customer_uuid: UUID,
                            articles_uuids: List[int],
                            day_offset: Optional[int] = None) -> pd.DataFrame:
        """
        The method is intended for receiving online features.
        Can use the day_offset argument to use interactions only that hit day offset.
        (day_offset does not work yet)
        return pd.DataFrame with columns:
            - customer_id
            - article_id
            - age
            - product_type_no
            - product_group_no
            - department_no
            - index_code
            - index_group_no
            - section_no
            - garment_group_no
            - article_freq
            - product_group_freq
            - index_freq
            - garment_group_freq
        """
        customer_features = self.get_customer_features(customer_uuid)
        articles_features = self.get_articles_features(articles_uuids)
        frequency_features = self._get_frequency_features(customer_uuid)

        df = customer_features.merge(articles_features, how="cross")
        df = df.merge(frequency_features,
                      how="left",
                      on=["customer_uuid", "customer_id", "product_group_no", "index_code", "garment_group_no"])

        df = df[[
            "customer_id", "article_id", "age",
            "product_type_no", "product_group_no", "department_no", "index_code", "index_group_no", "section_no",
            "garment_group_no", "article_freq", "product_group_freq", "index_freq", "garment_group_freq"
        ]]

        df = df.drop_duplicates(subset=["article_id"])
        df.fillna(0, inplace=True)

        return df

    def get_customer_features(self, customer_uuid: UUID) -> pd.DataFrame:
        return self._execute_query(
            """
                select *
                  from customers
                 where customer_uuid = :customer_uuid
            """,
            {"customer_uuid": customer_uuid}
        )

    def get_inner_customer_id(self, customer_uuid: UUID) -> pd.DataFrame:
        return self._execute_query(
            """
                select customer_id
                  from customers
                 where customer_uuid = :customer_uuid
            """,
            {"customer_uuid": customer_uuid}
        )

    def get_raw_customer_id(self, customer_id: int) -> pd.DataFrame:
        return self._execute_query(
            """
                select customer_uuid
                  from customers
                 where customer_id = :customer_id
            """,
            {"customer_id": customer_id}
        )

    def get_articles_features(self, artciles_ids: List[UUID]) -> pd.DataFrame:
        return self._execute_query(
            """
                select *
                  from articles a
                  join (select article_uuid, count(article_uuid) article_freq
                          from transactions
                         where article_uuid in :artciles_ids
                         group by article_uuid) freq using (article_uuid)
                 where a.article_uuid in :artciles_ids
            """,
            {"artciles_ids": tuple(artciles_ids)}
        )

    def get_raw_article_id(self, articles_ids: List[int]) -> pd.DataFrame:
        return self._execute_query(
            """
                select article_uuid
                  from articles
                 where article_id in :articles_ids
            """,
            {"articles_ids": tuple(articles_ids)}
        )

    def get_inner_article_id(self, articles_ids: List[UUID]) -> pd.DataFrame:
        return self._execute_query(
            """
                select article_id
                  from articles
                 where article_uuid in :articles_ids
            """,
            {"articles_ids": tuple(articles_ids)}
        )

    def _get_frequency_features(self, customer_uuid: UUID) -> pd.DataFrame:
        """
        return dataframe w/ freq columns:
            - product_group_freq
            - index_freq
            - garment_group_freq
        """
        transactions = self._get_transactions(customer_uuid)

        frequency_features = self._calculate_freq_feature(
            transactions, transactions, ["customer_uuid", "product_group_no"], "index_code", "product_group_freq"
        )
        frequency_features = self._calculate_freq_feature(
            frequency_features, transactions, ["customer_uuid", "index_code"], "product_group_no", "index_freq"
        )
        frequency_features = self._calculate_freq_feature(
            frequency_features, transactions, ["customer_uuid", "garment_group_no"], "index_code", "garment_group_freq"
        )

        return frequency_features[[
            "customer_uuid", "customer_id", "product_group_no", "index_code", "garment_group_no",
            "product_group_freq", "index_freq", "garment_group_freq"
        ]]

    def _get_transactions(self, customer_uuid: UUID) -> pd.DataFrame:
        """
            returns a pd.DataFrame with all user interactions.
            returns only the columns that were used to train the CatBoost model.
            that is, columns : (customer_id, article_id, age, ptn, pgn, ic, igc, sn, ggn) - frequency features.
        """
        return self._execute_query(
            """
                select c.customer_uuid,
                       c.customer_id,
                       a.product_type_no,
                       a.product_group_no,
                       a.department_no,
                       a.index_code,
                       a.index_group_no,
                       a.section_no,
                       a.garment_group_no
                  from transactions t
                  join articles a
                    on t.article_uuid = a.article_uuid
                  join customers c
                    on t.customer_uuid = c.customer_uuid
                 where c.customer_uuid = :customer_uuid
            """,
            {"customer_uuid": customer_uuid}
        )

    def _calculate_freq_feature(self,
                                left: pd.DataFrame,
                                right: pd.DataFrame,
                                group_by: List[str],
                                agg_col: str,
                                feature_name: str) -> pd.DataFrame:
        return left.merge(
            right.groupby(by=group_by)[agg_col]
            .count()
            .rename(feature_name) / 1,
            how="left",
            on=group_by
        )

    def _execute_query(self, sql_query: str, format_dict: Dict[str, Any]) -> pd.DataFrame:
        with self.database.session() as session:
            query = self.database.get_text(
                sql_query
            )
            result = session.execute(query, format_dict)
        return pd.DataFrame(result.mappings())
