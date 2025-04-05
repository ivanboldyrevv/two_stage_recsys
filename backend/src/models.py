from sqlalchemy import Column, Integer, UUID, VARCHAR, Text

from database import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_uuid = Column(UUID, primary_key=True)
    age = Column(Integer)


class Article(Base):
    __tablename__ = "articles"

    article_uuid = Column(UUID, primary_key=True)
    prod_name = Column(VARCHAR)
    product_type_name = Column(VARCHAR)
    product_group_name = Column(VARCHAR)
    detail_desc = Column(Text)
    image_id = Column(Integer)
