"""
#### Summary
1. Load us annual public holidays into bigquery
"""

from __future__ import annotations

from datetime import timedelta
from pathlib import Path
from textwrap import dedent

from airflow.models import DAG
from airflow.operators.python import PythonOperator
from include.bigquery import load_df
from include.helpers import us_annual_public_holidays
from pendulum import datetime

DAG_ID = Path(__file__).stem
DATASET, TABLE = DAG_ID.split("__")
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
    schedule="0 0 1 1 *",
    catchup=False,
    params=PARAMS,
    default_args=DEFAULT_ARGS,
) as dag:
    load_us_holidays = PythonOperator(
        task_id="load_us_holidays",
        python_callable=load_df,
        op_kwargs=dict(df=us_annual_public_holidays(), table_id=f"{DATASET}.{TABLE}"),
    )
