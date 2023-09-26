import datetime
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest

from app.models import Service, Application
from app.send_email import sendEmail
from appointment.models import Day, Entry


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


def tekhosmotrView(request):
    """Вьюха страницы списка услуг"""
    title = 'Техосмотр в Ярославле | Пройти техосмотр в "Натэкс"'
    description = 'Пройти техосмотр в Ярославле вы можете у Нас, записавшись в форме на сайте!'
    template = 'tekhosmotr.html'
    # Получем все дни с сегодняшней даты
    dt_now = datetime.datetime.now()
    day = Day.objects.filter(day__gte=dt_now)
    # Форматируем сегодняшнюю дату для vanila calendar
    dt_now_str = dt_now.strftime("%Y-%m-%d")
    # Записываем в массив все не рабочие дни для vanila calendar
    # C Сегоднишней даты до последнего дня из БД
    end = day.first()
    end_day = datetime.datetime.combine(end.day, datetime.time(0, 0))
    delta = datetime.timedelta(days=1)
    no_work_day = []
    statr_day = dt_now
    while (statr_day <= end_day):
        if not day.filter(day=statr_day):
            no_work_day.append(statr_day.strftime("%Y-%m-%d"))
        statr_day += delta
    no_work_day = json.dumps(no_work_day)
    endStr = end.day.strftime("%Y-%m-%d")
    # Получаем все свобоные время записи на настоящее время
    entrys = Entry.objects.filter(day__day=dt_now).filter(reserve=False).filter(time__gt=dt_now)
    service = Service.objects.get(slug='tekhosmotr')
    context = {'title': title,
               'description': description,
               'today_str': dt_now_str, 'today': dt_now,
               'end_str': endStr, 'no_work': no_work_day,
               'entrys': entrys, 'service': service}
    return render(request, template, context)


def applicationAjaxViews(request):
    """ Отправка заявки по AJAX """
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'POST':
            data = json.loads(request.body)
            try:
                lead = Application.objects.create(name=data['name'],
                                                  phone=data['phone'])
            except Exception:
                return JsonResponse({'status': 'Error'}, status=400)
            dt_now = datetime.datetime.now()
            date = dt_now.strftime('%H:%M - %d.%m.%Y')
            dictLead = {'name': lead.name, 'phone': lead.phone, 'date': date}
            sendEmail(dictLead)
            return JsonResponse({'status': 'Send'})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')
