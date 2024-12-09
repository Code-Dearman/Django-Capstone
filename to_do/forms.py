from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import To_Do_List, UserCharacter


class ToDoListForm(forms.ModelForm):
    class Meta:
        model = To_Do_List
        fields = ['list_title', 'list_content', 'status', 'complete',]
        widgets = {
            'list_content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your to-do list here...'}),
        }
    
    list_content = forms.CharField(widget=SummernoteWidget())


class CharacterForm(forms.ModelForm):
    class Meta:
        model = UserCharacter
        fields = ['character_name',]
        widgets = {
            'character_name': forms.TextInput(attrs={'placeholder': 'Enter name here...'})
        }

