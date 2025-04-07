from sqlalchemy import create_engine, orm
from sqlalchemy.orm import Session, declarative_base

from contextlib import contextmanager
from typing import Iterator

import logging

logger = logging.getLogger(__name__)

Base = declarative_base()


class Database:
    def __init__(self, db_uri: str) -> None:
        self._engine = create_engine(db_uri, echo=True)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    def drop_all(self) -> None:
        Base.metadata.drop_all(self._engine)

    @contextmanager
    def session(self) -> Iterator:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception")
            session.rollback()
            raise
        finally:
            session.close()
