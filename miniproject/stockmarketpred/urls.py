from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("signin/", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
    path("signout/", views.signout, name="signout"),
    path("home/", views.home, name="home"),
    path("predictions/", views.predictions, name="predictions"),
    path("sentiment/", views.sentiment, name="sentiment"),
    path("contact/", views.contact, name="contact"),
    path("", views.index, name="index")
]
