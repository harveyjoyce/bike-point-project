{{
    config(
        materialized='incremental'
        , incremental_strategy = 'append'
    )
}}

with source as (
    select * from {{ source('hj_des5_bike_point', 'raw_bike_point') }}
)

, json_parse as (
    select 
        raw_json:commonName::varchar as bike_point_name,
        raw_json:id::varchar as id,
        raw_json:lat::float as lat,
        raw_json:lon::float as lon,
        raw_json:additionalProperties::variant as nested_array,
        filename
    from source
)

, nested_array_parse as (
    select id,
        filename,
        bike_point_name,
        lat,
        lon,
        value:key::varchar as key,
        value:modified::varchar as modified_time,
        value:value::varchar as value
    from json_parse,
    lateral flatten(nested_array,outer=>true)
)


    select split_part(id,'_',2)::int as id,
            to_timestamp(split_part(filename,'.',1),'YYYY-mm-DD HH-MI-SS') as extract_timestamp,
            bike_point_name,
            lat,
            lon,
            to_timestamp(modified_time) as modified_timestamp,
            "'TerminalName'" as TerminalName,
            "'Installed'"::boolean as Installed,
            try_to_boolean("'Locked'") as Locked,
            try_to_date("'InstallDate'") as InstallDate,
            try_to_date("'RemovalDate'") as RemovalDate,
            "'Temporary'"::boolean as Temporary,
            "'NbBikes'"::int as NbBikes,
            "'NbEmptyDocks'"::int as NbEmptyDocks,
            "'NbDocks'"::int as NbDocks,
            "'NbStandardBikes'"::int as NbStandardBikes,
            "'NbEBikes'"::int as NbEBikes
    from nested_array_parse
    pivot(max(value) for key 
    in('TerminalName','Installed','Locked','InstallDate','RemovalDate','Temporary','NbBikes','NbEmptyDocks','NbDocks','NbStandardBikes','NbEBikes'))

{% if is_incremental() %}
    -- this filter will only be applied on an incremental run
    where extract_timestamp > (select coalesce(max(extract_timestamp),'1900-01-01') from {{ this }}) 
{% endif %}