from django import template
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone
from scrapper.scrapper import get_tweets
from .forms import SingleSearchForm, PhraseForm
from .models import User_Phrase, Phrase
from django.shortcuts import render, get_object_or_404


register = template.Library()


@login_required(login_url="login/")
def dashboard(request):
    # tweets = get_tweets()
    # context = {'tweets': tweets }
    # form = PhraseForm(request.POST or None)
    user_phrases = User_Phrase.objects.filter(user_id=request.user)
    return render(request, 'dashboard.html', {'phrases': user_phrases, 'active':True })

@login_required()
def single_search(request):
    template_name = 'search.html'

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        form = SingleSearchForm(request.POST)
        # return render(request, "search.html", context)
        tweets = get_tweets(request.POST['query_phrase'])
        context = {'tweets': tweets}
        return render(request, template_name, context)
    else:
        form = SingleSearchForm(initial={'query_phrase': '', })

        return render(request, template_name)

@login_required(login_url="login/")
def add_phrase(request):
    format = "%Y-%m-%d %H:%M:%S"
    if request.method == 'POST':
        form = PhraseForm(request.POST or None)
        if form.is_valid():
            if(form.cleaned_data['start_date'] > timezone.now()):
                user_phrase = User_Phrase()
                phrase_id = form.cleaned_data['phrase']
                phrase, created= Phrase.objects.get_or_create(phrase=phrase_id)
                if created:
                    phrase.save()
                # if form.is_valid():
                # user_phrase = form.save(commit=False)
                user_phrase.user = request.user
                user_phrase.name = form.cleaned_data['name']
                user_phrase.start_date = form.cleaned_data['start_date']
                user_phrase.phrase = phrase
                user_phrase.save()
                user_phrases = User_Phrase.objects.filter(user_id=request.user)
                return render(request, 'dashboard.html', {'phrases': user_phrases, 'success': True})
            else:
                form = PhraseForm()
                context = {
                    "form": form,
                    "error_date": True
                }
                return render(request, 'add_phrase.html', context)

    else:
        form = PhraseForm()
        context = {
            "form": form,
        }
        return render(request, 'add_phrase.html', context)

def phrase_detail(request, user_phrase_id):
    print(user_phrase_id)
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        user_phrase = get_object_or_404(User_Phrase, pk=user_phrase_id)
        user_phrases = User_Phrase.objects.filter(user_id=request.user)
        return render(request, 'phrase_detail.html', {'active_phrase': user_phrase, 'phrases':user_phrases})

