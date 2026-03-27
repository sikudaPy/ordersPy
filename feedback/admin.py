from django.contrib import admin
from .models import Feedback, FeedbackComment

class FeedbackInline(admin.TabularInline):
    model = FeedbackComment
    extra = 1

class FeedbackModelAdmin(admin.ModelAdmin):
  list_display = ("name", "email", "comment")
  list_filter = ('name','email')
  inlines = [FeedbackInline]

admin.site.register(Feedback, FeedbackModelAdmin)
