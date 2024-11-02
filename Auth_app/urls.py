# Authentication/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup", views.signup, name="Signup"),
    path("signin", views.signin, name="SignIn"),
    path("signout", views.signout, name="SignOut"),
    path("confirm_email/<str:token>/", views.confirm_email, name="ConfirmEmail"),
]
