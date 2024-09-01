from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.providers.amazon.aws.transfers.sql_to_s3 import SqlToS3Operator
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from airflow.providers.amazon.aws.operators.redshift_sql import RedshiftSQLOperator


from pathlib import Path


BASE_PATH = Path(__file__).parent.parent
MY_S3_BUCKET = "eingineerdata-dvd-rental"
MY_SQL_CONN_ID = "postgres_conn"
AWS_CONN_ID = "aws_s3_conn"
REDSHIFT_CONN_ID = "redshift_conn"
RAW_SCHEMA = "raw_data"


MY_S3_KEY = "actor"\
             "/{{ macros.ds_format(ds, '%Y-%m-%d', '%Y') }}"\
            "/{{ macros.ds_format(ds, '%Y-%m-%d', '%m') }}"\
            "/{{ macros.ds_format(ds, '%Y-%m-%d', '%d') }}"\
            "/actor"\
            "{{ ds_nodash }}.csv" 



DEFAULT_DAG_ARGS = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "email_on_failure": False,
    "email_on_retry": False,
}


with DAG(
    dag_id="actor_extract_load_v01",
    start_date=datetime.strptime("2013-05-06", "%Y-%m-%d"),
    end_date=datetime.strptime("2013-05-06", "%Y-%m-%d"),
    default_args=DEFAULT_DAG_ARGS,
    template_searchpath=f"{BASE_PATH}/include/",
    schedule_interval="@daily",
    catchup=True,
    # tags="main",
) as dag:


    psql_to_s3 = SqlToS3Operator(
        task_id = "psql_to_s3_data_extract",
        query="sql/snapshot.sql",
        s3_bucket=MY_S3_BUCKET,
        s3_key=MY_S3_KEY,
        sql_conn_id=MY_SQL_CONN_ID,
        params={"table_name": "actor", "date_column": "last_update"},
        replace="False",
        aws_conn_id=AWS_CONN_ID,
        file_format="csv",
        pd_kwargs={"index": False},
    )

    create_redshift_tables = RedshiftSQLOperator(
        task_id = "create_table",
        redshift_conn_id = REDSHIFT_CONN_ID,
        autocommit = True,
        sql="sql/create_tables/actor.sql",
    )

    s3_to_reshift = S3ToRedshiftOperator(
        task_id="s3_to_reshift_data_load",
        schema=RAW_SCHEMA,
        table="actor",
        s3_bucket=MY_S3_BUCKET,
        s3_key=MY_S3_KEY,
        redshift_conn_id=REDSHIFT_CONN_ID,
        aws_conn_id=AWS_CONN_ID,
        method="REPLACE",
        copy_options=['CSV', 'IGNOREHEADER 1']
        
    )

psql_to_s3 >> create_redshift_tables >> s3_to_reshift