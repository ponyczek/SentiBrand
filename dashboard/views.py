from django import template
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from scrapper.scrapper import get_tweets
from .forms import SingleSearchForm

register = template.Library()


@login_required(login_url="login/")
def dashboard(request):
    # tweets = get_tweets()
    # context = {'tweets': tweets }
    return render(request, "dashboard.html")


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

