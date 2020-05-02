from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@login_required
def payment_cancelled(request):
    return render(request, 'cancelled.html')
