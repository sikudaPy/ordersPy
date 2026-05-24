from django.contrib.auth.models import User
from django.db import models
import uuid
from django.db.models import Sum

class OrganizationModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

class AssortmentModel(models.Model):
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

class OrderModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    number = models.CharField(max_length=50,default="")
    date = models.DateField(auto_created=True,blank=True, null=True)
    organization = models.ForeignKey(OrganizationModel, on_delete = models.CASCADE, blank=True, null=True)
    comment = models.TextField(default="",blank=True)
    summa = models.DecimalField(max_digits=19, decimal_places=2, default=0, blank=True, null=True)


class OrderAssortmentTableModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete = models.CASCADE)
    #num = models.PositiveIntegerField(default=1)
    assortiment = models.ForeignKey(AssortmentModel, on_delete = models.PROTECT)
    count = models.DecimalField(max_digits=19, decimal_places=0, default=0)
    price = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    summa = models.DecimalField(max_digits=19, decimal_places=2, default=0)

    