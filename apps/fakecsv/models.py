from django.contrib.auth.models import User
from django.db import models

from .constants import DataType, Delimiter, QuoteCharacter, Status


class Schema(models.Model):
    """
    Model representing a schema for a CSV file.
    """

    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    delimiter = models.CharField(
        max_length=1,
        choices=Delimiter.choices,
        default=Delimiter.COMMA,
    )
    quote_character = models.CharField(
        max_length=1,
        choices=QuoteCharacter.choices,
        default=QuoteCharacter.DOUBLE_QUOTE,
    )


class Column(models.Model):
    """
    Model representing a column within a schema for a CSV file.
    """

    name = models.CharField(max_length=100)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, related_name="columns")
    data_type = models.CharField(max_length=12, choices=DataType.choices)
    order = models.PositiveIntegerField()
    data_range_from = models.IntegerField(blank=True, null=True, verbose_name="from")
    data_range_to = models.IntegerField(blank=True, null=True, verbose_name="to")


class DataSet(models.Model):
    """
    Model representing a dataset (CSV file) associated with a schema.
    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PROCESSING)
    file = models.FileField(null=True, blank=True)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, related_name="data_sets")
    number_of_rows = models.PositiveIntegerField()
