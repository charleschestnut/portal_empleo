from django.shortcuts import render, redirect
from portal.models import LabourRequest, LABOUR_STATE_CHOICES
import datetime
from django.contrib.auth.decorators import login_required


@login_required
def labour_total_finish(request, id):
    labour = LabourRequest.objects.get(id=int(id))

    soy_creador = labour.creator.user.id == request.user.id
    esta_end_worker = labour.state == LABOUR_STATE_CHOICES[2]
    soy_trabajador = labour.worker.user.id == request.user.id
    esta_end_client = labour.state == LABOUR_STATE_CHOICES[3]

    if soy_creador and esta_end_worker:

        labour.state = LABOUR_STATE_CHOICES[4]
        labour.finish_datetime = datetime.datetime.now()
        labour.save()
        return redirect('labour_list_in_process')

    elif soy_trabajador and esta_end_client:

        labour.state = LABOUR_STATE_CHOICES[4]
        labour.finish_datetime = datetime.datetime.now()
        labour.save()
        return redirect('labour_list_in_process')

    else:
        return render(request, 'search_list.html')
