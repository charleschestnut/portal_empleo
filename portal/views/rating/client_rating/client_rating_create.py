from django.shortcuts import render, redirect
from portal.models import *
from portal.forms import RatingForm
from django.db.models import Q
from portal.views import update_avg_rating as update
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
            puntuation = rating_form.cleaned_data['puntuation']
            rater = Profile.objects.get(user_id=request.user.id)
            rated = labour.creator

            rating = ClientRating(
                puntuation=puntuation,
                description=description,
                labour=labour,
                rater_person=rater,
                rated_person=rated,
            )
            rating.save()
            # TODO: ACTUALIZAMOS LA VALORACIÓN MEDIA DEL RATED
            update.update_avg_rating(rated, 'CLIENT')

            my_ratings_filter = Q(rater_person__id=request.user.id) | Q(rated_person__id=request.user.id)
            my_client_ratings = ClientRating.objects.filter(my_ratings_filter)
            context['rating_list'] = my_client_ratings

            return redirect('rating_list.html')
    else:
        rating_form = RatingForm()
        rated = labour.creator
        context = {'form': rating_form, 'rated': rated, 'labour_id': labour.id}

    return render(request, 'client_rating_create.html', context)
