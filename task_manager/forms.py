from django import forms
from .models import Status
from .models import Task
from .models import Label

class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'assignee', 'labels']
        widgets = {
            'labels': forms.CheckboxSelectMultiple,
        }

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
