from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from apps.fakecsv.constants import Status
from apps.fakecsv.forms import ColumnForm, DataSet, DataSetForm, SchemaForm
from apps.fakecsv.models import Column, Schema
from apps.fakecsv.utils import check_file_exists, generate_data_set


@login_required
def schema_list(request):
    """
    View for displaying a list of schemas owned by the user.
    """
    user = request.user
    schema = Schema.objects.filter(owner=user.id)
    return render(
        request,
        "fakecsv/schema/schema_list.html",
        {
            "schema": schema,
        },
    )


@login_required
def create_schema(request):
    """
    View for creating a new schema for a CSV file.
    """
    if request.method == "POST":
        form = SchemaForm(request.POST)
        if form.is_valid():
            schema = form.save(commit=False)
            schema.owner = request.user
            schema.save()
            if "action" in request.POST:
                if request.POST["action"] == "submit":
                    return redirect("fakecsv:schema_list")
                if request.POST["action"] == "add_column":
                    column = Column(schema=schema)
                    column.save()
                    return redirect("fakecsv:edit_column", pk=column.pk)
            else:
                return redirect("fakecsv:schema_list")
        else:
            return render(
                request,
                "fakecsv/schema/new_schema.html",
                {
                    "form": form,
                    "error_message": "Form is not valid",
                },
            )
    else:
        form = SchemaForm(initial={"owner": request.user})

    return render(
        request,
        "fakecsv/schema/new_schema.html",
        {
            "form": form,
        },
    )


@login_required
def delete_schema(request, pk):
    """
    View for deleting a schema for a CSV file.
    """
    schema = get_object_or_404(Schema, pk=pk, owner=request.user)
    schema.delete()
    return redirect("fakecsv:schema_list")


@login_required
def delete_column(request, pk):
    """
    View for deleting a column in a CSV file schema.
    """
    column = get_object_or_404(Column, pk=pk)
    column.delete()
    return redirect("fakecsv:schema_list")


@login_required
def edit_schema(request, pk):
    """
    View for editing a schema for a CSV file.
    """
    schema = Schema.objects.select_related("owner").get(pk=pk)
    ColumnFormSet = inlineformset_factory(Schema, Column, form=ColumnForm, extra=1, can_delete=True)
    formset_prefix = "column"
    if request.method == "POST":
        form = SchemaForm(request.POST, instance=schema)
        formset = ColumnFormSet(request.POST, instance=schema, prefix=formset_prefix)

        if form.is_valid() and formset.is_valid():
            if "action" in request.POST and request.POST["action"] == "submit":
                form.save()
                formset.save()
                return redirect("fakecsv:edit_schema", pk=schema.pk)
    else:
        form = SchemaForm(instance=schema)
        formset = ColumnFormSet(instance=schema, prefix=formset_prefix)

    context = {
        "form": form,
        "formset": formset,
    }
    return render(request, "fakecsv/schema/new_schema.html", context)


@login_required
def detail_schema(request, pk):
    """
    View for displaying details of a schema for a CSV file.
    """
    try:
        schema = Schema.objects.select_related("owner").get(pk=pk)
    except Schema.DoesNotExist:
        return redirect("fakecsv:schema_list")
    column = schema.columns.all().order_by("order")
    form = DataSetForm()
    dataset = schema.data_sets.all()
    if request.method == "POST":
        form = DataSetForm(request.POST, instance=schema)
        if form.is_valid():
            if "action" in request.POST and request.POST["action"] == "submit":
                dataset = form.save(commit=False)
                dataset.schema = schema
                dataset.status = Status.PROCESSING
                dataset.save()
                number_of_rows = form.cleaned_data["number_of_rows"]

                filename = generate_data_set(schema, number_of_rows=number_of_rows)
                file_key = "media/" + filename
                file_exists = check_file_exists(settings.AWS_STORAGE_BUCKET_NAME, file_key)

                if not file_exists:
                    return HttpResponse("File does not exist", status=404)
                return redirect("fakecsv:detail_schema", pk=schema.pk)
    else:
        initial_data = {
            "schema": schema,
            "status": Status.PROCESSING,
        }
        form = DataSetForm(initial=initial_data)

    context = {
        "schema": schema,
        "column": column,
        "form": form,
        "dataset": dataset,
    }

    return render(request, "fakecsv/schema/schema_detail.html", context)


@login_required
def download_data_set(request, data_set_id):
    """
    View for downloading a generated dataset for a CSV file.
    """
    data_set = get_object_or_404(DataSet, id=data_set_id)
    file_path = data_set.file.path

    with open(file_path, "rb") as f:
        response = HttpResponse(f.read(), content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={slugify(data_set.schema.name)}.csv"
        return response
