from django import forms
from booking.models import BusBookingModel


class ReservationForm(forms.ModelForm):

	class Meta:
		model=BusBookingModel
		fields= ('no_of_seat',)