from django import forms 
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    Username = forms.CharField()   #take a look on ()section
    password = forms.CharField(widget=forms.PasswordInput)

#signup:
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields =('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data      #------tal-------
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password don\'t match.')
        return cd['password2']