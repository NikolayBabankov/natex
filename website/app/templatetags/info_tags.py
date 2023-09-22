from django import template

from app.models import Service


register = template.Library()


@register.simple_tag()
def get_services():
    return Service.objects.all()
