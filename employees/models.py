from django.contrib.auth.models import User
from django.db import models

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