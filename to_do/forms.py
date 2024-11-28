from django import forms
from .models import To_Do_List


class ToDoListForm(forms.ModelForm):
    class Meta:
        model = To_Do_List
        fields = ['list_title', 'list_content', 'status']
        widgets = {
            'list_content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your to-do list here...'}),
        }


