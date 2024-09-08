CREATE TABLE IF NOT EXISTS raw_data.customer
(
    customer_id integer,
    store_id smallint,
    first_name character varying(45),
    last_name character varying(45),
    email character varying(50),
    address_id smallint,
    activebool boolean,
    create_date date,
    last_update timestamp without time zone,
    active integer,
    extracted_at timestamp without time zone
)