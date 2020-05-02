from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm

from portal.models import LabourRequest, LABOUR_STATE_CHOICES


@login_required
def payment_process(request, id):
    labour = LabourRequest.objects.get(id=int(id))
    soy_creador = request.user.id == labour.creator.user.id
    esta_terminado = labour.state == LABOUR_STATE_CHOICES[4]

    if soy_creador and esta_terminado:
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': '%.2f' % float(labour.price),
            'item_name': 'Order {}'.format(labour.id),
            'invoice': str(labour.id),
            'currency_code': 'EUR',
            'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
            'return_url': request.build_absolute_uri(reverse('payment_successful', kwargs={'id': id})),
            'cancel_return': request.build_absolute_uri(reverse('cancelled')),
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        return render(request, 'process.html', {'order': labour,
                                                'form': form})
    else:
        return render(request, 'search_list.html')
