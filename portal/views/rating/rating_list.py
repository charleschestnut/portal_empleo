from django.shortcuts import render

from portal.models import WorkerRating, ClientRating, Profile


def rating_list(request, type, id):
    context = {}
    profile = Profile.objects.get(user_id=int(id))
    if type == "worker_to_me":
        rating_list = WorkerRating.objects.filter(rated_person__user_id=profile.user.id)
    elif type == "client_to_me":
        rating_list = ClientRating.objects.filter(rated_person__user_id=profile.user.id)
    else:
        rating_list = ClientRating.objects.none()

    context['rating_list'] = rating_list

    return render(request, 'rating_list.html', context)
