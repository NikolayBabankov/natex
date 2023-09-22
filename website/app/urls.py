from django.urls import path

from app.views import (indexView, aboutView,
                       contactView, servicesView,
                       serviceView)

urlpatterns = [
    path('', indexView, name='index'),
    path('aboutnatex/', aboutView, name='about'),
    path('aboutnatex/contacts/', contactView, name='contacts'),
    path('nashiuslugi/', servicesView, name='services'),
    path('nashiuslugi/<slug:service_slug>/', serviceView, name='service'),
]
