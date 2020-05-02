from django.shortcuts import render

from portal.models import LabourRequest, LabourImage, WorkerRating, ClientRating, LABOUR_STATE_CHOICES


def labour_display(request, id):
    labour_id = int(id)
    labour = LabourRequest.objects.get(id=labour_id)
    labour_images = LabourImage.objects.filter(labour__id=labour_id)
    try:
        worker_rating = WorkerRating.objects.get(labour_id=labour_id)
    except WorkerRating.DoesNotExist:
        worker_rating = None
    try:
        client_rating = ClientRating.objects.get(labour_id=labour_id)
    except ClientRating.DoesNotExist:
        client_rating = None
    im_worker = request.user.id == labour.worker.user.id
    im_creator = request.user.id == labour.creator.user.id
    can_offer_worker = labour.state == LABOUR_STATE_CHOICES[0] or labour.state == LABOUR_STATE_CHOICES[9]
    can_offer_client = labour.state == LABOUR_STATE_CHOICES[8]
    print(LABOUR_STATE_CHOICES[0], LABOUR_STATE_CHOICES[8], LABOUR_STATE_CHOICES[9])
    print(im_worker, im_creator, can_offer_worker, can_offer_client, labour.state)

    context = {'labour_images': labour_images,
               'labour': labour,
               'worker_rating': worker_rating,
               'client_rating': client_rating,
               'im_worker': im_worker,
               'im_creator': im_creator,
               'can_offer_client': can_offer_client,
               'can_offer_worker': can_offer_worker}

    return render(request, 'labour_display.html', context)
