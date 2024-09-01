select *, now() as extracted_at
from {{ params.table_name }}
where date({{params.date_column}}) = '{{ ds }}'