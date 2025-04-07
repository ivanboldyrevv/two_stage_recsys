from uuid import UUID, uuid4
from datetime import datetime

from contextlib import AbstractContextManager
from typing import Callable, TypeVar, Generic, Type, List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import select

from models import Customer, Article, Transaction

T = TypeVar("T")


class Repository(Generic[T]):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]], model: Type[T]) -> None:
        self.session_factory = session_factory
        self.model = model

    def get_all(self) -> List[T]:
        with self.session_factory() as session:
            return session.query(self.model).all()

    def get_by_uuid(self, entity_uuid: UUID, filter_attr: str) -> T:
        with self.session_factory() as session:
            entity = session.query(self.model).filter(getattr(self.model, filter_attr) == entity_uuid).first()
            if not entity:
                raise NotFoundError(self.model.__name__, entity_uuid)
            return entity


class CustomerRepository(Repository[Customer]):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        super().__init__(session_factory, Customer)


class ArticleRepository(Repository[Article]):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        super().__init__(session_factory, Article)

    def get_articles(self,
                     limit: int,
                     offset: int,
                     type_name: Optional[str] = None,
                     group_name: Optional[str] = None) -> List[Article]:
        with self.session_factory() as session:
            query = select(Article).limit(limit).offset(offset)

            if type_name is not None:
                query = query.where(Article.product_type_name == type_name)
            if group_name is not None:
                query = query.where(Article.product_group_name == group_name)

            articles = session.execute(query).scalars().all()

            if not articles:
                raise NotFoundError(Article.__name__, "ALL")

            return articles


class TransactionRepository(Repository[Transaction]):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        super().__init__(session_factory, Transaction)

    def insert_transaction(self, customer_uuid: UUID, article_uuid: UUID) -> Transaction:
        with self.session_factory() as session:
            session.add(Transaction(
                transaction_uuid=uuid4(),
                t_dat=datetime.now().strftime("%Y-%m-%d"),
                customer_uuid=customer_uuid,
                article_uuid=article_uuid
            ))
            session.commit()

            entity = (session
                      .query(Transaction)
                      .where(Transaction.customer_uuid == customer_uuid)
                      .where(Transaction.article_uuid == article_uuid)
                      .first())
            if not entity:
                raise InsertError(self.model.__name__, customer_uuid)
            return entity

    def get_customer_transaction(self, customer_uuid: UUID) -> List[Transaction]:
        with self.session_factory() as session:
            entity = session.query(Transaction).where(Transaction.customer_uuid == customer_uuid).all()
            if not entity:
                raise NotFoundError(self.model.__name__, customer_uuid)
            return entity


class NotFoundError(Exception):
    def __init__(self, entity_name: str, entity_id: UUID) -> None:
        super().__init__(f"{entity_name} not found, id: {entity_id}")


class InsertError(Exception):
    def __init__(self, entity_name: str, entity_id: UUID) -> None:
        super().__init__(f"{entity_name} insert error, id: {entity_id}")
