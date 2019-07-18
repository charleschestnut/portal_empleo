from django import forms
from .models import *
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['dni', 'birthdate', 'city', 'description', 'professions', 'picture']


class Searchform(forms.Form):
    city = forms.CharField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class LabourRequestForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea, max_length=1000)


class RatingForm(forms.Form):
    puntuation = forms.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])
    description = forms.CharField(widget=forms.Textarea, max_length=1000)