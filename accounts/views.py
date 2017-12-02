from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import UserForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
# this login required decorator is to not allow to any
# view without authenticating
@login_required(login_url="login/")
def dashboard(request):
    return render(request, "dashboard.html")


# def login(request):
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         # Redirect to a success page.
#         return redirect('dashboard')
#     else:
#         # Return an 'invalid login' error message.
#         return redirect('home')

# def logout_view(request):
#     logout(request)

# def login_form(request):
#     return render(request, "login.html")


class UserFormView(View):
    form_class = UserForm
    template_name = 'registration_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    #process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            #clean data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            #returns User object if credentials are correct

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('dashboard')

        return render(request, self.template_name, {'form': form})