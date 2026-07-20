from django.contrib.auth.models import User
from django.db import models
import os
from django.core.exceptions import ValidationError
from datetime import date

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название навыка")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from workplaces.models import Workplace


class EmployeeProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('O', 'Другой'),
    ]

    ROLE_CHOICES = [
        ('tester', 'Тестировщик'),
        ('backend', 'Backend разработчик'),
        ('frontend', 'Frontend разработчик'),
    ]

    user = models.OneToOneField('auth.User',on_delete=models.CASCADE,related_name='profile',verbose_name="Пользователь")
    patronymic = models.CharField(max_length=50,blank=True,null=True,verbose_name="Отчество")
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,blank=True,verbose_name="Пол")
    description = models.TextField(blank=True,verbose_name="Описание / О себе")
    skills = models.ManyToManyField('Skill',through='EmployeeSkill',related_name='employees',verbose_name="Навыки")
    hire_date = models.DateField(verbose_name="Дата приёма на работу")
    workplace = models.ForeignKey('workplaces.Workplace',on_delete=models.SET_NULL,null=True,blank=True,verbose_name="Рабочее место")
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default='tester',verbose_name="Роль")

    @property
    def work_days(self):
        if not self.hire_date:
            return 0
        return (date.today() - self.hire_date).days

    def clean(self):
        if self.workplace and self.role:
            try:
                current_num = int(self.workplace.table_number)
            except (ValueError, TypeError):
                raise ValidationError("Номер стола должен быть числом для проверки соседей.")

            neighbor_nums = [current_num - 1, current_num + 1]

            for n in neighbor_nums:
                try:
                    neighbor_wp = Workplace.objects.get(table_number=str(n))
                    neighbor_emp = EmployeeProfile.objects.filter(workplace=neighbor_wp).first()
                    if neighbor_emp:
                        is_enemy = (
                            (self.role in ['backend', 'frontend'] and neighbor_emp.role == 'tester') or
                            (neighbor_emp.role in ['backend', 'frontend'] and self.role == 'tester')
                        )
                        if is_enemy:
                            raise ValidationError(
                                f"Нельзя сажать {self.get_role_display()} рядом со столом {neighbor_wp.table_number}, "
                                f"там уже сидит {neighbor_emp.get_role_display()}."
                            )
                except Workplace.DoesNotExist:
                    continue

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        full_name = f"{self.user.first_name} {self.user.last_name}"
        if self.patronymic:
            full_name += f" {self.patronymic}"
        return full_name

    class Meta:
        verbose_name = "Профиль сотрудника"
        verbose_name_plural = "Профили сотрудников"


class EmployeeSkill(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, verbose_name="Сотрудник")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, verbose_name="Навык")
    level = models.PositiveSmallIntegerField(default=1, verbose_name="Уровень (1-10)")

    def __str__(self):
        return f"{self.employee} - {self.skill}: {self.level}"

    class Meta:
        unique_together = ('employee', 'skill')
        verbose_name = "Навык сотрудника"
        verbose_name_plural = "Навыки сотрудников"


class EmployeeImage(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='employee_photos/')
    order_number = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order_number']

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)