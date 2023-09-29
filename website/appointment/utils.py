import datetime
from datetime import timedelta

from appointment.models import Day, Entry


def createNextDayEntry(day):
    """ Создание дней записи с ПН до СБ включительно"""
    end_day_week = day.day + datetime.timedelta(days=4)
    next_day = day.day + datetime.timedelta(days=1)
    while next_day <= end_day_week:
        Day.objects.get_or_create(day=next_day)
        obj = Day.objects.get(day=next_day)
        addEntryDay(obj)
        next_day = next_day + datetime.timedelta(days=1)


def addEntryDay(day):
    """ Создание времени для записи
    у дня с начала до конца рабочего дня с указанным интервалом
    """
    start = timedelta(hours=day.start.hour,
                      minutes=day.start.minute).total_seconds()
    end = timedelta(hours=day.end.hour, minutes=day.end.minute).total_seconds()
    step = float(day.step * 60)
    while start < end:
        time_entry = str(timedelta(seconds=start))
        Entry.objects.create(time=time_entry, day=day)
        start = start+step
