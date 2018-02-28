from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Phrase(models.Model):
    phrase = models.CharField(max_length=250, primary_key=True)

class User_Phrase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    start_date = models.DateTimeField(default=datetime.now, editable=True, null=False, blank=False)
    end_date = models.DateTimeField(editable=True, null=False, blank=False)
    phrase = models.ForeignKey(Phrase)
