import os
from fastapi import FastAPI

from containers import Container
from transport.recs import recs


def create_app() -> FastAPI:
    container = Container()
    container.config.from_yaml("./config.yaml", required=True)

    os.environ.update({
        "MLFLOW_TRACKING_URI": container.config.mlflow.tracking_uri(),
        "MLFLOW_S3_ENDPOINT_URL": container.config.mlflow.s3_endpoint_url(),
        "AWS_ACCESS_KEY_ID": container.config.aws.access_key_id(),
        "AWS_SECRET_ACCESS_KEY": container.config.aws.secret_access_key()
    })

    db = container.db()
    db.create_database()

    app = FastAPI()
    app.container = container
    app.include_router(recs)
    return app


app = create_app()
