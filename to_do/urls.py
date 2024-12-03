from django.urls import path
from . import views



urlpatterns = [
    path('', views.ToDoListView.as_view(), name='home'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('list/new/', views.edit_list, name='create_list'),
    path('edit/<slug:slug>/', views.edit_list, name='edit_list'),
]
