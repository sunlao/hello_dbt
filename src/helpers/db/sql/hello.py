class Hello:
    hello_count = "select count(*) from consumption.hello_world"

    hello_insert = (
        "INSERT INTO consumption.hello_world(col1, col2) VALUES (%(bv1)s, %(bv2)s)"
    )

    hello_postgres = "select 'hello_postgres'"

    hello_schema_count = """
select
count(*)
from
information_schema.schemata
where
schema_name in(
'consumption',
'working',
'stage',
'raw'
)
    """

    hello_select_value = "select * from consumption.hello_world where col1 = %(bv1)s"

    hello_select_many = "select * from consumption.hello_world order by col1"

    hello_truncate = "truncate table consumption.hello_world"

    hello_update = """
update consumption.hello_world
set
col2 = %(bv2)s
where
col1 = %(bv1)s
"""

    def get(self, p_name: str) -> str:
        return getattr(self, p_name)
