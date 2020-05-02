from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from portal.models import LabourRequest, LABOUR_STATE_CHOICES


@login_required
def payment_sucessful(request, id):
    labour = LabourRequest.objects.get(id=int(id))
    soy_creador = request.user.id == labour.creator.user.id
    esta_terminada = labour.state == LABOUR_STATE_CHOICES[4]

    if soy_creador and esta_terminada:
        labour.state = LABOUR_STATE_CHOICES[7]
        labour.save()
        return redirect('done')
    else:
        return redirect('search_list')
