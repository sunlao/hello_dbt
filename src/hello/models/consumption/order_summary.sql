{{ config(
    materialized="table",
    schema="consumption")
}}


select 
{{ dbt_utils.generate_surrogate_key(["a.id", "c.id"]) }} as order_summary_pk,
a.id::int                       order_id, 
a.order_date::date              order_date, 
a.status::varchar(10)           order_status, 
b.first_name::varchar(100)      first_name, 
b.last_name::varchar(100)       last_name,
c.amount::numeric(9,0)          amount,
c.payment_method::varchar(100)  payment_method
from 
{{ref('raw_orders')}} a
	left join {{ref('raw_customers')}} b on a.user_id =b.id 
	left join {{ref('raw_payments')}} c on a.id = c.order_id 
where c.amount > 0  