from django.contrib import admin
from .models import Task



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'deadline', 'status', 'owner')  # Columns to show
    list_filter = ('status', 'priority')  # Filters on the side
    search_fields = ('title', 'description')  # Search bar
    ordering = ['deadline']


