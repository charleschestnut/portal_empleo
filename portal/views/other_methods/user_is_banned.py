from django.contrib.auth import logout
from django.shortcuts import redirect


def check_user_is_banned(request):

    if request.user.profile.banning:
        logout(request)
        redirect('banned_user_view', id=request.user.id)