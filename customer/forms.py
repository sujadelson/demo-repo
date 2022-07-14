from django import forms
from customer.models import UserRegisterModel
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
	class Meta:
		model=User
		fields=["username","first_name","last_name","password1","password2","email"]

class ExtendedUserForm(forms.ModelForm):
	class Meta:
		model=UserRegisterModel
		fields=["age","address","id_card"]