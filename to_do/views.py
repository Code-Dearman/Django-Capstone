from django.shortcuts import render
from django.views import generic
from .models import To_Do_List

# Create your views here.

class ToDoListView(generic.ListView):
    """
    Displays to do lists that are selected 'public' by user and 'approved=True' by admin. 
    Sorted by newest first.

    """
    queryset = To_Do_List.objects.filter(status=1, approved=True).order_by("-created_on")
    template_name = 'to_do/to_do_list.html'
    paginate_by = 6