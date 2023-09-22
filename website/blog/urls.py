from django.urls import path
from django.conf.urls import include

from blog.views import blogView, postView


urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('stati/', blogView, name='blog'),
    path('stati/<slug:post_slug>/', postView, name='post'),
]
