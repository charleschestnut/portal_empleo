from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from portal.models import LabourRequest, LABOUR_STATE_CHOICES
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


@login_required
def payment_process(request, id):
    labour = LabourRequest.objects.get(id=int(id))
    soy_creador = request.user.id == labour.creator.user.id
    en_proceso = labour.state == LABOUR_STATE_CHOICES[1]

    if soy_creador and en_proceso:
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': '%.2f' % float(labour.price),
            'item_name': 'Order {}'.format(labour.id),
            'invoice': str(labour.id),
            'currency_code': 'EUR',
            'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
            'return_url': request.build_absolute_uri(reverse('payment_successful',  kwargs={'id': id})),
            'cancel_return': request.build_absolute_uri(reverse('cancelled')),
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        return render(request, 'process.html', {'order': labour,
                                                        'form': form})
    else:
        return render(request, 'search_list.html')
