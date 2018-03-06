from django.db import models

from dashboard.models import UserPhrase


class Search(models.Model):
    user_phrase = models.ForeignKey(UserPhrase, on_delete=models.CASCADE)  # must be changed to user_phrase
    created_at = models.DateTimeField(auto_now_add=True)


class Tweet(models.Model):
    search_id = models.ManyToManyField(Search)
    username = models.CharField(max_length=50, null=False)
    user_location = models.CharField(max_length=50)
    polarity = models.DecimalField(decimal_places=3, max_digits=6)
    tweet_id = models.BigIntegerField(primary_key=True, null=False)
    profile_image_url = models.CharField(max_length=100, null=True)
    lat = models.DecimalField(max_digits=12, decimal_places=8, null=True)
    lng = models.DecimalField(max_digits=12, decimal_places=8, null=True)
    created_at = models.DateTimeField(null=False)
    content = models.CharField(max_length=140, null=False)
