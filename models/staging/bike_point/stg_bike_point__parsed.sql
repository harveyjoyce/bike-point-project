{{
    config(
        materialized='incremental'
        , incremental_strategy = 'append'
    )
}}

with 

source as (

    select * from {{ ref('base_bike_point__parsed') }}

),

renamed as (

    select
        ID,
        EXTRACT_TIMESTAMP,
        BIKE_POINT_NAME,
        LAT,
        LON,
        MODIFIED_TIMESTAMP,
        TERMINALNAME,
        INSTALLED,
        LOCKED,
        INSTALLDATE,
        REMOVALDATE,
        TEMPORARY,
        NBBIKES,
        NBEMPTYDOCKS,
        NBDOCKS,
        NBSTANDARDBIKES,
        NBEBIKES
    from source

)

select * from renamed

{% if is_incremental() %}
    -- this filter will only be applied on an incremental run
    where extract_timestamp > (select coalesce(max(extract_timestamp),'1900-01-01') from {{ this }}) 
{% endif %}