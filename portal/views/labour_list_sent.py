from django.shortcuts import render
from portal.models import LabourRequest, LABOUR_STATE_CHOICES


def labour_list_sent(request):
    state_pending = LABOUR_STATE_CHOICES[0]

    labour_request_list = LabourRequest.objects.filter(creator__user__id=request.user.id)
    title = 'My sent requests'
    return render(request, 'labour_list.html', locals())
