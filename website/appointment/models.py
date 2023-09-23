from django.db import models
from datetime import timedelta
from django.core.exceptions import ValidationError


class Day(models.Model):
    """ Рабочие дня для запись на ТО """
    day = models.DateField(unique=True, verbose_name="Дата")
    start = models.TimeField(verbose_name="Начало записи", default='09:00:00')
    end = models.TimeField(verbose_name="Конец записи", default='20:00:00')
    step = models.IntegerField(verbose_name="Шаг записи, мин", default=20)

    class Meta:
        ordering = ['-day']
        verbose_name = 'День'
        verbose_name_plural = 'Дни'

    def __str__(self):
        return f'{self.day}'

    def duration_second(self):
        start = timedelta(hours=self.start.hour, minutes=self.start.minute)
        end = timedelta(hours=self.end.hour, minutes=self.end.minute)
        duration = end - start
        return duration.total_seconds()

    def clean(self):
        second_step = float(self.step * 60)
        if self.duration_second() % second_step != 0:
            raise ValidationError("Измените Шаг или Начало/Конец записи")


class Entry(models.Model):
    """ Модель запись на ТО """
    time = models.TimeField(verbose_name="Время записи")
    name = models.TextField(verbose_name="ФИО/Организация",
                            max_length=500, blank=True, null=True)
    phone = models.TextField(verbose_name="Телефон",
                             max_length=100, blank=True, null=True)
    email = models.TextField(verbose_name="Email",
                             max_length=200, blank=True, null=True)
    automobile = models.TextField(verbose_name="Автомобиль",
                                  max_length=500, blank=True, null=True)
    number = models.TextField(verbose_name="Номер автомобиля",
                              max_length=500, blank=True, null=True)
    year = models.TextField(verbose_name="Год выпуска",
                            max_length=100, blank=True, null=True)
    reserve = models.BooleanField(verbose_name="Резерв",
                                  default=False)
    day = models.ForeignKey(Day, related_name='entry',
                            verbose_name="Число", on_delete=models.CASCADE)

    class Meta:
        ordering = ['-day__day', 'time']
        unique_together = ('time', 'day',)
        verbose_name = 'Запись'
        verbose_name_plural = 'Время'

    def __str__(self):
        return f'Запись {self.time} - {self.day}'