from __future__ import annotations

import logging

import pandas as pd
from google.cloud import bigquery


def load_df(
    df: pd.DataFrame,
    table_id: str,
    schema: list[bigquery.SchemaField] | None = None,
    write_disposition: str = "WRITE_TRUNCATE",
) -> None:
    client = bigquery.Client()
    if schema:
        job_config = bigquery.LoadJobConfig(
            schema=schema,
            write_disposition=write_disposition,
        )
    else:
        job_config = bigquery.LoadJobConfig(write_disposition=write_disposition)

    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()

    table = client.get_table(table_id)
    logging.info(
        f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}"
    )
