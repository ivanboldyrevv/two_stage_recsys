import services
import repositories

from database import Database
from s3interface import S3interface
from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["transport"]
    )
    config = providers.Configuration()

    db = providers.Singleton(
        Database,
        db_uri=config.db.uri
    )

    s3_interface = providers.Singleton(
        S3interface,
        endpoint_url=config.s3.endpoint_url,
        access_key=config.s3.access_key,
        secret_key=config.s3.secret_key,
        bucket_name=config.s3.bucket_name
    )

    customer_repository = providers.Factory(
        repositories.CustomerRepository,
        session_factory=db.provided.session
    )

    article_repository = providers.Factory(
        repositories.ArticleRepository,
        session_factory=db.provided.session
    )

    transaction_repository = providers.Factory(
        repositories.TransactionRepository,
        session_factory=db.provided.session
    )

    image_service = providers.Factory(
        services.ImageService,
        s3_interface=s3_interface
    )

    customer_service = providers.Factory(
        services.CustomerService,
        repository=customer_repository
    )

    article_service = providers.Factory(
        services.ArticleService,
        repository=article_repository
    )

    recs_service = providers.Factory(
        services.RecommendationService,
        repository=article_repository,
        model_url=config.model.url
    )

    transaction_service = providers.Factory(
        services.TransactionService,
        repository=transaction_repository
    )
