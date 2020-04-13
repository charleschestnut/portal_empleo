from django.shortcuts import render


def banned_user_view(request, id):

    return render(request, 'chat_list.html')