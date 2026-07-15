from django.db import models
from employees.models import EmployeeProfile

class Workplace(models.Model):
    table_number = models.CharField(max_length=20, unique=True, verbose_name="Номер стола")
    extra_info = models.TextField(blank=True, verbose_name="Дополнительная информация")
    employee = models.OneToOneField(EmployeeProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='workplace', verbose_name="Закрепленный сотрудник")

    def __str__(self):
        return f"Стол {self.table_number}"

    class Meta:
        verbose_name = "Рабочее место"
        verbose_name_plural = "Рабочие места"