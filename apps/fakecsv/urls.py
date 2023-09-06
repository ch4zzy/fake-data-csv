from django.urls import include, path
from django.views.generic.base import RedirectView

from apps.fakecsv.views import (  # detail_schema,
    CreateSchemaView,
    DetailSchemaView,
    EditSchemaView,
    SchemaListView,
    delete_column,
    delete_schema,
    download_data_set,
)

app_name = "fakecsv"

urlpatterns = [
    path("", RedirectView.as_view(url="/login/", permanent=True)),
    path("", include("django.contrib.auth.urls")),
    path("create-schema/", CreateSchemaView.as_view(), name="create_schema"),
    path("edit-schema/<int:pk>/", EditSchemaView.as_view(), name="edit_schema"),
    path("delete-schema/<int:pk>/", delete_schema, name="delete_schema"),
    path("delete-column/<int:pk>/", delete_column, name="delete_column"),
    path("detail-schema/<int:pk>/", DetailSchemaView.as_view(), name="detail_schema"),
    path("download-data-set/<int:data_set_id>/", download_data_set, name="download_data_set"),
    path("list/", SchemaListView.as_view(), name="schema_list"),
]
