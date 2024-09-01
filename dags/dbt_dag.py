from airflow.decorators import dag
from airflow.operators.dummy_operator import DummyOperator

from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, RenderConfig
from cosmos.profiles import RedshiftUserPasswordProfileMapping
from cosmos.constants import TestBehavior

from pendulum import datetime
from pathlib import Path


BASE_PATH = Path(__file__).parent.parent

CONNECTION_ID = "redshift_conn"
DB_NAME = "dvd_rental"
SCHEMA_NAME = "transformed_data"


DBT_PROJECT_PATH = f"{BASE_PATH}/include/dbt_project"

profile_config = ProfileConfig(
    profile_name="dvd_rental",
    target_name="transformed_data",
    profile_mapping=RedshiftUserPasswordProfileMapping(
        conn_id=CONNECTION_ID,
        profile_args={"schema": SCHEMA_NAME},
        
    )
)


@dag(
    start_date=datetime(2024, 9, 1),
    schedule=None,
    catchup=False
)
def dag_dbt_cosmos():

    start_process = DummyOperator(task_id='start_process')

    transform_data = DbtTaskGroup(
        group_id="transform_data",
        project_config=ProjectConfig(DBT_PROJECT_PATH),
        profile_config=profile_config,
        default_args={"retries": 2},
        operator_args={
                "install_deps": True
            }
    )

    start_process >> transform_data


dag_dbt_cosmos()