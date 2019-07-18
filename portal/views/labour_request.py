from django.shortcuts import render
from portal.models import LabourRequest, Profile, LABOUR_STATE_CHOICES
from ..forms import LabourRequestForm


def labour_request(request, id):
    worker = Profile.objects.get(user_id=int(id))
    if request.method == 'POST':
        labour_form = LabourRequestForm(request.POST)

        if labour_form.is_valid():
            creator = Profile.objects.get(user_id=request.user.id)
            state = LABOUR_STATE_CHOICES[0]
            description = labour_form.cleaned_data['description']

            labour = LabourRequest(
                description=description,
                state=state,
                start_datetime=None,
                finish_datetime=None,
                creator=creator,
                worker=worker
            )
            labour.save()

            context = {'worker': worker}
            return render(request, 'profile_display.html', context)

    else:
        context = {'worker': worker}
        labour_form = LabourRequestForm()
        context['labour_request_form'] = labour_form
    return render(request, 'labour_request_request.html', context)
