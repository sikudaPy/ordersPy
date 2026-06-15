from django.contrib import admin
from django.http import HttpResponse
from .models import OrganizationModel, AssortmentModel, ManagerModel, OrderModel, OrderAssortmentTableModel

class OrderAssortmentlInline(admin.TabularInline):
    model = OrderAssortmentTableModel
    extra = 1

class OrderModelAdmin(admin.ModelAdmin):
  list_display = ("number", "date","organization","summa")
  list_filter = ('date', 'number','organization')
  search_fields = ('number', 'date', 'organization__name') 
  ordering = ('date',)
  inlines = [OrderAssortmentlInline]

admin.site.register(OrderModel, OrderModelAdmin)

def make_count(modeladmin, request, queryset):
    #queryset.update(price='summa/count')
    return HttpResponse("Selected lines were successfully update.")
make_count.short_description = "Count field count"

