from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from portal.models import LabourRequest, LABOUR_STATE_CHOICES
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


@login_required
def payment_sucessful(request, id):
    labour = LabourRequest.objects.get(id=int(id))
    soy_creador = request.user.id == labour.creator.user.id
    en_proceso = labour.state == LABOUR_STATE_CHOICES[1]

    if soy_creador and en_proceso:
        labour.state = LABOUR_STATE_CHOICES[7]
        return redirect('done')
    else:
        return redirect('search_list')
