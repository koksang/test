"""
#### Summary
1. Extract table from bq to gcs
2. Ingest data from gcs to bq
3. Run dbt models
"""

from __future__ import annotations

from datetime import timedelta
from pathlib import Path
from textwrap import dedent

from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateExternalTableOperator,
)
from airflow.providers.google.cloud.transfers.bigquery_to_gcs import (
    BigQueryToGCSOperator,
)
from cosmos import (
    DbtSeedKubernetesOperator,
    DbtTaskGroup,
    ExecutionConfig,
    ExecutionMode,
    ProjectConfig,
    RenderConfig,
)
from cosmos.constants import InvocationMode
from include.constants.dbt import DBT_IMAGE, DBT_PROJECT_DIR, PROFILE_CONFIG
from pendulum import datetime

HOLIDAY_TABLE_ID = "common.us_annual_public_holidays"
BUCKET = "mv-stg-etl-data-artifacts"
DATASET, TABLE = "chicago_taxi_trips", "taxi_trips"
FORMAT, COMPRESSION = "PARQUET", "GZIP"
GCS_OBJECT_URI = f"{DATASET}/{TABLE}/*.{COMPRESSION.lower()}.parquet"
DAG_ID = Path(__file__).stem
DEFAULT_ARGS = dict(
    owner="koksang",
    depends_on_past=False,
    retries=2,
    retry_delay=timedelta(minutes=5),
)
PARAMS = dict(start_timestamp=None, end_timestamp=None)

with DAG(
    dag_id=DAG_ID,
    doc_md=dedent(__doc__ or DAG_ID),
    start_date=datetime(2024, 8, 20),
    schedule=None,  # "0 2 * * *",
    catchup=False,
    params=PARAMS,
    default_args=DEFAULT_ARGS,
) as dag:
    bq_to_gcs = BigQueryToGCSOperator(
        task_id="bq_to_gcs",
        source_project_dataset_table=f"bigquery-public-data.{DATASET}.{TABLE}",
        destination_cloud_storage_uris=[f"gs://{BUCKET}/{GCS_OBJECT_URI}"],
        export_format=FORMAT,
        compression=COMPRESSION,
        labels=dict(
            task_id="bq_to_gcs",
        ),
    )

    create_table = BigQueryCreateExternalTableOperator(
        task_id="create_table",
        bucket=BUCKET,
        source_objects=[GCS_OBJECT_URI],
        destination_project_dataset_table=f"{DATASET}.{TABLE}",
        source_format=FORMAT,
        compression=COMPRESSION,
        autodetect=True,
        max_bad_records=0,
        labels=dict(
            task_id="create_table",
        ),
    )

    dbt_models = DbtTaskGroup(
        group_id=f"{DATASET}-{TABLE}",
        profile_config=PROFILE_CONFIG,
        project_config=ProjectConfig(DBT_PROJECT_DIR),
        execution_config=ExecutionConfig(
            execution_mode=ExecutionMode.LOCAL,
            invocation_mode=InvocationMode.DBT_RUNNER,
        ),
        render_config=RenderConfig(
            select=[DATASET],
        ),
        operator_args=dict(
            # image=DBT_IMAGE,
            # get_logs=True,
            # image_pull_policy="Always",
            # is_delete_operator_pod=False,
            # do_xcom_push=True,
            # startup_timeout_seconds=300,
            # execution_timeout=timedelta(minutes=20),
            #
            quiet=True,
            warn_error=True,
            cancel_query_on_kill=True,
        ),
        default_args=DEFAULT_ARGS,
    )

    bq_to_gcs >> create_table >> dbt_models
