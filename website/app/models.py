from django.db import models
from slugger import AutoSlugField
from mptt.models import MPTTModel, TreeForeignKey


class Service(MPTTModel):
    """Модель страницы услуг"""
    name = models.TextField(max_length=256, verbose_name='Название')
    slug = AutoSlugField(populate_from='name', unique=True)
    sort_number = models.IntegerField(default=100, verbose_name='Сортировка')
    main = models.BooleanField(default=False,
                               verbose_name='Добавить в главное меню')
    short_name = models.TextField(max_length=256,
                                  verbose_name='Короткое название',
                                  null=True, blank=True,)
    tag_title = models.TextField(max_length=80, verbose_name='Мета тег Title',
                                 null=True, blank=True)
    tag_description = models.TextField(max_length=300,
                                       verbose_name='Мета тег Description',
                                       null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True,
                            blank=True, related_name='children',
                            verbose_name='Родительская услуга')
    pic = models.FileField(upload_to='page_pic/', verbose_name='Иконка услуги')
    text = models.TextField(verbose_name='Текст')
    extra_text = models.TextField(verbose_name='Доп. текст',
                                  null=True, blank=True)

    class Meta:
        ordering = ['sort_number', 'name']
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return f'{self.name}'


# class DocumentProduct(models.Model):
#     """Модель документов"""
#     name = models.TextField(max_length=100, verbose_name='Название')
#     doc = models.FileField(upload_to='document/',
#                            verbose_name='Документ', blank=True, null=True)
#     service = models.ForeignKey(
#         Service, related_name='document', on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.name}'

#     class Meta:
#         verbose_name = 'Документ'
#         verbose_name_plural = 'Документы'
