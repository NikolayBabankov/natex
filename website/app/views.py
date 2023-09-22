from django.shortcuts import render, get_object_or_404

from app.models import Service


def indexView(request):
    """Вьюха главной страницы"""
    title = 'Натэкс-оценочная экспертная компания'
    description = 'Оценочная экспертная компания'
    template = 'index.html'
    context = {'title': title, 'description': description}
    return render(request, template, context)


def aboutView(request):
    """Вьюха страницы о компании"""
    title = 'О компании Натэкс'
    description = 'Оценочная экспертная компания'
    template = 'about.html'
    context = {'title': title, 'description': description}
    return render(request, template, context)


def contactView(request):
    """Вьюха страницы контактов"""
    title = 'Контакты ООО "Натэкс"'
    description = 'Контакты оценочная экспертная компания ООО "Натэкс '
    template = 'contacts.html'
    context = {'title': title, 'description': description}
    return render(request, template, context)


def servicesView(request):
    """Вьюха страницы списка услуг"""
    title = 'Услуги ООО "Натэкс"'
    description = 'Услуги оценочная экспертная компания ООО "Натэкс '
    template = 'serviceall.html'
    context = {'title': title,
               'description': description}
    return render(request, template, context)


def serviceView(request, service_slug):
    """Вьюха страницы списка услуг"""
    title = 'Услуги ООО "Натэкс"'
    description = 'Услуги оценочная экспертная компания ООО "Натэкс '
    template = 'service.html'
    service = get_object_or_404(Service, slug=service_slug)
    if service.tag_title:
        title = service.tag_title
    if service.tag_description:
        description = service.tag_description
    context = {'title': title,
               'description': description,
               'service': service}
    return render(request, template, context)
