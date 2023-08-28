import csv
import os
from datetime import datetime

import boto3
from django.core.files.storage import default_storage
from faker import Faker

from apps.fakecsv.constants import DataType, Status
from apps.fakecsv.models import DataSet, Schema


def fakedata_generator(data_type, value_range):
    fake_data = Faker()

    data_mapper = {
        DataType.FULL_NAME: fake_data.name,
        DataType.JOB: fake_data.job,
        DataType.EMAIL: fake_data.safe_email,
        DataType.DOMAIN_NAME: fake_data.domain_name,
        DataType.PHONE_NUMBER: fake_data.phone_number,
        DataType.COMPANY_NAME: fake_data.company,
        DataType.TEXT: fake_data.paragraph,
        DataType.INTEGER: fake_data.random_int,
        DataType.ADDRESS: fake_data.address,
        DataType.DATE: fake_data.date,
    }

    method = data_mapper[data_type]

    if data_type == DataType.TEXT:
        if value_range is None:
            result = method(nb_sentences=fake_data.random_int(min=1, max=10), variable_nb_sentences=False)
        else:
            result = method(nb_sentences=fake_data.random_int(*value_range), variable_nb_sentences=False)
    elif data_type == DataType.INTEGER:
        if value_range is None:
            result = method(0, 9999)
        else:
            result = method(*value_range)
    else:
        result = method()
    return result


def generate_data_set(schema: Schema, number_of_rows: int) -> None:
    """Method to generate dataset from schema"""
    dataset = DataSet.objects.create(schema=schema, number_of_rows=number_of_rows)

    csv.register_dialect(
        "custom",
        delimiter=schema.delimiter,
        quotechar=schema.quote_character,
        quoting=csv.QUOTE_ALL,
    )
    columns = schema.columns.all()

    filename = f"{schema.name}_{number_of_rows}_{datetime.now().isoformat()}.csv"
    with default_storage.open(os.path.join(filename), "w") as f:
        writer = csv.DictWriter(f, fieldnames=[c.name for c in columns], dialect="custom")
        writer.writeheader()
        for i in range(number_of_rows):
            row = dict()
            for column in columns:
                row[column.name] = fakedata_generator(
                    column.data_type,
                    value_range=(column.data_range_from, column.data_range_to),
                )
            writer.writerow(row)

    dataset.status = Status.READY
    dataset.file = filename
    dataset.save()
    return filename


def check_file_exists(bucket_name, file_key):
    s3 = boto3.client("s3")

    try:
        response = s3.head_object(Bucket=bucket_name, Key=file_key)
        return True
    except Exception:
        return False
