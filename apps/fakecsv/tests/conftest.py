import pytest
from django.contrib.auth import get_user_model
from fakecsv.models import Schema, Column, DataSet


@pytest.fixture
def user_data():
    return {
        "username": "test_user",
        "password": "test_password",
        "email": "test@t.com",
    }


@pytest.fixture
def schema_data(user):
    return {
        "name": "test_schema",
        "owner": user.id,
        "delimiter": ",",
        "quote_character": '"',
    }


@pytest.fixture
def column_data(schema):
    return {
        "name": "test_column",
        "schema": schema,
        "data_type": "FULL_NAME",
        "order": 1,
    }


@pytest.fixture
def data_set_data(schema):
    return {
        "status": "PROCESSING",
        "file": "",
        "schema": schema,
        "number_of_rows": 10,
    }


@pytest.fixture
def schema_data_models(user):
    return {
        "name": "test_schema",
        "owner": user,
        "delimiter": ",",
        "quote_character": '"',
    }


@pytest.fixture
def column_data_models(schema_model):
    return {
        "name": "test_column",
        "schema": schema_model,
        "data_type": "full_name",
        "order": 1,
    }


@pytest.fixture
def data_set_data_models(schema_model):
    return {
        "status": "PROCESSING",
        "file": "",
        "schema": schema_model,
        "number_of_rows": 10,
    }


@pytest.fixture
def user(user_data):
    user = get_user_model().objects.create_user(**user_data)
    user.set_password(user_data["password"])
    return user


@pytest.fixture
def authenticated_user(client, user, user_data):
    client.login(**user_data)
    return client


@pytest.fixture
def schema(schema_data):
    return Schema.objects.create(**schema_data)


@pytest.fixture
def column(column_data):
    return Column.objects.create(**column_data)


@pytest.fixture
def data_set(data_set_data):
    return DataSet.objects.create(**data_set_data)


@pytest.fixture
def schema_model(schema_data_models):
    return Schema.objects.create(**schema_data_models)


@pytest.fixture
def column_model(column_data_models):
    return Column.objects.create(**column_data_models)


@pytest.fixture
def data_set_model(data_set_data_models):
    return DataSet.objects.create(**data_set_data_models)
