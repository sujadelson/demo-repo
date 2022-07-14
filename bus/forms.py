from django import forms
from bus.models import BusModel,BusCategoryModel

class BusCategoryForm(forms.ModelForm):
	class Meta:
		model=BusCategoryModel
		exclude=('created_on',)

class BusForm(forms.ModelForm):
	class Meta:
		model=BusModel
		exclude=('status','created_on')
