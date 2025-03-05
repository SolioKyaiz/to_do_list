from django import forms
from .models import Task

class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'priority', 'deadline', 'status','description']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CreateTaskForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['status'].initial = 'todo'  # Default status for new tasks