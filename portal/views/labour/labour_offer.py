from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from portal.forms import OfferForm
from portal.models import LabourRequest, LabourOffer, LABOUR_STATE_CHOICES


@login_required
def labour_offer(request, id):
    def check_security(labour):
        im_worker = labour.worker.user.id == request.user.id
        im_client = labour.worker.user.id == request.user.id

        if not ((im_client and state_offer_worker) or (im_worker and (state_pending or state_offer_client))):
            redirect('search_list')

    labour_request = LabourRequest.objects.get(id=int(id))
    state_pending = LABOUR_STATE_CHOICES[0]
    state_offer_worker = LABOUR_STATE_CHOICES[8]
    state_offer_client = LABOUR_STATE_CHOICES[9]
    check_security(labour_request)

    if request.method == 'POST':
        context = {}
        offer_form = OfferForm(request.POST)

        if offer_form.is_valid():
            price = offer_form.cleaned_data['price']
            # There's only an offer per Labour. If offer exists, we only rewrite the price of it.
            if labour_request.offer is None:
                offer = LabourOffer(
                    price=price
                )
            else:
                offer = labour_request.offer
                offer.price = price
            offer.save()

            if labour_request.state == state_pending or labour_request.state == state_offer_client:
                labour_request.state = state_offer_worker
            else:
                labour_request.state = state_offer_client
            labour_request.offer = offer
            labour_request.save()

            return redirect('labour_display', id=labour_request.id)
        context['labour_offer_form'] = offer_form
        context['labour'] = labour_request

    else:

        context = {'labour': labour_request}
        labour_offer_form = OfferForm()
        context['labour_offer_form'] = labour_offer_form

    return render(request, 'labour_offer.html', context)
