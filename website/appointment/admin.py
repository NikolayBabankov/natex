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
    search_fields = ('id',)
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

    actions = ['add_week_entry']

    def save_model(self, request, obj, form, change):
        if not change:
            super().save_model(request, obj, form, change)
            day = Day.objects.get(day=obj.day)
            addEntryDay(day)
        else:
            super().save_model(request, obj, form, change)

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

    add_week_entry.short_description = "Заполнить неделю c Понедельника"
    add_week_entry.allowed_permissions = ('change', )
