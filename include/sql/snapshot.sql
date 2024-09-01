select *, now() as extracted_at
from {{ params.table_name }}