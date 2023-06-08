# Register your models here.
from django.contrib import admin

from apps.fakecsv.models import Column, DataSet, Schema


class ColumnInLine(admin.StackedInline):
    model = Column


@admin.register(Schema)
class SchemaAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "delimiter", "quote_character"]
    inlines = [ColumnInLine]


@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "data_type", "order", "data_range_from", "data_range_to"]


admin.site.register(DataSet)
