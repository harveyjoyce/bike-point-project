with fct_bike_point as (
    select * from {{ ref('fct_bike_point') }}
)

, dim_bike_point_snapshot as (
    select * from {{ ref('dim_bike_point_snapshot') }}
),


current_status as (
    select *
    from fct_bike_point
    qualify extract_timestamp = max(extract_timestamp) over(partition by id)
)
 
select
    c.id,
    bike_point_name,
    nbdocks,
    nbdocks - (nbemptydocks + nbbikes) as nbbrokendocks,
    lat,
    lon,
    update_time,
    installdate
from current_status c
    inner join dim_bike_point_snapshot d on c.id = d.id
    and c.extract_timestamp >= d.dbt_valid_from
    and c.extract_timestamp <= d.dbt_valid_to
where nbdocks != (nbemptydocks + nbbikes)