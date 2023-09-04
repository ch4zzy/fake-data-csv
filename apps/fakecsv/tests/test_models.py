import pytest 
from apps.fakecsv.models import Schema, Column, DataSet


@pytest.mark.django_db
def test_schema_model(create_test_schema_models, schema_data_models):
    schema = create_test_schema_models
    schema_data = schema_data_models
    assert Schema.objects.count() == 1
    assert schema.name == schema_data["name"]
    assert schema.owner == schema_data["owner"]
    assert schema.delimiter == schema_data["delimiter"]
    assert schema.quote_character == schema_data["quote_character"]


@pytest.mark.django_db
def test_column_model(create_test_columns_models, column_data_models):
    column = create_test_columns_models
    column_data = column_data_models
    assert Schema.objects.count() == 1
    assert Column.objects.count() == 1
    assert column.name == column_data["name"]
    assert column.schema == column_data["schema"]
    assert column.data_type == column_data["data_type"]
    assert column.order == column_data["order"]
    if column_data["data_type"] != "integer":
        assert column.data_range_from is None
        assert column.data_range_to is None
    else:
        assert column.data_range_from == column_data["data_range_from"] 
        assert column.data_range_to == column_data["data_range_to"]


@pytest.mark.django_db
def test_dataset_model(create_test_data_set_models ,data_set_data_models):
    dataset = create_test_data_set_models
    data_set_data = data_set_data_models
    assert Schema.objects.count() == 1
    assert DataSet.objects.count() == 1
    assert dataset.status == data_set_data["status"]
    assert dataset.file == data_set_data["file"]
    assert dataset.schema == data_set_data["schema"]
    assert dataset.number_of_rows == data_set_data["number_of_rows"]


@pytest.mark.django_db
def test_user_model(create_test_user, user_data):
    user = create_test_user
    assert user.username == user_data["username"]
    assert user.email == user_data["email"]
    assert user.check_password(user_data["password"]) is True
