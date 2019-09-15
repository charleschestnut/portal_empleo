from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from portal.models import LabourRequest, Profile, LABOUR_STATE_CHOICES, LabourChat
from portal.forms import LabourRequestForm
import datetime



@login_required
def labour_request(request, id):
    worker = Profile.objects.get(user_id=int(id))
    if request.method == 'POST':
        labour_form = LabourRequestForm(request.POST)
        context = {}

        if labour_form.is_valid() and worker.user.id != request.user.id:
            creator = Profile.objects.get(user_id=request.user.id)
            state = LABOUR_STATE_CHOICES[0]
            description = labour_form.cleaned_data['description']

            labour = LabourRequest(
                description=description,
                state=state,
                start_datetime=None,
                finish_datetime=None,
                creator=creator,                worker=worker
            )
            labour.save()

            #Creamos el chat una vez se crea la Labour Request
            crear_chat(labour.id)

            return redirect('profile_display', id=worker.user_id)
        context['labour_request_form'] = labour_form
        context['worker'] = worker

    else:
        context = {'worker': worker}
        labour_form = LabourRequestForm()
        context['labour_request_form'] = labour_form

    return render(request, 'labour_request_request.html', context)


def crear_chat(labour_id):
    now = datetime.datetime.now()
    labour = LabourRequest.objects.get(id=labour_id)
    chat = LabourChat(
        creation_datetime=now,
        last_message_datetime=now,
        labour=labour,
    )
    chat.save()
