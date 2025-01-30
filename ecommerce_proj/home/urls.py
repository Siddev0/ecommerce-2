from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/',views.loginUser, name='login'),
    path('register/',views.register, name='register'),
    path('otp/', views.otp_verification, name='otp_verification'),
    path('logout/', views.logoutUser, name='logout')
]
