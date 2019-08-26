from portal.models import Profile, ClientRating, WorkerRating
from django.db.models import Avg


def update_avg_rating(user_id, client_or_worker, excluded_user_id):
    profile = Profile.objects.get(user_id=int(user_id))
    print(excluded_user_id)
    if client_or_worker == 'CLIENT':

        avg_client_rating = ClientRating.objects.filter(rated_person__user_id=int(user_id))
        if excluded_user_id:
            avg_client_rating = avg_client_rating.exclude(rater_person__user_id=int(excluded_user_id))
        avg_client_rating.aggregate(Avg('puntuation'))
        if avg_client_rating['puntuation__avg'] is None:
            profile.client_rating_avg = 0.0
        else:
            profile.client_rating_avg = avg_client_rating['puntuation__avg']
        profile.save()

    else:

        avg_worker_rating = WorkerRating.objects.filter(rated_person__user_id=int(user_id))
        if excluded_user_id:
            avg_worker_rating = avg_worker_rating.exclude(rater_person__user_id=int(excluded_user_id))
        avg_worker_rating =  avg_worker_rating.aggregate(Avg('puntuation'))

        if avg_worker_rating['puntuation__avg'] is None:
            profile.worker_rating_avg = 0.0
        else:
            profile.worker_rating_avg = avg_worker_rating['puntuation__avg']
        profile.save()

