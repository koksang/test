"""Dbt constants"""

from __future__ import annotations

import os
from pathlib import Path

from airflow.configuration import conf
from cosmos import ProfileConfig
from include.constants.airflow import Environment


class DbtTarget:
    production = Environment.production
    staging = Environment.staging


DBT_IMAGE = "ghcr.io/dbt-labs/dbt-bigquery:1.8.2"
DBT_PROJECT_DIR = DBT_PROFILES_DIR = os.environ.get(
    "DBT_PROFILES_DIR",
    Path(conf.get(section="core", key="dags_folder"), "..", "dbt"),
)
PROFILE_CONFIG = ProfileConfig(
    profile_name="main",
    target_name=DbtTarget.production,
    profiles_yml_filepath=Path(DBT_PROFILES_DIR, "profiles.yml"),
)
