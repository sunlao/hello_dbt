{{ 
    config(
        materialized="table",
        schema="stage")
}}

select distinct 
id,first_name,last_name, 'init' load_type
from 
{{ref('raw_customers')}}