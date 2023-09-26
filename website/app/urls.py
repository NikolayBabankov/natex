from django.urls import path
from django.views.generic import TemplateView

from app.views import (indexView, aboutView,
                       contactView, servicesView,
                       serviceView, tekhosmotrView,
                       applicationAjaxViews)

urlpatterns = [
    path('', indexView, name='index'),
    path('aboutnatex/', aboutView, name='about'),
    path('aboutnatex/contacts/', contactView, name='contacts'),
    path('nashiuslugi/', servicesView, name='services'),
    path('nashiuslugi/tekhosmotr/', tekhosmotrView, name='tekhosmotr'),
    path('nashiuslugi/<slug:service_slug>/', serviceView, name='service'),
    path('lead/', applicationAjaxViews, name='lead'),
    path('success_lead/',
         TemplateView.as_view(
             template_name='success_lead.html'),
         name='success_lead'),
    path('politica/',
         TemplateView.as_view(
             template_name='politica.html'),
         name='politica'),
]
