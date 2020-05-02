import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from portal.models import LabourRequest, LABOUR_STATE_CHOICES


@login_required
def labour_accept(request, id):
    labour = LabourRequest.objects.get(id=int(id))
    soy_cliente = labour.creator.user.id = request.user.id
    soy_trabajor = labour.worker.user.id == request.user.id
    esta_pendiente = labour.state == LABOUR_STATE_CHOICES[0]
    ofertado_trabajador = labour.state == LABOUR_STATE_CHOICES[8]
    ofertado_cliente = labour.state == LABOUR_STATE_CHOICES[9]

    if soy_trabajor and esta_pendiente:
        labour.state = LABOUR_STATE_CHOICES[1]
        labour.start_datetime = datetime.datetime.now()
        labour.save()
        return redirect('labour_list_pending')

    elif (soy_trabajor and ofertado_cliente) or (soy_cliente and ofertado_trabajador):
        labour.state = LABOUR_STATE_CHOICES[1]
        labour.start_datetime = datetime.datetime.now()
        labour.price = labour.offer.price
        labour.save()
        return redirect('labour_list_pending')
    else:
        return render(request, 'search_list.html')
