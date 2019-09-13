from django.shortcuts import render
from portal.models import LabourRequest, LABOUR_STATE_CHOICES
from django.db.models import Q
from django.contrib.auth.decorators import login_required


@login_required
def labour_list_finished(request):
    state_first_end = LABOUR_STATE_CHOICES[2]
    state_finished = LABOUR_STATE_CHOICES[3]

    filter_states = (Q(state__exact=state_finished) | Q(state__exact=state_first_end)) & (Q(worker__user__id=request.user.id) | Q(creator__user__id=request.user.id))

    labour_request_list = LabourRequest.objects.filter(filter_states)

    title = 'My finished labours'
    context = {'labour_request_list': labour_request_list}
    context['title'] = title
    return render(request, 'labour_list.html', context)
