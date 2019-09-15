from django.shortcuts import render


def admin_rating_ban(request, id):
    return render(request, 'chat_display.html')
