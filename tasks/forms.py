from django import forms
from .models import Task, Subject

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'subject', 'task_type', 'priority', 'due_date', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Research Paper on Web Security'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Add notes, requirements, or reminders...', 'rows': 4}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'task_type': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Computer Science'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. CS101'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
        }