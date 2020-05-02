from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from portal.models import LabourRequest, LABOUR_STATE_CHOICES


@login_required
def labour_list_in_process(request):
    state_in_process = LABOUR_STATE_CHOICES[1]
    state_end_worker = LABOUR_STATE_CHOICES[2]
    state_end_client = LABOUR_STATE_CHOICES[3]

    filter_labour = (Q(worker__user__id=request.user.id) | Q(creator__user__id=request.user.id)) & (
            Q(state__exact=state_in_process) | Q(state__exact=state_end_worker) | Q(state__exact=state_end_client))
    labour_request_list = LabourRequest.objects.filter(filter_labour)

    title = 'My actual labours'
    return render(request, 'labour_list.html', locals())
