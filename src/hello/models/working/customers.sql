{{ 
    config(
        materialized="table",
        schema="working")
}}

select 
id, 
first_name, last_name, load_type,
max(delete_count) over(partition by id) max_delete_count
from(
    select 
    id, first_name::text first_name, last_name::text last_name,  'init' load_type, 0 delete_count
    from 
    {{ref('customers_init')}}    

    union 

    select 
    id, first_name::text, last_name::text, 'new' load_type, 0 delete_count
    from 
    {{ref('customers_new')}}

    union

    select 
    id, first_name::text, last_name::text, 'delete' load_type, 1 delete_count
    from 
    {{ref('customers_delete')}}

    union

    select 
    id, first_name::text, last_name::text, 'update' load_type, 0 delete_count
    from 
    {{ref('customers_update')}}
)a