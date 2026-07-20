from django.contrib import admin
from .models import Workplace

@admin.register(Workplace)
class WorkplaceAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'extra_info')
    search_fields = ['table_number']