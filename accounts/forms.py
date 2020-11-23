from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import forms
from django.forms import ModelForm


class RegisterForm(UserCreationForm):
	class Meta:
		model=User
		fields=['username','email','password1','password2']