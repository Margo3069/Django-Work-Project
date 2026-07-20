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

def home_view(request):
    total_count = EmployeeProfile.objects.count()
    latest_employees = EmployeeProfile.objects.order_by('-hire_date')[:4]
    
    return render(request, 'employees/home.html', {
        'total_count': total_count,
        'latest_employees': latest_employees
    })

class EmployeeListView(ListView):
    model = EmployeeProfile
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10

    def get_queryset(self):
        return EmployeeProfile.objects.all().prefetch_related('skills', 'images')

class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = EmployeeProfile
    template_name = 'employees/employee_detail.html'
    context_object_name = 'employee'
    login_url = '/login/'

    def get_queryset(self):
        return EmployeeProfile.objects.prefetch_related('skills', 'images')