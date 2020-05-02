from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from portal.models import LabourRequest, LABOUR_STATE_CHOICES


@login_required
def labour_list_pending(request):
    state_pending = LABOUR_STATE_CHOICES[0]
    state_offer_client = LABOUR_STATE_CHOICES[9]
    state_offer_worker = LABOUR_STATE_CHOICES[8]
    filter_user = Q(worker__user__id=request.user.id) | Q(creator__user__id=request.user.id)
    filter_states = Q(state__exact=state_pending) | Q(state__exact=state_offer_client) | \
                    Q(state__exact=state_offer_worker)

    labour_request_list = LabourRequest.objects.filter(filter_user).filter(filter_states)
    title = 'My pending labours'
    return render(request, 'labour_list.html', locals())
