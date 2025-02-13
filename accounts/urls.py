from django.urls import path
from . import views

# URLS 
urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),  
    path('register/', views.register, name='register'),
]