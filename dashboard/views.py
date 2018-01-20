from django import template
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from scrapper.scrapper import get_tweets
from .forms import SingleSearchForm, PhraseForm
from .models import User_Phrase
from django.shortcuts import render, get_object_or_404


register = template.Library()


@login_required(login_url="login/")
def dashboard(request):
    # tweets = get_tweets()
    # context = {'tweets': tweets }
    # form = PhraseForm(request.POST or None)
    user_phrases = User_Phrase.objects.filter(user_id=request.user)
    return render(request, 'dashboard.html', {'phrases': user_phrases, 'active':True })

# @login_required(login_url="login/")
def single_search(request):

    # return render(request, "search.html", context)

    # form_class = SingleSearchForm
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
    form = PhraseForm(request.POST or None)

    print(form.errors)
    if request.method == 'POST':

        if form.is_valid():
            phrase = form.save(commit=False)
            phrase.user = request.user
            phrase.save()
            user_phrases = User_Phrase.objects.filter(user_id=request.user)
            return render(request, 'dashboard.html', {'phrases': user_phrases})

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