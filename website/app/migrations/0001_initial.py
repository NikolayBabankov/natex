# Generated by Django 4.2.5 on 2023-09-22 08:51

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import slugger.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=256, verbose_name='Название')),
                ('slug', slugger.fields.AutoSlugField(populate_from='name', unique=True)),
                ('sort_number', models.IntegerField(default=100, verbose_name='Сортировка')),
                ('short_name', models.TextField(blank=True, max_length=256, null=True, verbose_name='Короткое название')),
                ('tag_title', models.TextField(blank=True, max_length=80, null=True, verbose_name='Мета тег Title')),
                ('tag_description', models.TextField(blank=True, max_length=300, null=True, verbose_name='Мета тег Description')),
                ('pic', models.FileField(upload_to='page_pic/', verbose_name='Иконка услуги')),
                ('text', models.TextField(verbose_name='Текст')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='app.service', verbose_name='Родительская услуга')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
                'ordering': ['sort_number', 'name'],
            },
        ),
    ]
