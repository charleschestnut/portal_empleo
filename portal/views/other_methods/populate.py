from portal.models import *
from django.contrib.auth.models import User
from django.shortcuts import render
from datetime import date, timedelta
from django.core.files import File

users_list = [
    #username, email, password, first_name, last_name
    ['daniel', 'daniel@gmail.com', 'password_d', 'Daniel', 'Castaño del Castillo'],
    ['elvira', 'elvira@gmail.com', 'password_e', 'Elvira', 'del Castillo González'],
    ['alejandro', 'alejandro@gmail.com', 'password_a', 'Alejandro', 'Castaño del Castillo'],
    ['dionisio', 'dionisio@gmail.com', 'password_d', 'Dionisio', 'Castaño Aguado'],
    ['deku', 'deku@gmail.com', 'password_d', 'Deku', 'Castaño Del Castillo'],
    ['juanmarco', 'juanmarco@gmail.com', 'password_jm', 'Juan Marco', 'Domínguez'],
]

professions_list = ['Electricidad', 'Jardinería', 'Carpintería', 'Fontenería', 'Hostelería', 'Albañilería']

profiles_list = [
    #birthdate, dni, city, description, professions, sin-imágenes, user
    ['1984-07-04', '00000001A', 'Utretch', "Daniel's description", ['Jardinería', 'Electricidad'], 'daniel', './static/media/population/profile_photo_1.jpg'],
    ['1966-01-27', '00000002B', 'Huelva', "Elvira's description", ['Carpintería', 'Electricidad'], 'elvira', './static/media/population/profile_photo_2.jpg'],
    ['1984-07-04', '00000003C', 'Sevilla', "Alejandro's description", ['Hostelería', 'Electricidad'], 'alejandro', './static/media/population/profile_photo_3.jpg'],
    ['1984-07-04', '00000004D', 'Huelva', "Dionisio's description", ['Jardinería', 'Albañilería'], 'dionisio', './static/media/population/profile_photo_4.jpg'],
    ['1984-07-04', '00000005E', 'Con Migo', "Deku's description", ['Electricidad', 'Albañilería'], 'deku', './static/media/population/profile_photo_5.jpg'],
    ['1984-07-04', '00000006F', 'Huelva', "Juan Marco's description", ['Hostelería'], 'juanmarco', './static/media/population/profile_photo_6.jpg'],
]


labourRequests_list = [
    #description, state, start_datetime, finish_datetime, creator, worker, price
    ['Ayúdame en esta tarea, por favor.', 'PENDING', None, None, 'daniel', 'alejandro', 100],
    ['Córtame jamón, por favor.', 'REJECTED', None, None, 'deku', 'dionisio', 10],
    ['Arréglame el ordenador, por favor.', 'FINISHED', 'yesterday', 'two days ago', 'elvira', 'alejandro', 0],
    ['Hazme un plan de ejercicio de piernas, por favor.', 'IN_PROCESS', 'yesterday', None, 'juanmarco', 'daniel', 15],
    ['Hazme una maqueta de aviones.', 'PAID_OUT', 'yesterday', None, 'juanmarco', 'daniel', 10]
]

labourChat_list = [
    #creation_datetime, last_message_datetime, labour
    ['two days ago', 'two days ago', 'Ayúdame en esta tarea, por favor.'],
    ['two days ago', 'two days ago', 'Córtame jamón, por favor.'],
    ['two days ago', 'two days ago', 'Arréglame el ordenador, por favor.'],
    ['two days ago', 'two days ago', 'Hazme un plan de ejercicio de piernas, por favor.'],
    ['two days ago', 'two days ago', 'Hazme una maqueta de aviones.']

]

chatMessage_list = [
    #Content, send_datetime, chat, owner
    []
]

clientRating_list = [
    #punctuation, description, labour, rater_person, rated_person
    []
]

workerRating_list = [
    #punctuation, description, labour, rater_person, rated_person
    []
]


def populate(request):
    def load_users():
        for user_fields in users_list:
            user = User.objects.create_user(username=user_fields[0],
                                            email=user_fields[1],
                                            password=user_fields[2],
                                            first_name=user_fields[3],
                                            last_name=user_fields[4]
            )
            user.save()


    def load_proffesions():
        for prof in professions_list:
            profession = Profession.objects.create(name=prof)
            profession.save()


    def load_profiles():
        for p_fields in profiles_list:
            user_profile = User.objects.get(username=p_fields[5])
            profile = Profile.objects.create(
                birthdate=p_fields[0],
                dni=p_fields[1],
                city=p_fields[2],
                description=p_fields[3],
                picture=None,
                user=user_profile,
                client_rating_avg=0.0,
                worker_rating_avg=0.0
            )
            pic = File(open(p_fields[6], "rb"))
            profile.picture.save(profile.user.first_name+" "+profile.user.last_name, pic, save=True)

            for p in p_fields[4]:
                profile.professions.add(Profession.objects.get(name=p))
            profile.save()

    def personal_datetime(str):
        if str is None:
            return None
        elif str == 'two days ago':
            return date.today()-timedelta(days=2)
        else:
            return date.today()-timedelta(days=1)

    def load_labourRequests():
        for lr_fields in labourRequests_list:
            creator_user = User.objects.get(username=lr_fields[4])
            worker_user = User.objects.get(username=lr_fields[5])
            creator = Profile.objects.get(user_id=creator_user.id)
            worker = Profile.objects.get(user_id=worker_user.id)
            labourRequest = LabourRequest.objects.create(
                description=lr_fields[0],
                state=lr_fields[1],
                start_datetime=personal_datetime(lr_fields[2]),
                finish_datetime=personal_datetime(lr_fields[3]),
                price=lr_fields[6],
                creator=creator,
                worker=worker
            )
            labourRequest.save()


    def load_labourChats():
        for lc_fields in labourChat_list:
            labour = LabourRequest.objects.get(description=lc_fields[2])
            lab_chat = LabourChat.objects.create(
                creation_datetime=personal_datetime(lc_fields[0]),
                last_message_datetime=personal_datetime(lc_fields[1]),
                labour=labour
            )
            lab_chat.save()

    def create_superuser():
        user = User.objects.create_user('carlos', password='carlos')
        user.is_superuser = True
        user.is_staff = True
        user.save()

    User.objects.all().delete()
    Profession.objects.all().delete()
    Administrator.objects.all().delete()
    Banning.objects.all().delete()
    Profile.objects.all().delete()
    LabourRequest.objects.all().delete()
    LabourChat.objects.all().delete()
    ChatMessage.objects.all().delete()
    ClientRating.objects.all().delete()
    WorkerRating.objects.all().delete()

    load_proffesions()
    load_users()
    load_profiles()

    load_labourRequests()
    load_labourChats()
    create_superuser()

    return render(request, 'populate.html')