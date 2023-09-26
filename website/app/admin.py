from django.contrib import admin
from django.contrib.auth.models import Group
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from mptt.admin import DraggableMPTTAdmin
from django import forms

from app.models import Service, DocumentProduct, Application


class ServiceAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Service
        fields = '__all__'


@admin.register(Service)
class ServiceAdmin(DraggableMPTTAdmin):
    form = ServiceAdminForm
    save_as = True
    save_on_top = True


@admin.register(DocumentProduct)
class DocumentProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created_at',)


admin.site.site_header = 'Администрирование сайта НАТЭКС'
admin.site.index_title = 'Настройки'
admin.site.unregister(Group)
