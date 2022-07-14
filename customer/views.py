from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from customer.forms import UserRegisterForm,ExtendedUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import View
from django.core.mail import send_mail
from ebus.settings import EMAIL_HOST_USER
from . import forms
from django.conf import settings
import requests
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.contrib.auth.models import User


# Create your views here.

def adduser(request):
	if request.method=="POST":
		form=UserRegisterForm(request.POST)
		extend_form=ExtendedUserForm(request.POST,request.FILES)

		if form.is_valid() and extend_form.is_valid():
			user=form.save()
			extended_profile=extend_form.save(commit=False)
			extended_profile.user=user
			extended_profile.save()

			sub = forms.UserRegisterForm(request.POST)
			name = str(sub['first_name'].value())
			subject = 'Welcome to EBus'
			message = 'Hi %s , your Registration with EBus was successful. Now you can use the credentials to login and book for your Journey ' %name
			recepient = str(sub['email'].value())
			send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently =False)

			username_var=form.cleaned_data.get('username')
			password_var=form.cleaned_data.get('password1')
			user=authenticate(username=username_var,password=password_var)

			login(request,user)
			return redirect ('chome')

	else:
		form=UserRegisterForm(request.POST)
		extend_form=ExtendedUserForm(request.POST,request.FILES)

	context={"form":form,"extend_form":extend_form}
	return render(request,'adduser.html',context)

class UserLogin(View):
	def get(self,request):
		form=AuthenticationForm()
		context={'form':form}
		return render(request,'login.html',context)

	def post(self,request):
		username=request.POST.get('username')
		password=request.POST.get('password')
		recaptcha_response = request.POST.get('g-recaptcha-response')
		data = {
			'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
			'response': recaptcha_response
			}
		r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
		result = r.json()
        
		if result['success']:
			user=authenticate(username=username,password=password)
			login(request,user,backend='django.contrib.auth.backends.ModelBackend')
        
			if user is not None :
				login(request,user)
				if user.is_superuser == True and user.is_staff == True:
					return redirect('ahome')
				if user.is_staff == True and user.is_superuser == False:
					return redirect('shome')
				if user.is_staff == False and user.is_superuser == False:
					return redirect ('chome')
			else:
				form=AuthenticationForm()
				context={'form':form}
				return render(request,'login.html',context)

def logout_view(request):
    logout(request)

    return redirect('chome')

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password_reset.html", context={"password_reset_form":password_reset_form})



