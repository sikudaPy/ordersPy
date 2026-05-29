from django.db import models
from django.contrib.auth.models import User
import uuid

class OrganizationModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

class ManagerModel(models.Model):
    uuid = models.UUIDField(primary_key=True, null=False,default=uuid.uuid4)
    organization = models.ForeignKey(OrganizationModel, on_delete = models.CASCADE)
    name = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
