from transport.articles import article
from transport.recs import recs
from transport.customers import customer
from containers import Container

from fastapi import FastAPI


def create_app() -> FastAPI:
    container = Container()
    container.config.from_yaml("./config.yaml", required=True)

    db = container.db()
    db.create_database()

    app = FastAPI()

    app.include_router(customer, prefix="/customer")
    app.include_router(article, prefix="/article")
    app.include_router(recs, prefix="/recs")

    app.container = container
    return app


app = create_app()
