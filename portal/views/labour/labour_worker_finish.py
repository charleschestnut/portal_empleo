from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from portal.models import LabourRequest, LABOUR_STATE_CHOICES


@login_required
def labour_worker_finish(request, id):
    labour = LabourRequest.objects.get(id=int(id))

    soy_trabajor = labour.worker.user.id == request.user.id
    esta_en_marcha = labour.state == LABOUR_STATE_CHOICES[1]

    if soy_trabajor and esta_en_marcha:
        labour.state = LABOUR_STATE_CHOICES[2]
        labour.save()

        return redirect('labour_list_in_process')
    else:
        return render(request, 'search_list.html')
