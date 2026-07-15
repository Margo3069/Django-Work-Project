from django.contrib import admin
from .models import Skill, EmployeeProfile, EmployeeSkill

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class EmployeeSkillInline(admin.TabularInline):
    model = EmployeeSkill
    extra = 1
    min_num = 0

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'patronymic', 'gender')
    list_filter = ('gender',)
    search_fields = ('user__first_name', 'user__last_name', 'patronymic')
    inlines = [EmployeeSkillInline]

@admin.register(EmployeeSkill)
class EmployeeSkillAdmin(admin.ModelAdmin):
    list_display = ('employee', 'skill', 'level')
    list_filter = ('skill',)