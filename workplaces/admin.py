from django.contrib import admin
from .models import Workplace

@admin.register(Workplace)
class WorkplaceAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'employee', 'extra_info')
    search_fields = ('table_number', 'employee__user__first_name')