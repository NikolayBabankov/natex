from django.urls import path

from appointment.views import getEntryFreeAjaxView, createEntryAjaxViews

urlpatterns = [
    path('free_entry/', getEntryFreeAjaxView, name="free_entry"),
    path('post_entry/', createEntryAjaxViews, name="post_entry"),
]
