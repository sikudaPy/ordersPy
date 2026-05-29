from django.db import models
import uuid

# Create your models here.
class AssortmentModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
