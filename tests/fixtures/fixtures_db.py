from pytest import fixture
from src.helpers.db.postgres import Postgres


@fixture
def db():
    return Postgres
