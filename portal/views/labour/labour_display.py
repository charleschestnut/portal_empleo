from django.shortcuts import render, redirect
from portal.models import LabourRequest, LabourImage, WorkerRating, ClientRating


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

    print(labour_images)
    context = {'labour_images': labour_images,
               'labour': labour,
               'worker_rating': worker_rating,
               'client_rating': client_rating}

    return render(request, 'labour_display.html', context)
