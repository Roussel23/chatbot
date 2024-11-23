from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

class Chat(models.Model):
    id = models.CharField(primary_key=True,max_length=100)
    username = models.CharField(max_length=100)
    # AutoField
    # username = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=10000)
    response = models.CharField(max_length=1000000)
    date = models.DateTimeField(auto_now=True)
   
    # username_fk = models.ForeignKey(to=User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.username}: {self.question}'
    class Meta:
        ordering = ['-date']
        

