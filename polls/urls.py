from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.get_users, name='users'),
    path('todo/', views.todo_page, name='todo'),
    path('users/<int:user_id>/', views.user_details, name='user_details'),

]