import pytest
from .utils import generate_data_set
from .models import Schema, Column, DataSet
from django.core.files.storage import default_storage


@pytest.mark.django_db
def test_generate_data_set(column_model):
    schema = column_model.schema
    column = column_model

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

    assert default_storage.exists(filename) is True
