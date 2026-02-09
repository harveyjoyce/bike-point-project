with cte as (
    select * from {{ ref('stg_bike_point__parsed') }}
)

select 
    id,
    max(modified_timestamp) as update_time,
    bike_point_name,
    lat,
    lon,
    installed,
    locked,
    installdate,
    removaldate,
    temporary
from cte
group by all