from django import forms 
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    Username = forms.CharField()   #take a look on ()section
    password = forms.CharField(widget=forms.PasswordInput)