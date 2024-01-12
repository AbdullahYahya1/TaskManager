from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'), # Include your app's URLs
    path('login_form', views.login_form, name='login_form'), # Include your app's URLs
    path('register_form', views.register_form, name='register_form'), # Include your app's URLs
    path('logout_page', views.logout_page, name='logout_page'),
    path('task/<str:pk>', views.task, name='task'),
    path('send_number/', views.send_number, name='send_number'),
]
