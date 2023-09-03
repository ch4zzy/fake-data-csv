import pytest
import datetime
from django.contrib.auth import get_user_model
from apps.fakecsv.models import Schema, Column, DataSet
from apps.fakecsv.constants import DataType, Delimiter, QuoteCharacter, Status


@pytest.fixture
def user_data():
    return {
        "username": "test_user",
        "password": "test_password",
        "email": "test@t.com",
    }


@pytest.fixture
def schema_data(create_test_user):
    return {
        "name": "test_schema",
        "owner": create_test_user.id,
        "delimiter": ",",
        "quote_character": '"',
    }


@pytest.fixture
def column_data(create_test_schema):
    return {
        "name": "test_column",
        "schema": create_test_schema,
        "data_type": "FULL_NAME",
        "order": 1,
    }


@pytest.fixture
def data_set_data(create_test_schema):
    return {
        "status": "PROCESSING",
        "file": "",
        "schema": create_test_schema,
        "number_of_rows": 10,
    }


@pytest.fixture
def schema_data_models(create_test_user):
    return {
        "name": "test_schema",
        "owner": create_test_user,
        "delimiter": ",",
        "quote_character": '"',
    }


@pytest.fixture
def column_data_models(create_test_schema):
    return {
        "name": "test_column",
        "schema": create_test_schema,
        "data_type": "FULL_NAME",
        "order": 1,
    }


@pytest.fixture
def data_set_data_models(create_test_schema):
    return {
        "status": "PROCESSING",
        "file": "",
        "schema": create_test_schema,
        "number_of_rows": 10,
    }


@pytest.fixture
def create_test_user(user_data):
    user = get_user_model().objects.create_user(**user_data)
    user.set_password(user_data["password"])
    return user


@pytest.fixture
def authenticated_user(client, create_test_user, user_data):
    client.login(**user_data)
    return client


@pytest.fixture
def create_test_schema(schema_data_models):
    return Schema.objects.create(**schema_data_models)


@pytest.fixture
def create_test_schema_with_columns(column_data):
    return Column.objects.create(**column_data)


@pytest.fixture
def create_test_data_set(data_set_data):
    return DataSet.objects.create(**data_set_data)


@pytest.fixture
def create_test_schema_models(schema_data_models):
    return Schema.objects.create(**schema_data_models)


@pytest.fixture
def create_test_columns_models(column_data_models):
    return Column.objects.create(**column_data_models)


@pytest.fixture
def create_test_data_set_models(data_set_data_models):
    return DataSet.objects.create(**data_set_data_models)
