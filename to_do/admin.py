from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import To_Do_List


@admin.register(To_Do_List)
class ToDoAdmin(SummernoteModelAdmin):
    list_display = ('list_title', 'slug', 'status', 'approved')
    search_fields = ['list_title']
    list_filter = ('status', 'approved', 'created_on',)
    prepopulated_fields = {'slug': ('list_title',)}
    summernote_fields = ('list_content',)

