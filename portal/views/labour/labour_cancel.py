from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from portal.models import LabourRequest, LABOUR_STATE_CHOICES


@login_required
def labour_cancel(request, id):
    labour = LabourRequest.objects.get(id=int(id))

    soy_trabajor = labour.worker.user.id == request.user.id
    soy_cliente = labour.creator.user.id == request.user.id
    esta_en_proceso = labour.state == LABOUR_STATE_CHOICES[1]

    if (soy_trabajor or soy_cliente) and esta_en_proceso:
        labour.state = LABOUR_STATE_CHOICES[5]
        labour.save()

        return redirect('labour_list_pending')
    else:
        return render(request, 'search_list.html')
