from django.contrib import admin
from .models import Subject, Task

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'color', 'user')
    search_fields = ('name', 'code')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'task_type', 'priority', 'status', 'due_date', 'user')
    search_fields = ('title', 'description')