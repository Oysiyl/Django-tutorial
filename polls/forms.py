from django import forms
from django.contrib.auth.forms import UserCreationForm


class QuestionForm(forms.Form):
    question_text = forms.CharField(max_length=100)
    choice_text_1 = forms.CharField(max_length=100)
    choice_text_2 = forms.CharField(max_length=100)
    choice_text_3 = forms.CharField(max_length=100)
