import pytest
from apps.fakecsv.utils import generate_data_set
from apps.fakecsv.models import Schema, Column, DataSet


@pytest.mark.django_db
def test_generate_data_set(create_test_columns_models):
    schema = create_test_columns_models.schema
    column = create_test_columns_models

    assert Schema.objects.count() == 1
    assert Column.objects.count() == 1

    number_of_rows = 10

    filename = generate_data_set(schema, number_of_rows)

    dataset = DataSet.objects.first()
    assert DataSet.objects.count() == 1
    assert dataset is not None
    assert dataset.status == "Ready"
    assert dataset.number_of_rows == number_of_rows
    assert dataset.schema == schema
    assert dataset.file == filename


