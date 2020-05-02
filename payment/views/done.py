from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@login_required
def payment_done(request):
    return render(request, 'done.html')
