from django.urls import path
from .views import project_list, create_project, delete_project, update_project, project_content, examples_list, example_content, create_task, user_task_list, toggle_visibility, public_task_list, delete_task, update_task, project_task_list, receive_task, task_files_view, task_project_content

urlpatterns = [
    path('list/', project_list, name='project_list'),
    path('list/', project_list, name='fabblocks'),
    path('create/', create_project, name='create_project'),
    path('delete/<int:pk>/', delete_project, name='delete_project'),
    path('update/<int:pk>/', update_project, name='update_project'),
    path('projects/<int:project_id>/', project_content, name='project_content'),
    path('examples/', examples_list, name='examples_list'),
    path('examples/<str:folder>/<str:file_name>/', example_content, name='example_content'),
    path('createTask/', create_task, name='create_task'),
    path('public_task_list/', public_task_list, name='task_list_public'),
    path('task_list/', user_task_list, name='task_list_user'),
    path('task_change_visibility/', toggle_visibility, name='change_task_visibility'),
    path('toggle-visibility/<int:task_id>/', toggle_visibility, name='toggle_visibility'),
    path('delete-task/<int:task_id>/', delete_task, name='delete_task'),
    path('update-task/<int:task_id>/', update_task, name='update_task'),
    path('update-task/<int:task_id>/', update_task, name='update_task'),
    path('project-task/', project_task_list, name='project_task_list'),
    path('receive_task/', receive_task, name='receive_task'),
    path('task/<int:task_id>/files/', task_files_view, name='task_files'),
    path('projects_task/<int:task_id>/', task_project_content, name='task_project_content'),

]
