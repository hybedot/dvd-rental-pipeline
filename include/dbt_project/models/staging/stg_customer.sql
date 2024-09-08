SELECT
    *
FROM
    {{ source('raw_data', 'customer') }}
