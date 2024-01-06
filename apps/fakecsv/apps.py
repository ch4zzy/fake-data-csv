from django.apps import AppConfig


class FakecsvConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.fakecsv"

    def ready(self):
        import apps.fakecsv.signals  # NOQA
