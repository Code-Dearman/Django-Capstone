from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import ToDoListForm
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
    

def edit_list(request, list_id):
    """
    Dispalys and editable form for the user, accepting a post request.
    """
    to_do_list = get_object_or_404(To_Do_List, id=list_id, author=request.user)
    if request.method == "POST":
        form = ToDoListForm(request.POST, instance=to_do_list)
        if form.is_valid():
            form.save()
            return redirect('profile')
    
    else:
        form = ToDoListForm(instance=to_do_list)
    return render(request, 'to_do/edit_list.html', {'form': form})


