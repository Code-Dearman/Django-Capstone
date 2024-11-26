from django.shortcuts import render
from django.views import generic
from .models import To_Do_List

# Create your views here.

class ToDoListView(generic.ListView):
    """
    Displays to do lists
    """
    queryset = To_Do_List.objects.all()
    template_name = 'to_do/to_do_list.html'