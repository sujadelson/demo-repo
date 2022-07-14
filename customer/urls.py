from django.urls import path
from . import views
from customer.views import UserLogin

urlpatterns = [
    path('register/', views.adduser, name='reg'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("password_reset/", views.password_reset_request, name="password_reset")
    ]