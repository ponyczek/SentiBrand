from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.
# this login required decorator is to not allow to any
# view without authenticating
@login_required(login_url="login/")
def dashboard(request):
    return render(request,"dashboard.html")

