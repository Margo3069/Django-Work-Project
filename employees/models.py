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


class EmployeeProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('O', 'Другой'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Пользователь")
    patronymic = models.CharField(max_length=50, blank=True, null=True, verbose_name="Отчество")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name="Пол")
    description = models.TextField(blank=True, verbose_name="Описание / О себе")
    skills = models.ManyToManyField(Skill, through='EmployeeSkill', related_name='employees', verbose_name="Навыки")
    hire_date = models.DateField(verbose_name="Дата приёма на работу")

    @property
    def work_days(self):
        if not self.hire_date:
            return 0
        return (date.today() - self.hire_date).days

    def save(self, *args, **kwargs):
        if self.workplace:
            current_table = self.workplace.table_number
            role = self.role

            is_enemy_role = False
            if role == 'tester':
                is_enemy_role = True
            elif role in ['backend', 'frontend']:
                is_enemy_role = True

            if is_enemy_role:
                neighbors = EmployeeProfile.objects.filter(
                    workplace__table_number__in=[current_table - 1, current_table + 1]
                )
                for neighbor in neighbors:
                    n_role = neighbor.role
                    if (role == 'tester' and n_role in ['backend', 'frontend']) or \
                    (n_role == 'tester' and role in ['backend', 'frontend']):
                        raise ValidationError(
                            f"Нельзя сажать {role} за стол {current_table}, "
                            f"рядом уже сидит {n_role}."
                        )
        
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