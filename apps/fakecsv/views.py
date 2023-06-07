from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render

from apps.fakecsv.forms import ColumnForm, SchemaForm
from apps.fakecsv.models import Column, Schema


@login_required
def schema_list(request):
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
    schema = get_object_or_404(Schema, pk=pk, owner=request.user)
    schema.delete()
    return redirect("fakecsv:schema_list")


@login_required
def delete_column(request, pk):
    column = get_object_or_404(Column, pk=pk)
    column.delete()
    return redirect("fakecsv:schema_list")


@login_required
def edit_schema(request, pk):
    schema = Schema.objects.get(pk=pk)
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
