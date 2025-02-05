with fct_worker_shifts as (

    select * from {{ ref("fct_worker_shifts") }}

)

select

    taxi_id
    , shift
    , shift_total_earnings

from
    fct_worker_shifts

where
    shift_end_timestamp <= timestamp(date_add(current_date(), interval -3 month))

order by
    2 desc

limit
    100
