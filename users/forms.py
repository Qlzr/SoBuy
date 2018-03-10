from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

class RegisterForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model = User
		fields = ("username", "email")

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ["nickname", "email", "first_name", "last_name"]