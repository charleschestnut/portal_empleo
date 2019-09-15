from django.shortcuts import render


def admin_search(request):
    return render(request, 'chat_display.html')
