# Generated by Django 4.2.5 on 2023-09-22 07:15

from django.db import migrations, models
import slugger.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0002_delete_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=500, verbose_name='Заголовок')),
                ('short_title', models.TextField(blank=True, max_length=300, null=True, verbose_name='Короткий пояснение')),
                ('description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Описание')),
                ('slug', slugger.fields.AutoSlugField(populate_from='title')),
                ('text', models.TextField(verbose_name='Текст')),
                ('sort_number', models.IntegerField(default=100, verbose_name='Сортировка')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
                'ordering': ['sort_number'],
            },
        ),
    ]
