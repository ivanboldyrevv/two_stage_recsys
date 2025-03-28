create database app_db;

\c app_db

create user backend with encrypted password 'backend';

grant connect on database app_db to backend;
grant usage, create on schema public to backend;
grant all privileges on all tables in schema public to backend;
alter default privileges in schema public grant all privileges on TABLES to backend;

do $$ 
begin
  raise notice 'Starting database initialization...';
end $$;

create table if not exists articles (
    article_uuid uuid primary key,
    product_code int,
    prod_name varchar(255),
    product_type_no int,
    product_type_name varchar(255),
    product_group_name varchar(255),
    graphical_appearance_no int,
    graphical_appearance_name varchar(255),
    colour_group_code int, 
    colour_group_name varchar(255),
    perceived_colour_value_id int,
    perceived_colour_value_name varchar(255),
    perceived_colour_master_id int, 
    perceived_colour_master_name varchar(255),
    department_no int,
    department_name varchar(255),
    index_code varchar(255),
    index_name varchar(255),
    index_group_no int,
    index_group_name varchar(255),
    section_no int,
    section_name varchar(255),
    garment_group_no int,
    garment_group_name varchar(255),
    detail_desc text
);

create table if not exists customers (
    customer_uuid uuid primary key,
    customer_id varchar(255),
    fn int,
    active int,
    club_member_status varchar(255),
    fashion_news_frequency varchar(255),
    age int,
    postal_code varchar(255)
);

create table if not exists transactions (
    transaction_uuid uuid primary key,
    t_dat date,
    customer_id varchar(255),
    article_id int,
    price numeric,
    sales_channel_id int,
    customer_uuid uuid references customers (customer_uuid)
        on delete cascade
        on update cascade,
    article_uuid uuid references articles (article_uuid)
        on delete cascade
        on update cascade
);

do $$
begin
    raise notice 'finished creating tables! start test check...';
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