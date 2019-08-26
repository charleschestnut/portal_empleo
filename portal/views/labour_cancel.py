from django.shortcuts import render
from portal.models import LabourRequest, LABOUR_STATE_CHOICES
import datetime


def labour_cancel(request, id):
    labour = LabourRequest.objects.get(id=int(id))

    soy_trabajor = labour.worker.user.id == request.user.id
    soy_cliente = labour.creator.user.id == request.user.id
    esta_en_proceso = labour.state == LABOUR_STATE_CHOICES[1]

    if((soy_trabajor or soy_cliente) and esta_en_proceso):
        labour.state = LABOUR_STATE_CHOICES[5]
        labour.save()
        labour_list = LabourRequest.objects.filter(state__exact=LABOUR_STATE_CHOICES[1])
        context = {'labour_request_list': labour_list}
        return render(request, 'labour_list.html', context)
    else:
        return render(request, 'search_list.html')
