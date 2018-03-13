from django import template
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, render_to_response
from django.utils import timezone
from accounts.models import UserProfile
from .forms import PhraseForm
from .models import UserPhrase, Phrase
from django.http import HttpResponseRedirect, JsonResponse
from scrapper.models import Search, Tweet
from django.urls import reverse
from django.core import serializers
import json
import datetime
import numpy as np
from scrapper.scrapper import  serialise_data
from django.core.serializers.json import DjangoJSONEncoder

register = template.Library()


@login_required(login_url="login/")
def dashboard(request):
    user_phrases = UserPhrase.objects.filter(user_id=request.user)
    try:
        user_avatar = UserProfile.objects.get(user_id=request.user.id)
        return render(request, 'dashboard.html', {'phrases': user_phrases, 'avatar': user_avatar, 'active': True})
    except  UserProfile.DoesNotExist:
        return render(request, 'dashboard.html', {'phrases': user_phrases, 'active': True})


@login_required()
def single_search(request):
    template_name = 'search.html'
    #handling only get
    try:
        user_avatar = UserProfile.objects.get(user_id=request.user.id)
        context = {'avatar': user_avatar}
        return render(request, template_name, context)
    except  UserProfile.DoesNotExist:
        return render(request, template_name)


@login_required(login_url="login/")
def add_phrase(request):
    form = PhraseForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user_phrases = UserPhrase.objects.filter(user_id=request.user)
            count_error = (user_phrases.count() >= 5)
            date_error = form.cleaned_data['start_date'] < timezone.now()
            start_end_error = form.cleaned_data['start_date'] > form.cleaned_data['end_date']

            if not count_error and not date_error and not start_end_error:
                user_phrase = UserPhrase()
                phrase_id = form.cleaned_data['phrase']
                phrase, created = Phrase.objects.get_or_create(phrase=phrase_id)
                if created:
                    phrase.save()
                user_phrase.user = request.user
                user_phrase.name = form.cleaned_data['name']
                user_phrase.start_date = form.cleaned_data['start_date']
                user_phrase.end_date = form.cleaned_data['end_date']
                user_phrase.phrase = phrase
                user_phrase.save()
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                errors = []
                if (date_error):
                    errors.append("Provided date must start in the future.")
                if (count_error):
                    errors.append("You have reached the maximum amount of tags (5)")
                if (start_end_error):
                    errors.append("End date cannot be before start date.")
                return render(request, 'add_edit_phrase.html',
                              {'phrases': user_phrases, 'errors': errors, 'form': form, 'edit': False})

    else:
        try:
            user_avatar = UserProfile.objects.get(user_id=request.user.id)
            context = {'form': form, 'avatar': user_avatar}
        except  UserProfile.DoesNotExist:
            context = {'form': form}
        return render(request, 'add_edit_phrase.html', context)


def phrase_detail(request, user_phrase_id):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        user_phrase = get_object_or_404(UserPhrase, pk=user_phrase_id)
        user_phrases = UserPhrase.objects.filter(user_id=request.user)
        search_records = Search.objects.filter(user_phrase=user_phrase_id)
        js_list = []
        for search_record in search_records:
            timestamp_in_sec = int(search_record.created_at.timestamp())
            js_list.append({'search_id': search_record.id, 'created_at': timestamp_in_sec})
        try:
            user_avatar = UserProfile.objects.get(user_id=request.user.id)
            context = {'active_phrase': user_phrase, 'phrases': user_phrases,
                       'search_records': json.dumps(js_list),
                       'avatar': user_avatar,
                       'first_search_date': js_list[0]['created_at'],
                       'last_search_date': js_list[-1]['created_at']}
        except  UserProfile.DoesNotExist:
            context = {'active_phrase': user_phrase,
                       'search_records': json.dumps(js_list),
                       'phrases': user_phrases,
                       'first_search_date': js_list[0]['created_at'],
                       'last_search_date': js_list[-1]['created_at']
                       }
        return render(request, 'phrase_detail.html', context)


@login_required()
def delete_phrase(request, user_phrase_id):
    user_phrase = UserPhrase.objects.get(id=user_phrase_id)
    user_phrase.delete()
    return HttpResponseRedirect(reverse('dashboard'))

@login_required()
def edit_phrase(request, user_phrase_id):
    user_phrase = UserPhrase.objects.get(id=user_phrase_id)

    form = PhraseForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user_phrases = UserPhrase.objects.filter(user_id=request.user)
            start_date_error = form.cleaned_data['start_date'] < timezone.now()
            end_date_start_error = form.cleaned_data['end_date'] > form.cleaned_data['start_date']
            end_date_now_error = form.cleaned_data['end_date'] < timezone.now()
            if not start_date_error:
                phrase_id = form.cleaned_data['phrase']
                phrase, created = Phrase.objects.get_or_create(phrase=phrase_id)
                if created:
                    phrase.save()
                user_phrase.user = request.user
                user_phrase.name = form.cleaned_data['name']
                user_phrase.start_date = form.cleaned_data['start_date']
                user_phrase.end_date = form.cleaned_data['end_date']
                user_phrase.phrase = phrase
                user_phrase.save()
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                errors = []
                if (start_date_error):
                    errors.append("Provided date must start in the future.")
                if (end_date_start_error):
                    errors.append("End date must be greater than start date.")
                if (end_date_now_error):
                    errors.append("End date must start in the future.")
                return render(request, 'add_edit_phrase.html',
                              {'phrases': user_phrases, 'errors': errors, 'form': form, 'edit': False})
    else:
        start_date = user_phrase.start_date.strftime("%Y-%m-%dT%H:%M")
        end_date = user_phrase.end_date.strftime("%Y-%m-%dT%H:%M")
        data = {'name': user_phrase.name, 'start_date': start_date, 'end_date': end_date, 'phrase': user_phrase.phrase.phrase}
        form = PhraseForm(initial=data)
        return render(request, 'add_edit_phrase.html', {'form': form, 'edit': True, 'id': user_phrase.id})

@login_required()
def phrase_detail_analysis(request,user_phrase_id):
    search_ids = np.array(json.loads(request.GET['search_ids']))
    print(search_ids)
    tweets = Tweet.objects.filter(search_id__in=search_ids)
    serialised_tweets = serialise_tweets(tweets)
    return JsonResponse(dict(tweets=list(serialised_tweets)))


def serialise_tweets(tweets):
    data = []
    for tweet in tweets:
        data.append({
            'text': tweet.content,
            'user': tweet.username,
            'polarity': tweet.polarity,
            'lat': tweet.lat,
            'lng': tweet.lng,
            'created_at': tweet.created_at,
            'profile_image_url' : tweet.profile_image_url,
            'id' : tweet.tweet_id,
            'search_id' : tweet.search_id.id,
            'search_date': tweet.search_id.created_at
        })
        print(tweet.search_id)
    return data
