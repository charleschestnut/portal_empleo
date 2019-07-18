from ..forms import LoginForm, UserRegistrationForm
from ..models import Profile
from django.shortcuts import render


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
            Profile.objects.create(user=new_user)
            new_user.save()
            context = {'new_user': new_user}
            return render(request, 'account/register_done.html', context)
    else:
        user_form = UserRegistrationForm()
        context = {'user_form': user_form}
    return render(request, 'registration/register.html', context)
