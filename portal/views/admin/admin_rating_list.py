from django.shortcuts import render


def admin_rating_list(request):
    return render(request, 'chat_display.html')
