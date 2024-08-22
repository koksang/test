"""Collection of miscellaneous helper functions"""

from __future__ import annotations

import logging
import os
from datetime import datetime

import holidays
import pandas as pd
from airflow.models import Variable
from include.constants.airflow import Environment


def airflow_environment(
    env_key: str = "AIRFLOW_ENVIRONMENT", airflow_variable: str = "AIRFLOW_ENVIRONMENT"
) -> str:
    """Retrieve airflow environment using airflow Variable or env variable

    Args:
        env_key (str, optional): Environment key to set on airflow. Defaults to "AIRFLOW_ENVIRONMENT".
        airflow_key (str, optional): Airflow variable name to retrieve environment. Defaults to "AIRFLOW_ENVIRONMENT".

    Returns:
        str | None: Current airflow environment
    """

    if env_key not in os.environ:
        os.environ[env_key] = getattr(
            Environment, Variable.get(airflow_variable, Environment.staging).lower()
        )

    return os.environ.get(env_key, Environment.staging)


def us_annual_public_holidays(year: int = datetime.now().year) -> pd.DataFrame:
    """Get us annual public holidays

    Args:
        year (int, optional): year. Defaults to datetime.now().year.

    Returns:
        pd.DataFrame: dataframe of us annual public holidays
    """
    us_holidays = holidays.US(years=year)
    public_holidays = dict(
        date=list(us_holidays.keys()),
        name=list(us_holidays.values()),
    )

    return pd.DataFrame(public_holidays)


def check_table_exists(
    dataset_id: str,
    table_id: str,
    success_task_id: str,
    failure_task_id: str,
    project_id: str = os.environ["PROJECT_ID"],
) -> str:
    from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook

    if BigQueryHook().table_exists(
        project_id=project_id, dataset_id=dataset_id, table_id=table_id
    ):
        return success_task_id
    else:
        return failure_task_id


def task_fail_alert(context) -> None:
    """Task failure callback

    Args:
        context (dict): Airflow context
    """
    # NOTE: send alert message to channels like email or slack
    logging.error(
        f"""
    :red_circle: Task Failed - Alert.
    *Task*: {context.get('task_instance').task_id}
    *Dag*: {context.get('task_instance').dag_id}
    *Execution Time*: {context.get('execution_date')}
    """
    )
