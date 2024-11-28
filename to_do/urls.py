from django.urls import path
from . import views



urlpatterns = [
    path('', views.ToDoListView.as_view(), name='home'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('edit/<int:list_id>/', views.edit_list, name='edit_list'),
]
