from django import template
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


from scrapper.scrapper import get_tweets
from .forms import SingleSearchForm, PhraseForm
from .models import User_Phrase, Phrase


register = template.Library()


@login_required(login_url="login/")
def dashboard(request):
    # tweets = get_tweets()
    # context = {'tweets': tweets }
    # form = PhraseForm(request.POST or None)
    user_phrases = User_Phrase.objects.filter(user_id=request.user)
    return render(request, 'dashboard.html', {'phrases': user_phrases, 'active': True})


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
    form = PhraseForm(request.POST or None)
    if request.method == 'POST':

        if form.is_valid():
            user_phrases = User_Phrase.objects.filter(user_id=request.user)
            count_error = (user_phrases.count() >= 5)
            date_error = form.cleaned_data['start_date'] < timezone.now()

            if not count_error and not date_error:
                user_phrase = User_Phrase()
                phrase_id = form.cleaned_data['phrase']
                phrase, created = Phrase.objects.get_or_create(phrase=phrase_id)
                if created:
                    phrase.save()
                user_phrase.user = request.user
                user_phrase.name = form.cleaned_data['name']
                user_phrase.start_date = form.cleaned_data['start_date']
                user_phrase.phrase = phrase
                user_phrase.save()
                return render(request, 'dashboard.html', {'phrases': user_phrases, 'success': 'You successfully added the search phrase.'})
            else:
                errors = []
                if (date_error):
                    errors.append("Provided date must start in the future.")
                if (count_error):
                    errors.append("You have reached the maximum amount of tags (5)")
                return render(request, 'add_phrase.html', {'phrases': user_phrases, 'errors': errors, 'form': form})


    else:
        context = {
            "form": form,
        }
        return render(request, 'add_phrase.html', context)


def phrase_detail(request, user_phrase_id):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        user_phrase = get_object_or_404(User_Phrase, pk=user_phrase_id)
        user_phrases = User_Phrase.objects.filter(user_id=request.user)
        return render(request, 'phrase_detail.html', {'active_phrase': user_phrase, 'phrases': user_phrases})

@login_required()
def delete_phrase(request, user_phrase_id):
    user_phrase = User_Phrase.objects.get(id=user_phrase_id)
    user_phrase.delete()
    user_phrases = User_Phrase.objects.filter(user_id=request.user)
    return render(request, 'dashboard.html', {'phrases': user_phrases, 'success': 'Phrase has been deleted.'})
    # return HttpResponseRedirect(reverse('/'))