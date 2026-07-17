from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import EmployeeProfile

class EmployeeListView(ListView):
    model = EmployeeProfile
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = EmployeeProfile
    template_name = 'employees/employee_detail.html'
    context_object_name = 'employee'
    login_url = '/login/'

# Create your views here.
