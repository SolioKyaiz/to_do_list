from django import forms
from .models import Task

class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'priority', 'deadline', 'status', 'description']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'priority': forms.Select(),
            'status': forms.Select(),
        }
        labels = {
            'title': 'Название',
            'priority': 'Приоритет',
            'deadline': 'Дедлайн',
            'status': 'Статус',
            'description': 'Описание',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CreateTaskForm, self).__init__(*args, **kwargs)
        if user:
            if not self.instance.pk:  # Only set initial for new tasks, not edits
                self.fields['status'].initial = 'todo'
        if self.instance and self.instance.deadline:
            self.fields['deadline'].initial = self.instance.deadline.strftime('%Y-%m-%d')