from django import forms

from apps.fakecsv.models import Column, DataSet, Schema


class SchemaForm(forms.ModelForm):
    """
    Form for creating or updating a Schema.
    """

    class Meta:
        model = Schema
        fields = (
            "owner",
            "name",
            "delimiter",
            "quote_character",
        )

        widgets = {
            "owner": forms.HiddenInput(),
            "name": forms.TextInput(),
            "delimiter": forms.Select(),
            "quote_character": forms.Select(),
        }


class ColumnForm(forms.ModelForm):
    """
    Form for creating or updating a Column for Schema.
    """

    class Meta:
        model = Column
        exclude = ("id",)
        fields = (
            "name",
            "order",
            "data_type",
            "data_range_from",
            "data_range_to",
        )

        widgets = {
            "name": forms.TextInput(),
            "order": forms.NumberInput(),
            "data_type": forms.Select(),
            "data_range_from": forms.NumberInput(),
            "data_range_to": forms.NumberInput(),
        }


class DataSetForm(forms.ModelForm):
    """
    Form for creating or updating DataSet.
    """

    class Meta:
        model = DataSet
        fields = "__all__"
