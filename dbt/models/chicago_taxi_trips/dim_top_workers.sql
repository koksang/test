with fct_worker_shifts as (

    select * from {{ ref("fct_worker_shifts") }}

)

select 

    taxi_id
    , round(
        avg(timestamp_diff(shift_end_timestamp, shift_start_timestamp, minute)), 1
    ) as avg_shift_period_minutes


from
    fct_worker_shifts

where
    shift_total_trip_seconds > (16 * 60 * 60) -- 24 - 8hours of sleep

group by
    1

order by
    2 desc

limit 
    100