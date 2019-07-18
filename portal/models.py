from django.db import models
from django.db.models import Avg
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
# Create your models here.


class Profession(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Profile(models.Model):
    birthdate = models.DateField(null=True)
    dni = models.CharField(max_length=9)
    city = models.TextField(max_length=30)
    professions = models.ManyToManyField(Profession)
    description = models.TextField(default="Default description", null=True, blank=True, max_length = 1000)
    picture = models.ImageField(null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    client_rating_avg = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, null=True, blank=True)
    worker_rating_avg = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, null=True, blank=True)

    def __str__(self):
        return self.user.first_name+" -- "+ self.city

    def get_client_rating_avg(self):
        return  ClientRating.objects.filter(rated__id=self.user_id).aggregate(Avg('puntuation')).get('puntuation__avg')

    def get_worker_rating_avg(self):
        return  WorkerRating.objects.filter(rated__id=self.user_id).aggregate(Avg('puntuation')).get('puntuation__avg')



LABOUR_STATE_CHOICES = [
    'PENDING',
    'IN_PROCESS',
    'END_WORKER',
    'FINISHED',
    'REJECTED',
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
