from django.urls import include, path

from apps.fakecsv.views import create_schema, delete_schema, edit_schema, schema_list

app_name = "fakecsv"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("create-schema/", create_schema, name="create_schema"),
    path("edit-schema/<int:pk>/", edit_schema, name="edit_schema"),
    path("delete-schema/<int:pk>/", delete_schema, name="delete_schema"),
    path("list/", schema_list, name="schema_list"),
]
