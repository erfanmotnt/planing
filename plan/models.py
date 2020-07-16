from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=50)
    end_time = models.DateTimeField("dedline", null = True)
    start_time = models.DateTimeField("start time", null = True)
    working_time = models.DateTimeField("working time", null = True)
    time_needed = models.DateTimeField("time needed", null = True)
    rate = models.IntegerField(default=1)
    