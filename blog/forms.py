from django import forms
from .models import Comment, Folder


class EmailTD_form(forms.Form):

    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['description']


class FolderForm(forms.ModelForm):
    parent_path = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"readonly": "readonly"})
    )

    class Meta:
        model = Folder
        fields = ["name", "parent"]

    def __init__(self, *args, **kwargs):
        parent_folder = kwargs.pop("parent_folder", None)  # Get parent folder if passed
        super().__init__(*args, **kwargs)

        # If a parent folder is provided, set it in the form
        if parent_folder:
            self.fields["parent"].initial = parent_folder
            self.fields["parent_path"].initial = parent_folder.get_full_path()

        # Make parent hidden so it doesn't show as a dropdown
        self.fields["parent"].widget = forms.HiddenInput()




