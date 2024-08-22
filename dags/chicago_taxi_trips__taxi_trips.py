"""
#### Summary
1. Extract table from bq to gcs
2. Ingest data from gcs to bq
3. Run dbt models
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta
from pathlib import Path
from textwrap import dedent

from airflow.models import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateEmptyDatasetOperator,
    BigQueryCreateExternalTableOperator,
)
from airflow.providers.google.cloud.transfers.bigquery_to_gcs import (
    BigQueryToGCSOperator,
)
from cosmos import DbtTaskGroup, LoadMode, RenderConfig
from include.constants.airflow import TableSchema
from include.constants.dbt import EXECUTION_CONFIG, PROFILE_CONFIG, PROJECT_CONFIG
from include.helpers import check_table_exists, task_fail_alert

PROJECT_ID, BUCKET = os.environ["PROJECT_ID"], os.environ["BUCKET"]
FORMAT, COMPRESSION = "PARQUET", "GZIP"

DAG_ID = Path(__file__).stem
DATASET, TABLE = DAG_ID.split("__")
GCS_OBJECT_URI = f"{DATASET}/{TABLE}/*.{COMPRESSION.lower()}.parquet"
DEFAULT_ARGS = dict(
    owner="koksang",
    depends_on_past=False,
    retries=2,
    retry_delay=timedelta(minutes=5),
    task_fail_alert=task_fail_alert,
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
    create_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id="create_dataset",
        project_id=PROJECT_ID,
        dataset_id=DATASET,
    )

    check_table_exists = BranchPythonOperator(  # type: ignore
        task_id="check_table_exists",
        python_callable=check_table_exists,
        op_kwargs=dict(
            dataset_id=DATASET,
            table_id=TABLE,
            success_task_id="prepare_dbt",
            failure_task_id="bq_to_gcs",
        ),
    )

    prepare_dbt = EmptyOperator(task_id="prepare_dbt", trigger_rule="none_failed")

    bq_to_gcs = BigQueryToGCSOperator(
        task_id="bq_to_gcs",
        source_project_dataset_table=f"bigquery-public-data.{DATASET}.{TABLE}",
        destination_cloud_storage_uris=[f"gs://{BUCKET}/{GCS_OBJECT_URI}"],
        export_format=FORMAT,
        compression=COMPRESSION,
    )
    create_table = BigQueryCreateExternalTableOperator(
        task_id="create_table",
        bucket=BUCKET,
        source_objects=[GCS_OBJECT_URI],
        destination_project_dataset_table=f"{DATASET}.{TABLE}",
        source_format=FORMAT,
        compression=COMPRESSION,
        schema_fields=getattr(TableSchema, DAG_ID),
        autodetect=True,
        max_bad_records=0,
    )

    dbt_models = DbtTaskGroup(
        group_id=f"{DATASET}__{TABLE}",
        profile_config=PROFILE_CONFIG,
        project_config=PROJECT_CONFIG,
        execution_config=EXECUTION_CONFIG,
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=[DATASET],
        ),
        operator_args=dict(
            quiet=True,
            warn_error=True,
            cancel_query_on_kill=True,
        ),
        default_args=DEFAULT_ARGS,
    )

    create_dataset >> check_table_exists >> [bq_to_gcs, prepare_dbt]  # type: ignore
    bq_to_gcs >> create_table >> prepare_dbt >> dbt_models  # type: ignore
