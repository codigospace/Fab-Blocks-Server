from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

class Project(models.Model):
    name = models.CharField(max_length=100)
    mac = models.CharField(max_length=100, null=True)
    cpu = models.CharField(max_length=100, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

User = get_user_model()

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='uploaded_files')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File uploaded by {self.user.username} for task {self.task.title}"