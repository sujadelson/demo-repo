from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserRegisterModel(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	age=models.IntegerField(default=18)
	address=models.TextField(max_length=80)
	id_card=models.ImageField(upload_to="idcard/")
	type=models.CharField(max_length=50)
	status=models.BooleanField(default=True)
	created_on=models.DateTimeField(auto_now=True)

	def __str__(self):
		return (self.user.first_name+" "+self.user.last_name)
