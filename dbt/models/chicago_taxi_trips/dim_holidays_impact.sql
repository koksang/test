with dim_worker_shifts as (

    select * from {{ ref("dim_worker_shifts") }}

)

, us_holidays as (

    select * from {{ source("common", "us_holidays") }}

)

select 

    holidays.date as holiday_date
    , holidays.name as holiday_name
    , count(shifts.taxi_id) as number_of_trips

from
    us_holidays as holidays
left join 
    dim_worker_shifts as shifts
on 
    shifts.shift = holidays.date
group by
    1, 2
order by
    1