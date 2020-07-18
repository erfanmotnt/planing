from django.db import models
#!!
class Task(models.Model):
    name = models.CharField(max_length=50)
    is_done = models.BooleanField(default=False)
    period = models.CharField(max_length=1, default='n')
    multi_change = models.BooleanField(default=False)
    time_needed = models.TimeField("time needed", null = True)
    working_time = models.DateTimeField("working time", null = True)
    end_time = models.DateTimeField("dedline", null = True)
    start_time = models.DateTimeField("start time", null = True)
    rate = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    def time_needed_todo(self):
        return self.time_needed.strftime("%H:%M:%S")
