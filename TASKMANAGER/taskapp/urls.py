from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'), # Include your app's URLs
    path('login_form', views.login_form, name='login_form'), # Include your app's URLs
    path('register_form', views.register_form, name='register_form'), # Include your app's URLs
    path('logout_page', views.logout_page, name='logout_page'),
    path('task/<int:pk>', views.task, name='task'),
    path('add_task/<int:room_id>/<str:task_type>', views.add_task, name='add_task'),
    path('edit_task/<int:task_id>/<str:task_type>/', views.edit_task, name='edit_task'),
    path('delete_task/<int:task_id>/<str:task_type>/', views.delete_task, name='delete_task'),
    path('create_room/', views.create_room, name='create_room'),
    path('share_room/<int:room_id>/', views.share_room, name='share_room'),
    path('send_number/', views.send_number, name='send_number'),
]