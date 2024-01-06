from django.core.files.storage import default_storage
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import DataSet


@receiver(post_delete, sender=DataSet)
def delete_s3_file(sender, instance, **kwargs):
    """
    Delete the file associated with the instance from S3 when the instance is deleted.
    """

    file_path = instance.file.name
    if file_path:
        default_storage.delete(file_path)
