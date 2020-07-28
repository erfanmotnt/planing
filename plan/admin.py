from django.contrib import admin
from django import forms
from .models import Task, Punishment
from datetime import timedelta, time, datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta


class TaskForm(forms.ModelForm):
    
    PERIODS = (
        ('n', 'None'),
        ('d', 'daily'),
        ('w', 'weekly'),
        ('m', 'monthly'),
        ('y', 'yearly')
    )
    period = forms.ChoiceField(choices=PERIODS)
    
def periodToRelativedelta(period):
    relativedeltaStartTime = relativedelta()
    relativedeltaEndTime = relativedelta()
    if period == 'lw':
        relativedeltaStartTime = relativedelta(weeks=-1)
    elif period == 'yd':
        relativedeltaStartTime = relativedelta(days=-1)
    elif period == 'd':
        relativedeltaEndTime = relativedelta(days=1)
    elif period == 'w':
        relativedeltaEndTime = relativedelta(weeks=1)
    elif period == 'm':
        relativedeltaEndTime = relativedelta(months=1)
    elif period == 'y':
        relativedeltaEndTime = relativedelta(years=1)
    return relativedeltaStartTime, relativedeltaEndTime

def getNext(obj):
    outObj = obj
    outObj.pk = None
    outObj.working_time = outObj.working_time + periodToRelativedelta(obj.period)[1]
    return outObj
class WorkingTimeSetFilter(admin.SimpleListFilter):
    title = 'working_time_set'
    parameter_name = 'working_time'

    def lookups(self, request, model_admin):
        return (
            ('lw', 'last week'),
            ('yd', 'yesterday'),
            ('d', 'today'),
            ('w', 'this week'),
            ('m', 'this month'),
            ('y', 'this year')
        )
    
    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        relativedeltaStartTime, relativedeltaEndTime = periodToRelativedelta(self.value())
        startDay = datetime(
                    timezone.now().year,
                    timezone.now().month,
                    timezone.now().day,
                    0,
                    0,
                    0
                ) + relativedeltaStartTime
        endDay = datetime(
                    timezone.now().year,
                    timezone.now().month,
                    timezone.now().day,
                    0,
                    0,
                    0
                ) + relativedeltaEndTime
        print(startDay.day, endDay.day, "!!!!!!!!!!!!!!!!!!!!!!!!!!")
        queryset = queryset.filter(working_time__lte=endDay)
        queryset = queryset.filter(working_time__gte=startDay)
        queryset = queryset.order_by('working_time')
        return queryset
        

class TaskAdmin(admin.ModelAdmin):
    form = TaskForm
    list_display = ('name', 'working_time', 'time_needed_todo', 'is_done')
    list_filter = [WorkingTimeSetFilter, 'name']

    def get_form(self, request, obj=None, **kwargs):
        form = super(TaskAdmin, self).get_form(request, obj, **kwargs)
        if obj is not None:
            self.task_last_name = obj.name
            self.task_last_cost = obj.cost_of_delay*obj.delay
        else:
            form.base_fields['start_time'].initial = datetime(
                    timezone.now().year,
                    timezone.now().month,
                    timezone.now().day,
                    0,
                    0,
                    0
                )
            form.base_fields['end_time'].initial = datetime(
                    timezone.now().year,
                    timezone.now().month,
                    timezone.now().day,
                    0,
                    0,
                    0
                ) + relativedelta(days=1)
            form.base_fields['working_time'].initial = timezone.now()
            form.base_fields['time_needed'].initial = time(0, 15, 0)
        return form

    def save_model(self, request, obj, form, change):    
        if not change and obj.period != 'n':
            while obj.working_time < obj.end_time:
                obj.save()
                obj = getNext(obj)
        elif obj.multi_change:
            obj.save()
            querys = Task.objects.all().filter(name=self.task_last_name)
            querys = querys.filter(working_time__gte=obj.working_time)
            for q in querys:
                wttmp = datetime(
                    q.working_time.year,
                    q.working_time.month,
                    q.working_time.day,
                    obj.working_time.hour,
                    obj.working_time.minute,
                    obj.working_time.second
                )
                
                pktmp = q.pk
                donetmp = q.is_done
                delaytmp = q.delay
                q = obj
                q.pk = pktmp
                q.working_time = wttmp
                q.is_done = donetmp
                q.delay = delaytmp
                q.multi_change = False
                q.save()
        else:
            obj.save()
        
        obj.punishment.to_do_number = obj.punishment.to_do_number - \
            (self.task_last_cost if self.task_last_cost else 0) + \
            obj.delay*obj.cost_of_delay
        obj.punishment.save()

class PunishmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'need_to_do')

admin.site.register(Task, TaskAdmin)
admin.site.register(Punishment, PunishmentAdmin)
