from django.contrib import admin
from .models import Task
import datetime

class TaskAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        form = super(TaskAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['start_time'].initial = datetime.datetime.now()
        return form



admin.site.register(Task, TaskAdmin)
