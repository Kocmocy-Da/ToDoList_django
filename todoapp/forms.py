from django.forms import ModelForm
from .models import ToDoList


class TodoForm(ModelForm):
    class Meta:
        model = ToDoList
        fields = ['title', 'memo', 'important']
