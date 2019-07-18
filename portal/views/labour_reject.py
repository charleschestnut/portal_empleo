from django.shortcuts import render
from portal.models import LabourRequest, LABOUR_STATE_CHOICES
import datetime


def labour_reject(request, id):
    labour = LabourRequest.objects.get(id=int(id))

    soy_trabajador = labour.worker.id == request.user.id
    esta_pendiente = labour.state == LABOUR_STATE_CHOICES[0]

    if(soy_trabajador and esta_pendiente):
        labour.state = LABOUR_STATE_CHOICES[4]
        labour.save()
        labour_list = LabourRequest.objects.filter(state__exact=LABOUR_STATE_CHOICES[0])
        context = {'labour_request_list': labour_list}
        return render(request, 'labour_list.html', context)
    else:
        return render(request, 'search_list.html')
