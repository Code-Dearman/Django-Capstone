from . import views
from django.urls import path


urlpatterns = [
    path('', views.ToDoListView.as_view(), name='home'),
]
