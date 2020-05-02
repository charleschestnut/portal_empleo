from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from portal.forms import UserEditForm, ProfileForm


@login_required
def profile_edit(request):
    context = {}
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileForm(instance=request.user.profile,
                                   data=request.POST,
                                   files=request.FILES)
        print(request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile_display', id=request.user.id)
        context['user_form'] = user_form
        context['profile_form'] = profile_form
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        context['user_form'] = user_form
        context['profile_form'] = profile_form

    return render(request, 'profile_edit.html', context)
