
from django import forms
from .models import Profile
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class  LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)




class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email", "first_name", "last_name", "department")




User = get_user_model()

class ProfileForm(forms.ModelForm):
    department_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'textarea textarea-bordered', 'rows': 3})
    )
    position_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'textarea textarea-bordered', 'rows': 3})
    )

    class Meta:
        model = Profile
        fields = ['photo', 'date_of_birthday', 'number']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from the view
        super().__init__(*args, **kwargs)

        if user:
            self.fields['department_description'].initial = user.department.description
            self.fields['position_description'].initial = user.position.description

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user

        # Save department & position descriptions
        user.department.description = self.cleaned_data['department_description']
        user.position.description = self.cleaned_data['position_description']
        user.department.save()
        user.position.save()

        if commit:
            profile.save()

        return profile


