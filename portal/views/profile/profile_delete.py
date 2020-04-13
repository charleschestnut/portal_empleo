from django.shortcuts import redirect
from portal.models import ClientRating, WorkerRating
from portal.views.rating import update_avg_rating as update
from django.contrib.auth.decorators import login_required


@login_required
def profile_delete(request):
    def all_rated_by_clients_ratings(user_id):
        c_ratings = ClientRating.objects.filter(rater_person__user_id=int(user_id)).values_list('rated_person__user_id',
                                                                                                flat=True)
        return c_ratings

    def all_rated_by_worker_ratings(user_id):
        w_ratings = WorkerRating.objects.filter(rater_person__user_id=int(user_id)).values_list('rated_person__user_id',
                                                                                                flat=True)
        return w_ratings

    user_to_delete = request.user
    users_cr = all_rated_by_clients_ratings(user_to_delete.id)
    users_wr = all_rated_by_worker_ratings(user_to_delete.id)

    for new_avg_user in users_cr:
        update.update_avg_rating(new_avg_user, 'CLIENT')

    for new_avg_user1 in users_wr:
        update.update_avg_rating(new_avg_user1, 'WORKER')

    user_to_delete.delete()

    return redirect('search_list')