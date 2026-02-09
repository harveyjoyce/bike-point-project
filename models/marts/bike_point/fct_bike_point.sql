{{
    config(
        materialized='incremental'
        , incremental_strategy = 'append'
    )
}}

with cte as (
    select * from {{ ref('stg_bike_point__parsed') }}
)

select id,
    extract_timestamp,
    modified_timestamp,
    NbBikes,
    NbEmptyDocks,
    NbDocks,
    NbStandardBikes,
    NbEBikes
from cte

{% if is_incremental() %}
    -- this filter will only be applied on an incremental run
    where extract_timestamp > (select coalesce(max(extract_timestamp),'1900-01-01') from {{ this }}) 
{% endif %}