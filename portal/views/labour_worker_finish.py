from django.shortcuts import render
from portal.models import LabourRequest, LABOUR_STATE_CHOICES
import datetime


def labour_worker_finish(request, id):
    labour = LabourRequest.objects.get(id=int(id))

    soy_trabajor = labour.worker.id == request.user.id
    esta_en_marcha = labour.state == LABOUR_STATE_CHOICES[1]

    if(soy_trabajor and esta_en_marcha):
        labour.state = LABOUR_STATE_CHOICES[2]
        labour.save()
        labour_list = LabourRequest.objects.filter(state__exact=LABOUR_STATE_CHOICES[1])
        context = {'labour_request_list': labour_list}
        return render(request, 'labour_list.html', context)
    else:
        return render(request, 'search_list.html')
