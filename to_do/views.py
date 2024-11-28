from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
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


class ProfileView(LoginRequiredMixin, generic.ListView):
    """
    Displays all personal to do lists created by a user.
    """
    model = To_Do_List
    template_name = 'to_do/profile.html'
    context_object_name = 'user_lists'

    def get_queryset(self):
        """
        Returns only lists which match the current logged in user.
        """
        return To_Do_List.objects.filter(author=self.request.user)
    

