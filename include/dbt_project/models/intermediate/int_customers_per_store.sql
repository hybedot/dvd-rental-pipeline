SELECT
    store_id,
    COUNT(*) AS total_customers
FROM
    {{ ref('stg_customer') }}
GROUP BY
    1
