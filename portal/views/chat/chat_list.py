from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from portal.models import LabourChat


@login_required
def chat_list(request):
    filter = Q(labour__worker__user__id=request.user.id) | Q(labour__creator__user__id=request.user.id)

    chat_list = LabourChat.objects.filter(filter)
    title = 'My open chats'
    context = {'chat_list': chat_list}
    context['title'] = title
    return render(request, 'chat_list.html', context)
