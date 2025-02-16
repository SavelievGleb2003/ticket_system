from django import forms
from .models import Ticket, Position

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description','screenshot' , 'department', 'position', 'due_date']

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['position'].queryset = Position.objects.filter(department_id=department_id)
            except (ValueError, TypeError):
                self.fields['position'].queryset = Position.objects.none()
        elif self.instance.pk:
            self.fields['position'].queryset = self.instance.department.positions.all()
