from django import forms
from django.contrib.auth import get_user_model
from .models import Profile, CustomUser

from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class  LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)




class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email", "first_name", "last_name", "department")


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birthday', 'photo']
