from django.db import models
from django.db.models import Avg
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Profession(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    birthdate = models.DateField(null=True)
    dni = models.CharField(max_length=9, unique=True)
    city = models.TextField(max_length=30)
    description = models.TextField(default="Default description", null=True, blank=True, max_length = 1000)

    professions = models.ManyToManyField(Profession)
    picture = models.ImageField(null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    client_rating_avg = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, null=True, blank=True)
    worker_rating_avg = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, null=True, blank=True)

    def __str__(self):
        return self.user.first_name+" -- "+ self.city

    def get_client_rating_avg(self):
        avg = ClientRating.objects.filter(rated_person__user_id=self.user_id).aggregate(Avg('puntuation')).get('puntuation__avg')
        if avg:
            return avg
        else:
            return 0.0

    def get_worker_rating_avg(self):
        avg =  WorkerRating.objects.filter(rated_person__user_id=self.user_id).aggregate(Avg('puntuation')).get('puntuation__avg')
        if avg:
            return avg
        else:
            return 0.0



LABOUR_STATE_CHOICES = [
    'PENDING',
    'IN_PROCESS',
    'END_WORKER',
    'END_CLIENT',
    'FINISHED',
    'REJECTED',
    'CANCELLED',
]



class LabourRequest(models.Model):
    description = models.TextField(max_length=1000, null=True, blank=True)
    state = models.CharField(max_length=20)
    start_datetime = models.DateTimeField(null=True, blank=True)
    finish_datetime = models.DateTimeField(null=True, blank=True)

    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='creator')
    worker = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='worker')

    def __str__(self):
        return "Labour request created by "+self.creator.user.first_name



class LabourChat(models.Model):
    creation_datetime = models.DateTimeField(null=False, blank=False)
    last_message_datetime = models.DateTimeField(null=False, blank=False)

    labour = models.OneToOneField(LabourRequest, on_delete=models.CASCADE)

    def last_message(self):
        chat_message = ChatMessage.objects.filter(chat__id=self.id).order_by('-send_datetime').first()
        if chat_message:
            return str(chat_message.content)
        else:
            return ' '



class ChatMessage(models.Model):
    content = models.TextField(max_length=500)
    send_datetime = models.DateTimeField(null=False, blank=False)
    is_read = models.BooleanField(default=False)

    chat = models.ForeignKey(LabourChat, on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)



class ClientRating(models.Model):
    puntuation = models.PositiveIntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])
    description = models.TextField(max_length=300, blank=True, null= True)

    labour = models.OneToOneField(LabourRequest, on_delete=models.CASCADE)

    rater_person = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='rater')
    rated_person = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='rated')

    def __str__(self):
        return self.rater_person.user.first_name+" -> "+ self.rated_person.user.first_name+" -- " +str(self.puntuation)





class WorkerRating(models.Model):
    puntuation = models.PositiveIntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])
    description = models.TextField(max_length=300, blank=True, null= True)

    labour = models.OneToOneField(LabourRequest, on_delete=models.CASCADE)

    rater_person = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='workerRater')
    rated_person = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='workerRated')

    def __str__(self):
        return self.rater_person.user.first_name+" -> "+ self.rated_person.user.first_name+" -- " +str(self.puntuation)

