from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User

class RegisterForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model = User
		fields = ("username", "email")

class UserForm(UserChangeForm):
	class Meta(UserChangeForm.Meta):
		model = User
		fields = ('username', 'nickname', 'email', 'last_login', 'date_joined')