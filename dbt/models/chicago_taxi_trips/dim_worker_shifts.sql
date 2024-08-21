{{
    config(materialized="table")
}}

with fct_taxi_trips as (

    select * from {{ ref("fct_taxi_trips") }}

)

select

    taxi_id
    , date(trip_start_timestamp) as shift
    , sum(trip_seconds) as shift_total_trip_seconds
    , min(trip_start_timestamp) as shift_start_timestamp
    , max(trip_end_timestamp) as shift_end_timestamp

from
    fct_taxi_trips

group by
    1, 2