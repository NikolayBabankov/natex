from django.http import JsonResponse, HttpResponseBadRequest
import logging, datetime, json
from django.core import serializers

from appointment.models import Entry


logger = logging.getLogger(__name__)


def getEntryFreeAjaxView(request):
    """ Получение свободных времени для записи по Ajax """
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'POST':
            data = json.loads(request.body)
            dt_now = datetime.datetime.now()
            date_request = datetime.datetime.strptime(data['date'], '%Y-%m-%d')
            if date_request > dt_now:
                entrys = Entry.objects.filter(day__day=date_request).filter(reserve=False)
            else:
                entrys = Entry.objects.filter(day__day=date_request).filter(reserve=False).filter(time__gt=dt_now)
            date_entry = {}
            for entry in entrys:
                date_entry[entry.id] = entry.time.strftime('%H %M')
            return JsonResponse({'data': date_entry}, status=200)
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')


def createEntryAjaxViews(request):
    """ Запись на свободное время Ajax """
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'POST':
            data = json.loads(request.body)
            entry = Entry.objects.get(id=data['time'])
            if entry.reserve:
                return JsonResponse({'status': 'Reserve'}, status=200)
            entry.reserve = True
            entry.name = data['name']
            entry.phone = data['phone']
            entry.automobile = data['automobile']
            entry.number = data['number']
            entry.year = data['year']
            if 'email' in data:
                entry.email = data['email']
            entry.save()
            data_answer = {
                'id': entry.id,
                'time': entry.time,
                'day': entry.day.day,
                'automobile': entry.automobile,
                'number': entry.number,
                'year': entry.year,
                'phone': entry.phone,
                'name': entry.name}
            return JsonResponse({'data': data_answer}, status=200)
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')
