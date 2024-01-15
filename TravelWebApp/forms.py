from django.forms import ModelForm
from .models import Travel
from django import forms
from .models import Task

class TravelForm(ModelForm):
    class Meta:
        model = Travel
        fields = ['city', 'country', 'start_date', 'end_date', 'number_of_people', 'type_of_transport', 'description']




class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']