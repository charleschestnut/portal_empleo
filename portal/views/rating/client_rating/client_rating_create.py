from django.shortcuts import render
from portal.models import *
from portal.forms import RatingForm
from django.db.models import Q
from portal.views.rating import update_avg_rating as update
from django.contrib.auth.decorators import login_required


@login_required
def client_rating_create(request, id):
    labour = LabourRequest.objects.get(id=int(id))

    if request.method == 'POST':
        rating_form = RatingForm(request.POST)
        context = {}
        if rating_form.is_valid():
            labour = LabourRequest.objects.get(id=int(id))
            description = rating_form.cleaned_data['description']
            punctuation = rating_form.cleaned_data['punctuation']
            rater = Profile.objects.get(user_id=request.user.id)
            rated = labour.creator

            rating = ClientRating(
                punctuation=punctuation,
                description=description,
                labour=labour,
                rater_person=rater,
                rated_person=rated,
            )
            rating.save()
            # TODO: ACTUALIZAMOS LA VALORACIÓN MEDIA DEL RATED
            update.update_avg_rating(rated.user_id, 'CLIENT')

            my_ratings_filter = Q(rater_person__id=request.user.id) | Q(rated_person__id=request.user.id)
            my_client_ratings = ClientRating.objects.filter(my_ratings_filter)
            context['rating_list'] = my_client_ratings

            return render(request, 'rating_list.html', context)
    else:
        rating_form = RatingForm()
        rated = labour.creator
        context = {'form': rating_form, 'rated': rated, 'labour_id': labour.id}

    return render(request, 'client_rating_create.html', context)
