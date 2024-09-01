SELECT
    *
FROM
    {{ source('raw_data', 'payment') }}
