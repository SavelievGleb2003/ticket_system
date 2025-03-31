from django import forms
from .models import Ticket, Position

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'department', 'position', 'attachment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Вызов __init__ родительского класса
        self.fields['title'].required = True
        self.fields['department'].required = True
        self.fields['position'].required = True




class TicketRedirectForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'attachment', 'department', 'position']

    def __init__(self, *args, **kwargs):
        super(TicketRedirectForm, self).__init__(*args, **kwargs)
        # Запрещаем изменение title, description, attachment
        self.fields['title'].disabled = True
        self.fields['description'].disabled = True
        self.fields['attachment'].disabled = True

        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['position'].queryset = Position.objects.filter(department_id=department_id)
            except (ValueError, TypeError):
                self.fields['position'].queryset = Position.objects.none()
        elif self.instance.pk:
            self.fields['position'].queryset = self.instance.department.positions.all()


class TicketCloneForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'attachment', 'department', 'position']

    def __init__(self, *args, **kwargs):
        super(TicketCloneForm, self).__init__(*args, **kwargs)
        # Запрещаем изменение title, description, attachment
        self.fields['title'].disabled = True
        self.fields['description'].disabled = True
        self.fields['attachment'].disabled = True

        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['position'].queryset = Position.objects.filter(department_id=department_id)
                self.instance.id = None  # Сбрасываем ID при изменении отдела
            except (ValueError, TypeError):
                self.fields['position'].queryset = Position.objects.none()
        elif self.instance.pk:
            self.fields['position'].queryset = self.instance.department.positions.all()