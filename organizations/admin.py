from django.contrib import admin
from .models import OrganizationModel,ManagerModel 

admin.site.register(OrganizationModel)

class ManagerModelAdmin(admin.ModelAdmin):
  list_display = ("name", "organization", "user")
  list_filter = ('organization__name','name', 'user')
admin.site.register(ManagerModel, ManagerModelAdmin)