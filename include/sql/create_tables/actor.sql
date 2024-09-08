CREATE TABLE IF NOT EXISTS raw_data.actor(
    actor_id integer,
    first_name character varying(45),
    last_name character varying(45) ,
    last_update timestamp without time zone,
    extracted_at timestamp without time zone     
)