import datetime

from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import render, redirect

from portal.forms import LabourRequestForm, ImageForm
from portal.models import LabourRequest, Profile, LABOUR_STATE_CHOICES, LabourChat, LabourImage


@login_required
def labour_request(request, id):
    worker = Profile.objects.get(user_id=int(id))
    ImageFormSet = modelformset_factory(LabourImage,
                                        form=ImageForm, extra=5)
    # 'extra' means the number of photos that you can upload  ^
    if request.method == 'POST':
        labour_form = LabourRequestForm(request.POST)
        multiple_images = request.FILES.getlist('images')
        context = {}

        if labour_form.is_valid() and worker.user.id != request.user.id:
            creator = Profile.objects.get(user_id=request.user.id)
            state = LABOUR_STATE_CHOICES[0]
            description = labour_form.cleaned_data['description']
            price = labour_form.cleaned_data['price']
            title = labour_form.cleaned_data['title']

            labour = LabourRequest(
                title=title,
                description=description,
                state=state,
                start_datetime=None,
                finish_datetime=None,
                price=price,
                creator=creator,
                worker=worker
            )
            labour.save()

            for pic in multiple_images:
                # this helps to not crash if the user
                # do not upload all the photos
                if pic:
                    picture = LabourImage(image=pic, labour=labour)
                    picture.save()
            # Creamos el chat una vez se crea la Labour Request
            crear_chat(labour.id)
            return redirect('profile_display', id=worker.user_id)
        context['labour_request_form'] = labour_form
        context['worker'] = worker

    else:
        context = {'worker': worker}
        labour_form = LabourRequestForm()
        formset = ImageFormSet(queryset=LabourImage.objects.none())
        context['labour_request_form'] = labour_form
        context['formset'] = formset

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
