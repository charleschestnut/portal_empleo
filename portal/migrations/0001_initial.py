# Generated by Django 2.2.3 on 2019-07-15 07:54

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LabourRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('state', models.CharField(max_length=20)),
                ('start_datetime', models.DateTimeField(blank=True, null=True)),
                ('finish_datetime', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthdate', models.DateField(null=True)),
                ('dni', models.CharField(max_length=9)),
                ('city', models.TextField(max_length=30)),
                ('description', models.TextField(blank=True, default='Default description', max_length=1000, null=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='')),
                ('client_rating_avg', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=4, null=True)),
                ('worker_rating_avg', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=4, null=True)),
                ('professions', models.ManyToManyField(to='portal.Profession')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WorkerRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntuation', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('labour', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='portal.LabourRequest')),
                ('rated_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workerRated', to='portal.Profile')),
                ('rater_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workerRater', to='portal.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='labourrequest',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to='portal.Profile'),
        ),
        migrations.AddField(
            model_name='labourrequest',
            name='worker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='worker', to='portal.Profile'),
        ),
        migrations.CreateModel(
            name='ClientRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntuation', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('labour', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='portal.LabourRequest')),
                ('rated_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rated', to='portal.Profile')),
                ('rater_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rater', to='portal.Profile')),
            ],
        ),
    ]
