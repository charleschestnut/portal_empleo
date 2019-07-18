from django.shortcuts import render
from portal.models import LabourRequest, LABOUR_STATE_CHOICES


def labour_list_pending(request):
    state_pending = LABOUR_STATE_CHOICES[0]

    labour_request_list = LabourRequest.objects.filter(worker__user__id=request.user.id).filter(state__exact=state_pending)
    title = 'My pending requests'
    return render(request, 'labour_list.html', locals())
