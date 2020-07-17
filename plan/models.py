from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=50)
    period = models.CharField(max_length=1, default='n')
    time_needed = models.TimeField("time needed", null = True)
    working_time = models.DateTimeField("working time", null = True)
    end_time = models.DateTimeField("dedline", null = True)
    start_time = models.DateTimeField("start time", null = True)
    rate = models.IntegerField(default=1)

    def __str__(self):
        return self.name
