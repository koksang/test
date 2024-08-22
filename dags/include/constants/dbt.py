"""Dbt constants"""

from __future__ import annotations

import os
from pathlib import Path

from airflow.configuration import conf
from cosmos import ExecutionConfig, ExecutionMode, ProfileConfig, ProjectConfig
from cosmos.constants import InvocationMode
from include.constants.airflow import Environment
from include.helpers import airflow_environment


class DbtTarget:
    production = Environment.production
    staging = Environment.staging


DBT_IMAGE = "ghcr.io/dbt-labs/dbt-bigquery:1.8.2"
DBT_PROJECT_DIR = os.environ.get(
    "DBT_PROJECT_DIR",
    Path(conf.get(section="core", key="dags_folder"), "..", "dbt"),
)
DBT_PROFILES_DIR = os.environ.get(
    "DBT_PROFILES_DIR",
    Path(conf.get(section="core", key="dags_folder"), "..", "dbt"),
)
PROFILE_CONFIG = ProfileConfig(
    profile_name="main",
    target_name=getattr(DbtTarget, airflow_environment()),
    profiles_yml_filepath=Path(DBT_PROFILES_DIR, "profiles.yml"),
)
PROJECT_CONFIG = ProjectConfig(dbt_project_path=DBT_PROJECT_DIR)
EXECUTION_CONFIG = ExecutionConfig(
    execution_mode=ExecutionMode.LOCAL,
    invocation_mode=InvocationMode.DBT_RUNNER,
)
