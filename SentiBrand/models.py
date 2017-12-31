from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

class User_Phrase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    start_date = models.DateTimeField(default=datetime.now, editable=True)
    interval_in_sec = models.IntegerField()

class Phrase(models.Model):
    phrase = models.CharField(max_length=250, primary_key=True)
    user_phrase = models.ForeignKey(User_Phrase, on_delete=models.CASCADE)