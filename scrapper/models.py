from django.db import models
from dashboard.models import User_Phrase

class Search(models.Model):
    user_phrase_id = models.ForeignKey(User_Phrase, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add= True)

class Tweet(models.Model):
    search_id = models.ManyToManyField(Search)
    username = models.CharField(max_length=50)
    user_location = models.CharField(max_length=50)
    polarity = models.DecimalField(decimal_places=3, max_digits=6)
    tweet_id = models.BigIntegerField(primary_key=True)
    profile_image_url = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=12, decimal_places=8)
    lng = models.DecimalField(max_digits=12, decimal_places=8)
    created_at = models.DateTimeField()
