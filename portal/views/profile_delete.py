from django.shortcuts import render
from portal.models import ClientRating, WorkerRating
from . import update_avg_rating

def delete_profile(request):
    def all_rated_by_clients_ratings(user_id):
        c_ratings = ClientRating.objects.filter(rater_person__user_id=int(user_id)).only('rated_person__user_id')
        return c_ratings

    def all_rated_by_worker_ratings(user_id):
        w_ratings = WorkerRating.objects.filter(rater_person__user_id=int(user_id)).only('rated_person__user_id')
        return w_ratings

    user_to_delete = request.user
    users_cr = all_rated_by_clients_ratings(user_to_delete.id)
    users_wr = all_rated_by_worker_ratings(user_to_delete.id)

    for new_avg_user in users_cr:
        update_avg_rating(new_avg_user, 'CLIENT', user_to_delete.id)

    for new_avg_user in users_wr:
        update_avg_rating(new_avg_user, 'WORKER', user_to_delete.id)


    user_to_delete.delete()

    return render()