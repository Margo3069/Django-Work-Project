from django.db import models

class Workplace(models.Model):
    table_number = models.CharField(max_length=20, unique=True, verbose_name="Номер стола")
    extra_info = models.TextField(blank=True, verbose_name="Дополнительная информация")
    def __str__(self):
        return f"Стол {self.table_number}"

    class Meta:
        verbose_name = "Рабочее место"
        verbose_name_plural = "Рабочие места"