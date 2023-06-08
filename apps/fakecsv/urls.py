from django.urls import include, path

from apps.fakecsv.views import (
    create_schema,
    delete_column,
    delete_schema,
    detail_schema,
    download_data_set,
    edit_schema,
    schema_list,
)

app_name = "fakecsv"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("create-schema/", create_schema, name="create_schema"),
    path("edit-schema/<int:pk>/", edit_schema, name="edit_schema"),
    path("delete-schema/<int:pk>/", delete_schema, name="delete_schema"),
    path("delete-column/<int:pk>/", delete_column, name="delete_column"),
    path("detail-schema/<int:pk>/", detail_schema, name="detail_schema"),
    path("download-data-set/<int:data_set_id>/", download_data_set, name="download_data_set"),
    path("list/", schema_list, name="schema_list"),
]
