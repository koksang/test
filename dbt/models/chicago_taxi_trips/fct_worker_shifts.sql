{{
    config(
        materialized="incremental", 
        unique_key="unique_key"
    )
}}

with fct_taxi_trips as (

    select * from {{ ref("fct_taxi_trips") }}

)

select

    unique_key
    , taxi_id
    , shift
    , min(trip_start_timestamp) as shift_start_timestamp
    , max(trip_end_timestamp) as shift_end_timestamp
    , sum(trip_seconds) as shift_total_trip_seconds
    , sum(trip_total) as shift_total_earnings

from
    fct_taxi_trips

{% if is_incremental() %}

where shift >= ( select max(shift) from {{ this }} )

{% endif %}

group by
    1, 2, 3