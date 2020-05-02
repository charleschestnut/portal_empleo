from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from portal.models import LabourRequest, LABOUR_STATE_CHOICES


@login_required
def labour_reject(request, id):
    labour = LabourRequest.objects.get(id=int(id))

    soy_trabajador = labour.worker.user.id == request.user.id
    esta_pendiente = labour.state == LABOUR_STATE_CHOICES[0]

    if soy_trabajador and esta_pendiente:
        labour.state = LABOUR_STATE_CHOICES[4]
        labour.save()
        return redirect('labour_list_pending')
    else:
        return render(request, 'search_list.html')
