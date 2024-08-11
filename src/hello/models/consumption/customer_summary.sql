{{ config(
    materialized="incremental",
    unique_key = 'source_id',
    schema="consumption")
}}

select 
md5(source_id::text)::uuid          dwh_pk,
source_id,
first_name::varchar(100)            first_name, 
last_name::varchar(100)             last_name,
dwh_create_user::varchar(100)       dwh_create_user,
dwh_create_ts::timestamp            dwh_create_ts,
dwh_update_user::varchar(100)       dwh_update_user,
dwh_update_ts::timestamp            dwh_update_ts,
dwh_delete_flag::boolean            dwh_delete_flag
from (
    -- Select new records
    select 
    a.id            source_id,
    first_name,
    last_name,
    user            dwh_create_user,
    now()           dwh_create_ts,
    null            dwh_update_user,
    null            dwh_update_ts,
    null::boolean   dwh_delete_flag
    from
    {{ref('customers')}} a
    {% if is_incremental() %}
	    join (
	            select id from {{ref('customers')}} where load_type != 'delete' and max_delete_count = 0
	            except
	            select source_id from {{ this }}
            ) b on a.id = b.id

        union all 

        -- Select update records
        select 
        a.id, 
        a.first_name,
        a.last_name,
        b.dwh_create_user,
        b.dwh_create_ts,
        user  dwh_update_user,
        now() dwh_update_ts,
        null::boolean  dwh_delete_flag
        from
        {{ref('customers')}} a
            join {{ this }} b on a.id = b.source_id
        where 
            a.first_name != b.first_name
        or
            a.last_name != b.last_name
        and a.load_type != 'delete'
        and a.max_delete_count = 0

        union all 

        -- Select delete records
        select 
        a.id, 
        a.first_name,
        a.last_name,
        b.dwh_create_user,
        b.dwh_create_ts,
        user                dwh_update_user,
        now()               dwh_update_ts,
        true                dwh_delete_flag
        from
        {{ref('customers')}} a
            join {{ this }} b on a.id = b.source_id
        where 
        a.load_type = 'delete'
    {% endif %}
)a