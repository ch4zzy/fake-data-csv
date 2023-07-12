import csv
import os
from datetime import datetime

import boto3
from django.core.files.storage import default_storage
from django.test import TestCase
from faker import Faker
from unittest import mock
from django.contrib.auth.models import User

from apps.fakecsv.constants import DataType, Status
from apps.fakecsv.models import DataSet, Schema
from apps.fakecsv.utils import fakedata_generator, generate_data_set, check_file_exists


class FakeCSVUtilsTestCase(TestCase):

    def setUp(self):
        self.fake = Faker()
        self.user = User.objects.create(username="test_user")


    def test_fakedata_generator(self):
        # Test a few data types
        name = fakedata_generator(DataType.FULL_NAME, None)
        self.assertTrue(isinstance(name, str))

        job = fakedata_generator(DataType.JOB, None)
        self.assertTrue(isinstance(job, str))

        email = fakedata_generator(DataType.EMAIL, None)
        self.assertTrue(isinstance(email, str))

        domain = fakedata_generator(DataType.DOMAIN_NAME, None)
        self.assertTrue(isinstance(domain, str))

        phone = fakedata_generator(DataType.PHONE_NUMBER, None)
        self.assertTrue(isinstance(phone, str))

        company = fakedata_generator(DataType.COMPANY_NAME, None)
        self.assertTrue(isinstance(company, str))

        text = fakedata_generator(DataType.TEXT, (1, 5))
        self.assertTrue(isinstance(text, str))

        integer = fakedata_generator(DataType.INTEGER, (10, 20))
        self.assertTrue(isinstance(integer, int))

        address = fakedata_generator(DataType.ADDRESS, None)
        self.assertTrue(isinstance(address, str))

        date = fakedata_generator(DataType.DATE, None)
        self.assertTrue(isinstance(date, str))


    @mock.patch('apps.fakecsv.utils.default_storage')
    @mock.patch('apps.fakecsv.utils.csv.DictWriter')
    def test_generate_data_set(self, mock_csv_writer, mock_default_storage):
        schema = Schema.objects.create(name='Test Schema', delimiter=',', quote_character='"', owner=self.user)
        column1 = schema.columns.create(name='Column1', data_type=DataType.FULL_NAME, order=0)
        column2 = schema.columns.create(name='Column2', data_type=DataType.EMAIL, order=1)

        number_of_rows = 5
        filename = generate_data_set(schema, number_of_rows)

        self.assertEqual(DataSet.objects.count(), 1)
        dataset = DataSet.objects.first()
        self.assertEqual(dataset.schema, schema)
        self.assertEqual(dataset.number_of_rows, number_of_rows)
        self.assertEqual(dataset.status, Status.READY)
        self.assertEqual(dataset.file, filename)

        mock_csv_writer.assert_called_once_with(
            mock_default_storage.open.return_value.__enter__.return_value,
            fieldnames=[column1.name, column2.name],
            dialect='custom'
        )

        writer_instance = mock_csv_writer.return_value.__enter__.return_value


    @mock.patch('apps.fakecsv.utils.boto3.client')
    def test_check_file_exists(self, mock_boto3_client):
        bucket_name = 'test-bucket'
        file_key = 'test-file.csv'

        # Test when file exists
        mock_boto3_client.return_value.head_object.return_value = {}
        exists = check_file_exists(bucket_name, file_key)
        self.assertTrue(exists)

        # Test when file does not exist
        mock_boto3_client.return_value.head_object.side_effect = Exception()
        exists = check_file_exists(bucket_name, file_key)
        self.assertFalse(exists)
