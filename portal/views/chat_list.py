from django.shortcuts import render
from ..models import LabourChat
from django.db.models import Q


def chat_list(request):

    filter = Q(labour__worker__user__id=request.user.id) | Q(labour__creator__user__id=request.user.id)

    chat_list = LabourChat.objects.filter(filter)
    title = 'My open chats'
    context = {'chat_list': chat_list}
    context['title'] = title
    return render(request, 'chat_list.html', context)
