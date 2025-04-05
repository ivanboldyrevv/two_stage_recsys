from dependency_injector import containers, providers
import mlflow.tracking

import services
import feature_store
import mlflow

from database import Database


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["transport"])
    config = providers.Configuration()

    mlflow_client = providers.Singleton(mlflow.MlflowClient)

    selection_model = providers.Singleton(
        mlflow.pyfunc.load_model,
        model_uri=(
            providers.Factory(
                lambda client, name, stage: f"models:/{name}/{client.get_latest_versions(name, [stage])[0].version}",
                client=mlflow_client,
                name=config.selection_model.name,
                stage="Production"
            )
        )
    )

    rerank_model = providers.Singleton(
        mlflow.catboost.load_model,
        model_uri=(
            providers.Factory(
                lambda client, name, stage: f"models:/{name}/{client.get_latest_versions(name, [stage])[0].version}",
                client=mlflow_client,
                name=config.rerank_model.name,
                stage="Production"
            )
        )
    )

    db = providers.Singleton(Database, db_uri=config.db.database_uri)

    feature_store = providers.Factory(
        feature_store.LocalFeatureStore,
        database=db
    )
    service = providers.Factory(
        services.Service,
        selection_model=selection_model,
        rerank_model=rerank_model,
        feature_store=feature_store
    )
