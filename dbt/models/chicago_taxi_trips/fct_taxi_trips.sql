with taxi_trips as (

    select * from {{ source("chicago_taxi_trips", "taxi_trips") }}

)

select

    unique_key
    , taxi_id
    , trip_start_timestamp
    , trip_end_timestamp
    , trip_seconds
    , trip_miles
    , pickup_census_tract
    , dropoff_census_tract
    , pickup_community_area
    , dropoff_community_area
    , fare
    , tips
    , tolls
    , extras
    , trip_total
    , payment_type
    , company
    , pickup_latitude
    , pickup_longitude
    , pickup_location
    , dropoff_latitude
    , dropoff_longitude
    , dropoff_location
    , date(trip_start_timestamp) as shift

from
    taxi_trips
