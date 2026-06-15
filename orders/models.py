from django.contrib.auth.models import User
from django.db import models
import uuid
from assortment.models import AssortmentModel
from organizations.models import OrganizationModel, ManagerModel

class OrderModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    number = models.CharField(max_length=50,default="")
    date = models.DateField(auto_created=True,blank=True, null=True)
    organization = models.ForeignKey(OrganizationModel, on_delete = models.CASCADE, blank=True, null=True)
    comment = models.TextField(default="",blank=True)
    summa = models.DecimalField(max_digits=19, decimal_places=2, default=0, blank=True, null=True)


class OrderAssortmentTableModel(models.Model):
    order = models.ForeignKey(OrderModel, related_name='table', on_delete = models.CASCADE)
    num = models.PositiveIntegerField(default=1)
    assortment = models.ForeignKey(AssortmentModel, on_delete = models.PROTECT)
    count = models.DecimalField(max_digits=19, decimal_places=0, default=0)
    price = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    summa = models.DecimalField(max_digits=19, decimal_places=2, default=0)

    