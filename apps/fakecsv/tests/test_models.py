from django.test import TestCase
from django.contrib.auth.models import User
from apps.fakecsv.models import Schema, Column, DataSet
from apps.fakecsv.constants import DataType, Delimiter, QuoteCharacter, Status


class SchemaModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")
        self.schema = Schema.objects.create(
            name="Test Schema",
            owner=self.user,
            delimiter=Delimiter.COMMA,
            quote_character=QuoteCharacter.DOUBLE_QUOTE,
        )

    def test_schema_creation(self):
        self.assertEqual(self.schema.name, "Test Schema")
        self.assertEqual(self.schema.owner, self.user)
        self.assertEqual(self.schema.delimiter, Delimiter.COMMA)
        self.assertEqual(self.schema.quote_character, QuoteCharacter.DOUBLE_QUOTE)


class ColumnModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")
        self.schema = Schema.objects.create(
            name="Test Schema",
            owner=self.user,
            delimiter=Delimiter.COMMA,
            quote_character=QuoteCharacter.DOUBLE_QUOTE,
        )
        self.column = Column.objects.create(
            name="Test Column",
            schema=self.schema,
            data_type=Status.PROCESSING,
            order=1,
            data_range_from=1,
            data_range_to=10,
        )

    def test_column_creation(self):
        self.assertEqual(self.column.name, "Test Column")
        self.assertEqual(self.column.schema, self.schema)
        self.assertEqual(self.column.data_type, Status.PROCESSING)
        self.assertEqual(self.column.order, 1)
        self.assertEqual(self.column.data_range_from, 1)
        self.assertEqual(self.column.data_range_to, 10)


class DataSetModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")
        self.schema = Schema.objects.create(
            name="Test Schema",
            owner=self.user,
            delimiter=Delimiter.COMMA,
            quote_character=QuoteCharacter.DOUBLE_QUOTE,
        )
        self.dataset = DataSet.objects.create(
            schema=self.schema,
            number_of_rows=100,
        )

    def test_dataset_creation(self):
        self.assertEqual(self.dataset.schema, self.schema)
        self.assertEqual(self.dataset.number_of_rows, 100)
        self.assertEqual(self.dataset.status, Status.PROCESSING)
        self.assertFalse(self.dataset.file)
