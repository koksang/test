"""Airflow constants"""

from __future__ import annotations


class Environment:
    production = "production"
    staging = "staging"


class TableSchema:
    chicago_taxi_trips__taxi_trips: list = [
        {"name": "unique_key", "type": "STRING", "mode": "REQUIRED"},
        {"name": "taxi_id", "type": "STRING", "mode": "NULLABLE"},
        {"name": "trip_start_timestamp", "type": "TIMESTAMP", "mode": "NULLABLE"},
        {"name": "trip_end_timestamp", "type": "TIMESTAMP", "mode": "NULLABLE"},
        {"name": "trip_seconds", "type": "INT64", "mode": "NULLABLE"},
        {"name": "trip_miles", "type": "FLOAT", "mode": "NULLABLE"},
        {"name": "pickup_census_tract", "type": "INT64", "mode": "NULLABLE"},
        {"name": "dropoff_census_tract", "type": "INT64", "mode": "NULLABLE"},
        {"name": "pickup_community_area", "type": "INT64", "mode": "NULLABLE"},
        {"name": "dropoff_community_area", "type": "INT64", "mode": "NULLABLE"},
        {"name": "fare", "type": "FLOAT", "mode": "NULLABLE"},
        {"name": "tips", "type": "FLOAT", "mode": "NULLABLE"},
        {"name": "tolls", "type": "FLOAT", "mode": "NULLABLE"},
        {"name": "extras", "type": "FLOAT", "mode": "NULLABLE"},
        {"name": "trip_total", "type": "FLOAT", "mode": "NULLABLE"},
        {"name": "payment_type", "type": "STRING", "mode": "NULLABLE"},
        {"name": "company", "type": "STRING", "mode": "NULLABLE"},
        {"name": "pickup_latitude", "type": "FLOAT", "mode": "NULLABLE"},
        {"name": "pickup_longitude", "type": "FLOAT", "mode": "NULLABLE"},
        {"name": "pickup_location", "type": "STRING", "mode": "NULLABLE"},
        {"name": "dropoff_latitude", "type": "FLOAT", "mode": "NULLABLE"},
        {"name": "dropoff_longitude", "type": "FLOAT", "mode": "NULLABLE"},
        {"name": "dropoff_location", "type": "STRING", "mode": "NULLABLE"},
    ]
