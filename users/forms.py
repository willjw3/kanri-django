from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']


class LoginDemoForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginDemoForm, self).__init__(*args, **kwargs)


    username = forms.CharField(widget=forms.HiddenInput(), initial="kanri_demo")
    password = forms.CharField(widget=forms.HiddenInput(), initial="testuser987")

