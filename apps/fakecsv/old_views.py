# old views
# all this views now are class based views
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import SchemaForm
from .models import Schema, Column
from django.forms import inlineformset_factory
from .forms import ColumnForm
from .constants import Status
from .forms import DataSetForm
from .utils import generate_data_set, check_file_exists
from django.conf import settings
from django.http import HttpResponse


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
