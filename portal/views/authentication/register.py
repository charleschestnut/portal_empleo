from portal.forms import LoginForm, UserRegistrationForm
from portal.models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate



def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            # Create the user profile
            new_user.save()
            Profile.objects.create(user=new_user)
            user = authenticate(username=new_user.username, password=new_user.password)
            login(request, user)

            context = {'new_user': new_user}
            return redirect(request, 'registration/register_done.html', context)
    else:
        user_form = UserRegistrationForm()

    context = {'user_form': user_form}
    return render(request, 'registration/register.html', context)
