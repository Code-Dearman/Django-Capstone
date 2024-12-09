from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ToDoListForm, CharacterForm
from .models import To_Do_List, UserCharacter
from .character_script import get_character_data

# Create your views here.

class ToDoListView(generic.ListView):
    """
    Displays to do lists that are selected 'public' by user and 'approved=True' by admin. 
    Sorted by newest first.

    """
    queryset = To_Do_List.objects.filter(status=1, approved=True).order_by("-created_on")
    template_name = 'to_do/to_do_list.html'
    paginate_by = 6


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    """
    Displays all personal to do lists created by a user.
    """
    # model = To_Do_List
    template_name = 'to_do/profile.html'
    # context_object_name = 'user_lists'

    # def get_queryset(self):
    #     """
    #     Returns only lists which match the current logged in user.
    #     """
    #     return To_Do_List.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_character = UserCharacter.objects.filter(user=self.request.user).first()
        form = CharacterForm()

        # If the character doesn't exist, we include the form
        if not user_character:
            context['form'] = form
        else:
            context['user_character'] = user_character

        # Get to-do lists for the logged-in user
        context['user_lists'] = To_Do_List.objects.filter(author=self.request.user)

        return context

    def post(self, request, *args, **kwargs):
        form = CharacterForm(request.POST)

        if form.is_valid():
            character_name = form.cleaned_data['character_name']
            success = get_character_data(request.user, character_name)
            if success:
                return redirect('profile')
            else:
                form.add_error(None, f"Unable to find {character_name}, please try again.")

        # If form isn't valid, just re-render with the errors
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


    
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
        action = "updated"

    else:
        form = ToDoListForm(request.POST or None)
        template_name = 'to_do/new_list.html'
        action = "created"

    if form.is_valid():
        to_do_list = form.save(commit=False)
        to_do_list.author = request.user
        to_do_list.save()

        if action == 'created':
            messages.success(request, f"Well done {request.user}, you just {action} a new list! <br> If you have marked it as public it must be approved by an admin before it will be visable on the home page")
        else:
            messages.success(request, f"Well done {request.user}, you just {action} an existing list!")

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
        messages.success(request, f"There it goes! Well done {request.user} you deleted a list!")
        return redirect('profile')

    return redirect('profile')


# @login_required
# def character_view(request):
#     user_character = UserCharacter.objects.filter(user=request.user).first()

#     if request.method == ('POST'):
#         form = CharacterForm(request.POST)
#         if form.is_valid():

#             # Use the fetch API function here
            
#             character_name = form.cleaned_data['character_name']
#             success = get_character_data(request.user, character_name)
#             if success:
#                 return redirect('profile')
#             else:
#                 form.add_error(None, f"Unable to find {character_name}, please try again.")
#     else:
#         form = CharacterForm()

#     context = {
#         'user_character': user_character,
#         'form': form,
#     }

#     return render(request, 'to_do/partials/character_section.html', context)

