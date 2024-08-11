{% snapshot customer_snapshot %}

{{
    config(
      target_schema='snapshots',
      unique_key='id',

      strategy='check',
      check_cols = 'all',
    )
}}

select * from {{ ref('raw_customers') }}

{% endsnapshot %}