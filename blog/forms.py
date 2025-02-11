from django import forms
from .models import Comment


class EmailTD_form(forms.Form):

    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['description']

