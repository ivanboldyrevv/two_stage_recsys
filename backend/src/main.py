from transport.articles import articles
from transport.recs import recs
from transport.customers import customer
from containers import Container

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    container = Container()
    container.config.from_yaml("./config.yaml", required=True)

    db = container.db()
    db.create_database()

    app = FastAPI()

    app.include_router(customer, prefix="/customer")
    app.include_router(articles, prefix="/articles")
    app.include_router(recs, prefix="/recs")

    app.container = container

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


app = create_app()
