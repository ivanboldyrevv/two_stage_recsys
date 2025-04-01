create database app_db;

\c app_db

create user backend with encrypted password 'backend';

do $$ 
begin
  raise notice 'Starting database initialization...';
end $$;

create table if not exists articles (
    article_uuid uuid   primary key,
    prod_name           varchar(255),
    product_type_no     int,
    product_type_name   varchar(255),
    product_group_no    int,
    product_group_name  varchar(255),
    department_no       int,
    department_name     varchar(255),
    index_code          varchar(255),
    index_name          varchar(255),
    index_group_no      int,
    index_group_name    varchar(255),
    section_no          int,
    section_name        varchar(255),
    garment_group_no    int,
    garment_group_name  varchar(255),
    detail_desc         text,
    article_id          serial
);

create table if not exists customers (
    customer_uuid uuid      primary key,
    fn                      int,
    active                  int,
    club_member_status      varchar(255),
    fashion_news_frequency  varchar(255),
    age                     int,
    postal_code             varchar(255),
    customer_id             serial
);

alter sequence customers_customer_id_seq restart with 0;
alter sequence articles_article_id_seq restart with 0;

create table if not exists transactions (
    transaction_uuid uuid primary key,
    t_dat                 date,
    price                 numeric,
    sales_channel_id      int,

    customer_uuid uuid references customers (customer_uuid)
        on delete cascade
        on update cascade,
    article_uuid uuid references articles (article_uuid)
        on delete cascade
        on update cascade
);

do $$
begin
    raise notice 'finished creating tables!';
end $$;


grant connect on database app_db to backend;
grant usage, select, update on all sequences in schema public TO backend;
grant all privileges on all tables in schema public to backend;
alter default privileges in schema public grant all privileges on tables to backend;


do $$
begin
    raise notice 'finished grant priveleges...';
end $$;


do $$
begin
    raise notice 'start test check...';
end $$;

do $$
begin
  if not exists (
    select 1 from information_schema.tables 
    where table_name = 'articles'
  ) then
    raise exception 'Table "articles" not created!';
  end if;

  if not exists (
    select 1 from information_schema.tables 
    where table_name = 'customers'
  ) then
    raise exception 'Table "customers" not created!';
  end if;
end $$;


create database mlflow_db;
\c mlflow_db

create user mlflow with encrypted password 'mlflow';

GRANT ALL PRIVILEGES ON DATABASE mlflow_db TO mlflow;
GRANT ALL ON SCHEMA public TO mlflow;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO mlflow;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO mlflow;