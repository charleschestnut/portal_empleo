from django.shortcuts import render
from portal.models import LabourRequest, LABOUR_STATE_CHOICES
import datetime


def labour_total_finish(request, id):
    labour = LabourRequest.objects.get(id=int(id))

    soy_creador = labour.creator.id == request.user.id
    esta_end_work = labour.state == LABOUR_STATE_CHOICES[2]

    if(soy_creador and esta_end_work):
        labour.state = LABOUR_STATE_CHOICES[3]
        labour.finish_datetime = datetime.datetime.now()
        labour.save()
        labour_list = LabourRequest.objects.filter(state__exact=LABOUR_STATE_CHOICES[1])
        context = {'labour_request_list': labour_list}
        return render(request, 'labour_list.html', context)
    else:
        return render(request, 'search_list.html')
