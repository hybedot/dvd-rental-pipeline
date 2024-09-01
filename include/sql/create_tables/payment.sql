CREATE TABLE IF NOT EXISTS raw_data.payment
(
    payment_id integer,
    customer_id smallint,
    staff_id smallint,
    rental_id integer,
    amount numeric(5,2),
    payment_date timestamp without time zone,
	extracted_at timestamp without time zone
    
)