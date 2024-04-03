from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.get_users, name='users'),
    path('users/<int:user_id>/', views.user_details, name='user_details'),

]