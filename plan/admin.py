from django.contrib import admin
from django import forms
from .models import Task
from datetime import timedelta, time, datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta

PERIODS = (
        ('n', 'None'),
        ('d', 'Daily'),
        ('w', 'Weekly'),
        ('m', 'Monthly'),
        ('y', 'Yearly')
    )

class TaskForm(forms.ModelForm):
    
    period = forms.ChoiceField(choices=PERIODS)
    
class WorkingTimeSetFilter(admin.SimpleListFilter):
    title = 'working_time_set'
    parameter_name = 'working_time'

    def lookups(self, request, model_admin):
        return  PERIODS


    def queryset(self, request, queryset):
        value = self.value()
        ###

        
def getNext(obj):
    outObj = obj
    outObj.pk = None
    period = obj.period
    relativedeltaTime = relativedelta()
    if period is 'n':   
        relativedeltaTime = relativedelta()
    elif period is 'd':
        relativedeltaTime = relativedelta(days=1)
    elif period is 'w':
        relativedeltaTime = relativedelta(weeks=1)
    elif period is 'm':
        relativedeltaTime = relativedelta(months=1)
    elif period is 'y':
        relativedeltaTime = relativedelta(years=1)

    outObj.working_time = outObj.working_time + relativedeltaTime
    return outObj


class TaskAdmin(admin.ModelAdmin):
    form = TaskForm
    list_display = ('name', 'working_time', 'time_needed')
    list_filter = [WorkingTimeSetFilter, 'name']
    def get_form(self, request, obj=None, **kwargs):
        form = super(TaskAdmin, self).get_form(request, obj, **kwargs)
        if obj is not None:
            self.task_last_name = obj.name
        form.base_fields['start_time'].initial = timezone.now()
        form.base_fields['time_needed'].initial = time(0, 15, 0)
        return form

    def save_model(self, request, obj, form, change):    
        if not change:
            while obj.working_time < obj.end_time:
                obj.save()
                obj = getNext(obj)
        else:
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
                q = obj
                q.pk = pktmp
                q.working_time = wttmp
                q.save()

admin.site.register(Task, TaskAdmin)
