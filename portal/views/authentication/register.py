from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from portal.forms import UserRegistrationForm, ProfileForm


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST, prefix='user')
        profile_form = ProfileForm(request.POST, prefix='profile', files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_profile = profile_form.save(commit=False)
            new_user.save()
            new_profile.user = new_user
            new_profile.picture = request.FILES['profile-picture']
            new_profile.save()
            user = authenticate(username=new_user.username, password=new_user.password)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                context = {'new_user': new_user}
                return redirect(request, 'registration/register_done.html', context)
            else:
                return redirect('login')
    else:
        user_form = UserRegistrationForm(prefix='user')
        profile_form = ProfileForm(prefix='profile')

    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'registration/register.html', context)
