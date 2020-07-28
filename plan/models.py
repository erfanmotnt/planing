from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=50)
    is_done = models.BooleanField(default=False)
    delay = models.IntegerField(default=0)
    period = models.CharField(max_length=1, default='n')
    multi_change = models.BooleanField(default=False)
    time_needed = models.TimeField("time needed", null = True)
    working_time = models.DateTimeField("working time", null = True)
    end_time = models.DateTimeField("dedline", null = True)
    start_time = models.DateTimeField("start time", null = True)
    rate = models.IntegerField(default=1)
    punishment = models.ForeignKey('Punishment', on_delete=models.CASCADE, null=True)
    cost_of_delay = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def time_needed_todo(self):
        return self.time_needed.strftime("%H:%M:%S")

class Punishment(models.Model):
    name = models.CharField(max_length=50)
    to_do_number = models.IntegerField(default=0)
    done_number = models.IntegerField(default=0)
  
    def __str__(self):
        return self.name
    
    def need_to_do(self):
        return -(-self.to_do_number//100) - self.done_number
