from django.shortcuts import render
from portal.models import *

def search_list(request):

    profession_choices = Profession.objects.all()
    context = {'profession_choices': profession_choices}
    profession_selected = request.GET.get('profession', '')
    city_selected = request.GET.get('city', '')
    rating_order = request.GET.get('rating_order', '')
    min_puntuation = request.GET.get('min_puntuation','')
    workers_list = None;
    print("Puntuation: " + min_puntuation)

    if profession_selected:
        workers_list = Profile.objects.filter(professions__pk=profession_selected)

    if city_selected:
        if workers_list is None:
            workers_list = Profile.objects.filter(city__search=city_selected)
        else:
            workers_list = workers_list.filter(city__search=city_selected)\

    if min_puntuation:
        if workers_list is None:
            workers_list = Profile.objects.filter(worker_rating_avg__gte=min_puntuation)
            print(workers_list)
        else:
            workers_list= workers_list.filter(worker_rating_avg__gte=min_puntuation)


    if rating_order:
        if workers_list is None:
            workers_list = Profile.objects.order_by('-rating_avg')
        else:
            workers_list = workers_list.order_by('-rating_avg')

    context['workers_list'] = workers_list




    return render(request, 'search_list.html', context)