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

    
@login_required
def edit_list(request, slug=None):
    """
    Dispalys and editable form for the user, accepting a post request if the form has a slug.
    If no slug, creates a new to-do list.
    """
    if slug:
        todo_list = get_object_or_404(To_Do_List, slug=slug, author=request.user)
        form = ToDoListForm(request.POST or None, instance=todo_list)
        template_name = 'to_do/edit_list.html'

    else:
        form = ToDoListForm(request.POST or None)
        template_name = 'to_do/new_list.html'

    if form.is_valid():
        to_do_list = form.save(commit=False)
        to_do_list.author = request.user
        to_do_list.save()
        return redirect('profile')

    return render(request, template_name, {'form': form})


@login_required
def delete_list(request, slug):
    """
    View to delete lists.
    """
    to_do_list = get_object_or_404(To_Do_List, slug=slug, author=request.user)

    if request.method == "POST":
        to_do_list.delete()
        return redirect('profile')

    return redirect('profile')

