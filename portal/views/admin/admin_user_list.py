from django.shortcuts import render


def admin_user_list(request):
    return render(request, 'chat_display.html')
