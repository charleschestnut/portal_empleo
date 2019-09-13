from django.shortcuts import render
from portal.models import LabourRequest, LABOUR_STATE_CHOICES
import datetime
from django.contrib.auth.decorators import login_required


@login_required
def labour_accept(request, id):
    labour = LabourRequest.objects.get(id=int(id))

    soy_trabajor = labour.worker.user.id == request.user.id
    esta_pendiente = labour.state == LABOUR_STATE_CHOICES[0]
    print(soy_trabajor)
    print(esta_pendiente)
    if(soy_trabajor and esta_pendiente):
        labour.state = LABOUR_STATE_CHOICES[1]
        labour.start_datetime = datetime.datetime.now()
        labour.save()
        labour_list = LabourRequest.objects.filter(state__exact=LABOUR_STATE_CHOICES[0])
        context = {'labour_request_list': labour_list}
        return render(request, 'labour_list.html', context)
    else:
        return render(request, 'search_list.html')
