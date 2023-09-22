from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from blog.models import Post


class PostAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "sort_number"]
    form = PostAdminForm
    save_as = True
    save_on_top = True
