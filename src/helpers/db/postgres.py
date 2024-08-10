from psycopg2 import connect
from src.helpers.db.query import Query
from src.helpers.secrets import Secrets


class Postgres:
    def __init__(self, p_user_context):
        secrets = Secrets().db(p_user_context)
        self.connection = connect(
            dbname=secrets["DB_NAME"],
            host=secrets["HOST"],
            port=secrets["PORT"],
            user=secrets["USER"].lower(),
            password=secrets["SECRET"],
        )
        self.connection.set_session(autocommit=True)

    def execute(self, p_query_name: str, p_values=None) -> None:
        cursor_obj = self.connection.cursor()
        cursor_obj.execute(Query().get(p_query_name), p_values)
        return cursor_obj

    def execute_many(self, p_query_name: str, p_values=None) -> None:
        cursor_obj = self.connection.cursor()
        cursor_obj.executemany(Query().get(p_query_name), p_values)
        return cursor_obj

    def get_one(self, p_query_name: str, p_values=None) -> tuple:
        return self.execute(p_query_name, p_values).fetchone()
