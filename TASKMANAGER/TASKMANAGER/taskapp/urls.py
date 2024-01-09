from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'), # Include your app's URLs
    path('login_register_form', views.login_register_form, name='login_register_form'), # Include your app's URLs
    
]
