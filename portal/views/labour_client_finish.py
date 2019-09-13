from django.shortcuts import render, redirect
from portal.models import LabourRequest, LABOUR_STATE_CHOICES
from django.contrib.auth.decorators import login_required


@login_required
def labour_client_finish(request, id):
    labour = LabourRequest.objects.get(id=int(id))

    soy_cliente = labour.creator.user.id == request.user.id
    esta_en_marcha = labour.state == LABOUR_STATE_CHOICES[1]


    if(soy_cliente and esta_en_marcha):
        labour.state = LABOUR_STATE_CHOICES[3]
        labour.save()

        return redirect('labour_list_in_process')
    else:
        return render(request, 'search_list.html')
