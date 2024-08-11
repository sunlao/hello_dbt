{{ 
    config(
        materialized="table",
        schema="stage")
}}

select distinct 
id,first_name,last_name, 'new' load_type
from 
{{ref('raw_customers_new')}}
