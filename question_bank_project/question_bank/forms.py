from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['qus', 'subject']


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['text','is_correct']



class Signup(UserCreationForm):
    class Meta:
        model=User
        fields=['username','first_name','email']
        labels={'email':'Email'}