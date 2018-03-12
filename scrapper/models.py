from django.db import models

from dashboard.models import UserPhrase


class Search(models.Model):
    user_phrase = models.ForeignKey(UserPhrase, on_delete=models.CASCADE)  # must be changed to user_phrase
    created_at = models.DateTimeField(auto_now_add=True)


class Tweet(models.Model):
    search_id = models.ForeignKey(Search, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, null=False)
    polarity = models.DecimalField(decimal_places=3, max_digits=6)
    tweet_id = models.BigIntegerField(primary_key=True, null=False)
    profile_image_url = models.CharField(max_length=150, null=True)
    lat = models.DecimalField(max_digits=12, decimal_places=8, null=True)
    lng = models.DecimalField(max_digits=12, decimal_places=8, null=True)
    created_at = models.DateTimeField(null=False)
    content = models.CharField(max_length=330, null=False)
