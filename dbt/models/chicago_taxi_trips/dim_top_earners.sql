with fct_taxi_trips as (

    select * from {{ ref("fct_taxi_trips") }}

)

select 

    taxi_id
    , sum(trip_total) as earnings

from
    fct_taxi_trips

where
    trip_end_timestamp <= timestamp(date_add(current_date(), interval -3 month))

group by 
    1
order by 
    2 desc
limit 
    100