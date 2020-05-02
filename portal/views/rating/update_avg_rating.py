from portal.models import Profile


def update_avg_rating(user_id, client_or_worker):
    profile = Profile.objects.get(user_id=int(user_id))
    if client_or_worker == 'CLIENT':
        average = profile.get_client_rating_avg()
        print(average)
        if average is None:
            profile.client_rating_avg = 0.0
        else:
            profile.client_rating_avg = average
        profile.save()

    else:
        average = profile.get_worker_rating_avg()
        print(average)
        if average is None:
            profile.worker_rating_avg = 0.0
        else:
            profile.worker_rating_avg = average
        profile.save()
