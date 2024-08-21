"""Collection of miscellaneous helper functions"""

from __future__ import annotations

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
