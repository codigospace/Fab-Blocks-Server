from django.contrib import admin
from .models import Project, Task, UploadedFile

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'owner__username')
    list_filter = ('created_at',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'created_at')
    search_fields = ('title', 'creator__username')
    list_filter = ('created_at',)

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('user', 'task','uploaded_at')
    search_fields = ('user__username', 'task__title')
    list_filter = ('uploaded_at',)
