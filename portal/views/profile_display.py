from django.shortcuts import render
from portal.models import *


def profile_display(request, id):
    user_id = int(id)
    worker = Profile.objects.get(user_id=user_id)
    return render(request, 'profile_display.html', locals())