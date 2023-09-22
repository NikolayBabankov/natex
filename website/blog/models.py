from django.db import models
from slugger import AutoSlugField


class Post(models.Model):
    """ Модель статьи """
    title = models.TextField(verbose_name="Заголовок", max_length=500)
    short_title = models.TextField(verbose_name="Короткий пояснение",
                                   max_length=300,
                                   blank=True, null=True)
    description = models.TextField(verbose_name="Описание",
                                   max_length=500,
                                   blank=True, null=True)
    slug = AutoSlugField(populate_from='title', unique=True)
    text = models.TextField(verbose_name="Текст")
    sort_number = models.IntegerField(default=100, verbose_name='Сортировка')

    class Meta:
        ordering = ['sort_number']
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return f'{self.title}'
