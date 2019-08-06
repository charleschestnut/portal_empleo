import os


users_list = [
    #username, email, password, first_name, last_name
    ['daniel', 'daniel@gmail.com', 'password_d', 'Daniel', 'Castaño del Castillo'],
    ['elvira', 'elvira@gmail.com', 'password_e', 'Elvira', 'del Castillo González'],
    ['alejandro', 'alejandro@gmail.com', 'password_a', 'Alejandro', 'Castaño del Castillo'],
    ['dionisio', 'dionisio@gmail.com', 'password_d', 'Dionisio', 'Castaño Aguado'],
    ['mariam', 'mariam@gmail.com', 'password_m', 'Saadi', 'Crespo'],
    ['juanmarco', 'juanmarco@gmail.com', 'password_jm', 'Juan Marco', 'Domínguez'],
]

professions_list = ['Electridad', 'Jardinería', 'Carpinteria', 'Fontenería', 'Hostelería', 'Albañilería'],

profiles_list = [
    #birthdate, dni, city, description, professions, sin-imágenes, user
    ['1984-07-04', '00000001A', 'Utretch', "Daniel's description", ['Jardinería', 'Electricidad'], 'daniel'],
    ['1966-01-27', '00000002B', 'Huelva', "Elvira's description", ['Carpintería', 'Electricidad'], 'elvira'],
    ['1984-07-04', '00000003C', 'Sevilla', "Alejandro's description", ['Hostelería', 'Electricidad'], 'alejandro'],
    ['1984-07-04', '00000004D', 'Huelva', "Dionisio's description", ['Jardinería', 'Albañilería'], 'dionisio'],
    ['1984-07-04', '00000005E', 'Dos Hermanas', "Mariam's description", ['Electricidad', 'Albañilería'], 'mariam'],
    ['1984-07-04', '00000006F', 'Huelva', "Juan Marco's description", ['Hostelería'], 'juanmarco'],
]

labourRequests_list = [
    #description, state, start_datetime, finish_datetime, creator, worker
    []
]

labourChat_list = [
    #creation_datetime, last_message_datetime, labour
    []
]

chatMessage_list = [
    #
    []
]

clientRating_list = [
    #
    []
]

workerRating_list = [
    #
    []
]

def populate():

    print("----------------------------")
    print("STATING POPULATION DATA BASE")
    print("----------------------------")

    for user_fields in users_list:
        user = User.objects.create_user(username=user_fields[0],
                                        email=user_fields[1],
                                        password=user_fields[2],
                                        first_name=user_fields[3],
                                        last_name=user_fields[4])

        user.save()
        print("User saved")

    print("----------------------------")

    for prof in professions_list:
        profession = Profession.objects.create(name=prof)
        profession.save()
        print("Profession saved")

    print("----------------------------")

    for p_fields in profiles_list:
        user_profile = User.objects.get(username=p_fields[5])
        professions = []
        for p in p_fields[4]:
            professions.append(Profession.objects.get(name=p))

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

        profile.save()
        profile.professions.add(professions)
        profile.save()

    print("----------------------------")
    print("POPULATION DATA BASE FINISHED")
    print("----------------------------")


if __name__ == '__main__':
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'Project.settings')
    #django.setup()
    from models import *
    from django.contrib.auth.models import User


    populate()  # Call the populate function, which calls the
                # add_genre and add_musician functions