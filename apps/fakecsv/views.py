from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import CreateView, ListView, UpdateView, View

from .constants import Status
from .forms import ColumnForm, DataSet, DataSetForm, SchemaForm
from .models import Column, Schema
from .utils import check_file_exists, generate_data_set


class SchemaListView(LoginRequiredMixin, ListView):
    model = Schema
    template_name = "fakecsv/schema/schema_list.html"
    context_object_name = "schema"

    def get_queryset(self):
        return Schema.objects.filter(owner=self.request.user)


class CreateSchemaView(LoginRequiredMixin, CreateView):
    model = Schema
    form_class = SchemaForm
    template_name = "fakecsv/schema/new_schema.html"
    success_url = reverse_lazy("fakecsv:schema_list")

    def get_initial(self):
        initial = super().get_initial()
        initial["owner"] = self.request.user
        return initial

    def form_valid(self, form):
        super().form_valid(form)
        return redirect(self.success_url)


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


class EditSchemaView(LoginRequiredMixin, UpdateView):
    """
    Editing s schema or adding columns to it.
    """

    model = Schema
    form_class = SchemaForm
    template_name = "fakecsv/schema/new_schema.html"
    success_url = reverse_lazy("fakecsv:schema_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = self.get_formset()
        return context

    def get_formset(self):
        return inlineformset_factory(Schema, Column, form=ColumnForm, extra=1, can_delete=True)(
            self.request.POST or None, instance=self.object
        )

    def form_valid(self, form):
        formset = self.get_formset()
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.save()
            return redirect("fakecsv:edit_schema", pk=self.object.pk)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = self.get_formset()
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.save()
            return redirect("fakecsv:edit_schema", pk=self.object.pk)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class DetailSchemaView(LoginRequiredMixin, View):
    """
    View for displaying details of a schema for a CSV file.
    """

    template_name = "fakecsv/schema/schema_detail.html"

    def get(self, request, pk):
        try:
            schema = Schema.objects.select_related("owner").get(pk=pk)
        except Schema.DoesNotExist:
            return redirect("fakecsv:schema_list")
        column = schema.columns.all().order_by("order")
        form = DataSetForm(initial={"schema": schema})
        dataset = schema.data_sets.all()
        context = {
            "schema": schema,
            "column": column,
            "form": form,
            "dataset": dataset,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            schema = Schema.objects.select_related("owner").get(pk=pk)
        except Schema.DoesNotExist:
            return redirect("fakecsv:schema_list")

        column = schema.columns.all().order_by("order")
        form = DataSetForm(request.POST, instance=schema)
        dataset = schema.data_sets.all()

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
        return render(
            request,
            self.template_name,
            {
                "schema": schema,
                "column": column,
                "form": form,
                "dataset": dataset,
            },
        )


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
