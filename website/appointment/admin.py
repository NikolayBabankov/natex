from django.contrib import admin
from django.contrib import messages
from django.forms import TextInput, Textarea
from django.db import models
from rangefilter.filters import (
    DateRangeQuickSelectListFilterBuilder,
)

from appointment.models import Day, Entry
from appointment.utils import addEntryDay, createNextDayEntry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'day', 'name',
                    'phone', 'automobile', 'number', 'reserve')
    search_fields = ('id', 'number')
    list_filter = (
        ("day__day", DateRangeQuickSelectListFilterBuilder()),
        ('reserve')
    )

    readonly_fields = ('time', 'day',)

    fieldsets = (
        (None, {'fields': (('reserve',), )}),
        (None, {'fields': (('name', 'phone', 'email'), )}),
        (None, {'fields': (('automobile', 'year', 'number'), )}),
    )

    save_as = True
    save_on_top = True

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 5, 'cols': 40})},
    }


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ('day',)
    list_filter = (
        ("day", DateRangeQuickSelectListFilterBuilder()),
    )

    actions = ['add_week_entry', 'days_delete_queryset']

    def save_model(self, request, obj, form, change):
        if not change:
            super().save_model(request, obj, form, change)
            day = Day.objects.get(day=obj.day)
            addEntryDay(day)
        else:
            super().save_model(request, obj, form, change)

    def get_actions(self, request):
        actions = super(DayAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def add_week_entry(self, request, queryset):
        """Заполнить неделю c ПН"""
        if len(queryset) != 1:
            return messages.error(request, "Выберите один день")
        day = queryset[0]
        if day.day.weekday() != 0:
            return messages.error(request, "Выберите понедельник")
        try:
            createNextDayEntry(day)
            self.message_user(request, f"Неделя с {day} заполнена")
        except:
            return messages.error(request, "Произошла ошибка")

    def days_delete_queryset(self, request, queryset):
        """ Удаление нескольких дней с проверкой
        если зарезервированное время записи в этих днях"""
        for day in queryset:
            entry = Entry.objects.filter(day=day).filter(reserve=True)
            if entry:
                print(day)
                return messages.error(request,
                                      f"Есть резервированное время у {day} в количестве {len(entry)} шт")
        count_day = len(queryset)
        queryset.delete()
        return self.message_user(request, f"Успешно удалены {count_day} дней")

    def delete_model(self, request, obj):
        """ Удаление одного дня с проверкой
        если зарезервированное время записи в этот день"""
        entry = Entry.objects.filter(day=obj).filter(reserve=True)
        if entry:
            return messages.error(request,
                                  f"Есть резервированное время у {obj} в количестве {len(entry)} шт")
        obj.delete()

    days_delete_queryset.short_description = "Удалить дни"
    add_week_entry.short_description = "Заполнить неделю c Понедельника"
    add_week_entry.allowed_permissions = ('change', )
    days_delete_queryset.allowed_permissions = ('delete', )
