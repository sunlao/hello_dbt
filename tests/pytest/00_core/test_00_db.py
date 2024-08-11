from psycopg2.errors import InsufficientPrivilege
from pytest import raises
from src.helpers.db.models import DatabaseUserContext
from tests.fixtures.fixtures_db import db


def test_hello_postgres_app(db):
    row = db(DatabaseUserContext.APP).get_one("hello_postgres")
    assert row[0] == "hello_postgres"


def test_app_fail(db):
    with raises(InsufficientPrivilege):
        db(DatabaseUserContext.APP).get_one("hello_count")


def test_truncate_hello_world(db):
    db(DatabaseUserContext.DATA).execute("hello_truncate")
    row = db(DatabaseUserContext.DATA).get_one("hello_count")
    assert row[0] == 0


def test_hello_insert_one(db):
    values = {"bv1": "abc", "bv2": 123}
    db(DatabaseUserContext.DATA).execute("hello_insert", values)
    row = db(DatabaseUserContext.DATA).get_one("hello_count")
    assert row[0] == 1


def test_hello_insert_many(db):
    values = ({"bv1": "def", "bv2": 456}, {"bv1": "ghi", "bv2": 789})
    db(DatabaseUserContext.DATA).execute_many("hello_insert", values)
    row = db(DatabaseUserContext.DATA).get_one("hello_count")
    assert row[0] == 3


def test_hello_select_value(db):
    values = {"bv1": "abc"}
    row = db(DatabaseUserContext.DATA).get_one("hello_select_value", values)
    assert row == (values["bv1"], 123)


def test_hello_update_one(db):
    values = {"bv1": "abc", "bv2": 999}
    db(DatabaseUserContext.DATA).execute("hello_update", values)
    row = db(DatabaseUserContext.DATA).get_one("hello_select_value", values)
    assert row == (values["bv1"], 999)


def test_hello_schema_count(db):
    row = db(DatabaseUserContext.DATA).get_one("hello_schema_count")
    assert row[0] == 4
