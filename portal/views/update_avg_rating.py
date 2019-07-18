from portal.models import Profile, ClientRating, WorkerRating
from django.db.models import Avg

def update_avg_rating(user_id, client_or_worker):
    profile = Profile.objects.get(user_id=int(user_id))
    if client_or_worker == 'CLIENT':
        avg_client_rating = ClientRating.objects.filter(rated_person__user_id=int(user_id)).aggregate(Avg('puntuation'))
        profile.client_rating_avg = avg_client_rating['puntuation__avg']
        profile.save()
    else:
        avg_worker_rating = WorkerRating.objects.filter(rated_person__user_id=int(user_id)).aggregate(Avg('puntuation'))
        profile.worker_rating_avg = avg_worker_rating['puntuation__avg']
        profile.save()
