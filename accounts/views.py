from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import View
from .models import UserProfile
from .forms import UserForm, EditProfileForm, EditProfileAvatarForm


class UserFormView(View):
    form_class = UserForm
    template_name = 'registration_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # clean data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns User object if credentials are correct

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('dashboard')

        return render(request, self.template_name, {'form': form})


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            if(request.FILES):
                avatar = request.FILES['avatar']
                user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                user_profile.avatar = avatar
                user_profile.user = request.user
                user_profile.save()
                user_avatar = UserProfile.objects.get(user_id=request.user.id)
                avatar_form = EditProfileAvatarForm(instance=user_avatar)
                context = {'form': form, 'avatar_form': avatar_form, 'success': 'Profile information has been updated.', 'avatar': user_avatar}
                return render(request, 'edit_profile.html', context)
            else:
                context = {'form': form, 'error': 'Image deleted.'}
                return render(request, 'edit_profile.html', context)
        else:
            context = {'form': form, 'error': 'Something went wrong with your submission'}
            return render(request, 'dashboard.html', context)
    else:
        form = EditProfileForm(instance=request.user)
        avatar_form = EditProfileAvatarForm()
        try:
            user_avatar = UserProfile.objects.get(user_id=request.user.id)
            avatar_form = EditProfileAvatarForm(instance=user_avatar)
            context = {'form': form, 'avatar_form': avatar_form, 'avatar': user_avatar}
        except  UserProfile.DoesNotExist:
            context = {'form': form, 'avatar_form': avatar_form }
        return render(request, 'edit_profile.html', context)
