from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from django.http import JsonResponse, HttpResponse
import json
from .models import Project, Task
import shutil
import os
from django.conf import settings

@login_required(login_url="/auth/login/")
def project_list(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'project_list.html', {'projects': projects})

@login_required(login_url="/auth/login/")
def create_project(request):
    if request.method == 'POST':
        project_name = request.POST.get('nombreProyecto','')
        if Project.objects.filter(owner=request.user).count() >= 15:
            error_message = "Ya has alcanzado el límite máximo de proyectos (15). No puedes crear más."
            projects = Project.objects.filter(owner=request.user)
            return render(request, 'project_list.html', {'projects': projects, 'error_message': error_message})
        
        if Project.objects.filter(name=project_name, owner=request.user).exists():
            error_message = f"Ya existe un proyecto con el nombre '{project_name}'. Por favor, elige otro nombre."
            projects = Project.objects.filter(owner=request.user)
            return render(request, 'project_list.html', {'projects': projects, 'error_message': error_message})
        
        new_project = Project.objects.create(name=project_name, owner=request.user)
        project_folder = os.path.join(settings.MEDIA_ROOT,'projects', str(request.user.id), project_name)
        os.makedirs(project_folder)
        fab_file_path = os.path.join(project_folder, f"{project_name}.fab")
        with open(fab_file_path, "w") as fab_file:
            fab_file.write('<xml id="startBlocks" style="display: none"><block type="controls_setupLoop" deletable="false"></block></xml>')
        
        return redirect('project_list')
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required(login_url="/auth/login/")
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    # Verificar si el proyecto pertenece al usuario actual
    if project.owner != request.user:
        return JsonResponse({'error': 'No tienes permiso para eliminar este proyecto.'}, status=403)
    
    # Eliminar la carpeta del proyecto
    project_folder = os.path.join(settings.MEDIA_ROOT, 'projects', str(request.user.id), project.name)
    if os.path.exists(project_folder):
        shutil.rmtree(project_folder)  # Eliminar carpeta y su contenido recursivamente
    
    project.delete()  # Eliminar el proyecto de la base de datos
    
    return JsonResponse({'success': 'Proyecto y carpeta asociada eliminados exitosamente'})

@login_required(login_url="/auth/login/")
def update_project(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_name = data.get('newName')
        if new_name:
            try:
                project = Project.objects.get(pk=pk)

                # Almacenar el nombre anterior del proyecto antes de cambiarlo
                old_project_name = project.name

                old_project_folder = os.path.join(settings.MEDIA_ROOT, 'projects', str(request.user.id), old_project_name)
                new_project_folder = os.path.join(settings.MEDIA_ROOT, 'projects', str(request.user.id), new_name)

                os.rename(old_project_folder, new_project_folder)
                print("luego de rename")
                # Actualizar el nombre del proyecto en la base de datos
                project.name = new_name
                project.save()

                # Renombrar el archivo .fab dentro de la carpeta del proyecto
                old_fab_path = os.path.join(new_project_folder, f"{old_project_name}.fab")
                new_fab_path = os.path.join(new_project_folder, f"{new_name}.fab")
                os.rename(old_fab_path, new_fab_path)

                return JsonResponse({'success': 'Nombre de proyecto y archivo .fab actualizados correctamente'})
            except Project.DoesNotExist:
                return JsonResponse({'error': 'El proyecto no existe'}, status=404)
            except FileNotFoundError:
                return JsonResponse({'error': 'El archivo .fab no pudo ser encontrado o renombrado'}, status=404)
        else:
            return JsonResponse({'error': 'El nuevo nombre del proyecto es requerido'}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required(login_url="/auth/login/")
def project_content(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        if request.user == project.owner:
            fab_file_path = os.path.join(settings.MEDIA_ROOT, 'projects', str(request.user.id), project.name, f"{project.name}.fab")
            with open(fab_file_path, "r") as fab_file:
                fab_content = fab_file.read()
            return render(request, 'project_content.html', {'project': project, 'fab_content': fab_content})
        else:
            return HttpResponse("No tienes permiso para ver este proyecto")
    except Project.DoesNotExist:
        return HttpResponse("El proyecto no existe")

@login_required(login_url="/auth/login/")
def examples_list(request):
    example_folders = ['Arduino', 'Modular', 'Betto','Blass','Carlitto']
    examples = []

    for folder in example_folders:
        folder_path = os.path.join(settings.MEDIA_ROOT, 'examples', folder)
        if os.path.isdir(folder_path):
            example_files = os.listdir(folder_path)
            for file in example_files:
                if file.endswith('.fab'):
                    example_name = os.path.splitext(file)[0]
                    example_url = os.path.join('/media', folder, file)
                    examples.append({'name': example_name, 'url': example_url, 'folder': folder, 'file': file})

    return render(request, 'example_list.html', {'examples': examples})

def example_content(request, folder, file_name):
    try:
        example_folder_path = os.path.join(settings.MEDIA_ROOT, 'examples', folder)
        if not os.path.isdir(example_folder_path):
            return HttpResponse("La carpeta de ejemplos no existe")
        
        example_file_path = os.path.join(example_folder_path, file_name)
        if not os.path.isfile(example_file_path):
            return HttpResponse("El archivo de ejemplo no existe")
        
        with open(example_file_path, "r") as example_file:
            example_content = example_file.read()
        
        return render(request, 'example_content.html', {'folder': folder, 'file_name': file_name, 'example_content': example_content})
    except Exception as e:
        return HttpResponse(f"Error al leer el archivo de ejemplo: {str(e)}")

@login_required(login_url="/auth/login/")
def create_task(request):
    if request.method == 'POST':
        task_name = request.POST.get('task_name', '')
        task_description = request.POST.get('task_description', '')
        
        if task_name:
            new_task = Task.objects.create(title=task_name, description=task_description, creator=request.user)
            user_folder_path = os.path.join(settings.MEDIA_ROOT, 'tasks', str(request.user.id), str(new_task.id))
            os.makedirs(user_folder_path, exist_ok=True)
            
            # Agregar registros de impresión para verificar si se creó la tarea y el archivo
            print("Nueva tarea creada:", new_task.title)
            print("Descripción de la tarea:", new_task.description)
            print("Creada por:", new_task.creator)
            
            return redirect('task_list_user')
        else:
            return HttpResponse("El nombre de la tarea es requerido")
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required(login_url="/auth/login/")
def user_task_list(request):
    tasks = Task.objects.filter(creator=request.user)
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required(login_url="/auth/login/")
def public_task_list(request):
    tasks = Task.objects.filter(visible=True)
    return render(request, 'public_task_list.html', {'tasks': tasks})

@login_required(login_url="/auth/login/")
def toggle_visibility(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.user == task.creator:
        task.visible = not task.visible
        task.save()
        return JsonResponse({'success':True,'visible': task.visible})
    return JsonResponse({'success':False,'error': 'No tienes permiso para cambiar la visibilidad de esta tarea.'}, status=403)

@login_required(login_url="/auth/login/")
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.user == task.creator:
        # Eliminar la carpeta correspondiente a la tarea si existe
        task_folder_path = os.path.join(settings.MEDIA_ROOT, 'tasks', str(task.creator.id), str(task.id))
        if os.path.exists(task_folder_path):
            shutil.rmtree(task_folder_path)
        
        # Eliminar la tarea de la base de datos
        task.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'No tienes permiso para eliminar esta tarea.'}, status=403)

@login_required(login_url="/auth/login/")
def update_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id)
        if request.user == task.creator:
            data = json.loads(request.body)
            new_title = data.get('newTitle')
            new_description = data.get('newDescription')
            if new_title:
                task.title = new_title
                task.description = new_description
                task.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'El nuevo título de la tarea es requerido'}, status=400)
        else:
            return JsonResponse({'success': False, 'error': 'No tienes permiso para actualizar esta tarea.'}, status=403)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def project_task_list(request):
    user = request.user
    projects = Project.objects.filter(owner=user)
    tasks = Task.objects.filter(visible=True)

    return render(request, 'task_send.html', {'projects': projects, 'tasks': tasks})

from .models import UploadedFile

@login_required(login_url="/auth/login/")
def receive_task(request):
    if request.method == 'POST':
        project_id = request.POST.get('project')
        task_id = request.POST.get('task')
        
        try:
            project = Project.objects.get(id=project_id)
            task = Task.objects.get(id=task_id)
            
            # Verificar que el usuario que envía la tarea sea el propietario del proyecto
            if project.owner != request.user:
                return JsonResponse({'error': 'No tienes permiso para enviar esta tarea.'}, status=403)
            
            existing_file = UploadedFile.objects.filter(user=request.user, task=task).first()
            if existing_file:
                existing_file.delete()  # Eliminar el archivo existente
            
            # Crear una nueva instancia de UploadedFile
            uploaded_file_instance = UploadedFile.objects.create(
                user=request.user,
                task=task
            )
            
            # Copiar el archivo .fab del proyecto a la carpeta de la tarea
            project_folder = os.path.join(settings.MEDIA_ROOT, 'projects', str(request.user.id), project.name)
            task_folder = os.path.join(settings.MEDIA_ROOT, 'tasks', str(task.creator.id), str(task.id))
            fab_file_path = os.path.join(project_folder, f"{project.name}.fab")
            task_fab_file_path = os.path.join(task_folder, f"{project.name}.fab")
            
            if os.path.exists(fab_file_path):
                user_name = CustomUser.objects.get(id=request.user.id).username
                shutil.copy(fab_file_path, task_fab_file_path)
                new_fab_file_name = f"{user_name}.fab"
                new_fab_file_path = os.path.join(task_folder, new_fab_file_name)
                if os.path.exists(new_fab_file_path):
                    os.remove(new_fab_file_path)
                
                os.rename(task_fab_file_path, new_fab_file_path)

                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'El archivo .fab del proyecto no fue encontrado'}, status=404)
        except Project.DoesNotExist:
            return JsonResponse({'error': 'El proyecto no existe'}, status=404)
        except Task.DoesNotExist:
            return JsonResponse({'error': 'La tarea no existe'}, status=404)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


@login_required(login_url="/auth/login/")
def task_files_view(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    files = task.uploaded_files.all()
    print(files)  # Verifica si hay archivos asociados a la tarea
    return render(request, 'task_files.html', {'task': task, 'files': files})

@login_required(login_url="/auth/login/")
def task_project_content(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        fab_file_name = UploadedFile.objects.get(task_id=task_id).user

        fab_file_path = os.path.join(settings.MEDIA_ROOT, 'tasks', str(request.user.id), str(task_id), f"{fab_file_name}.fab")
        print(fab_file_path)
        if os.path.exists(fab_file_path):
            with open(fab_file_path, "r") as fab_file:
                fab_content = fab_file.read()            
            return render(request, 'project_content.html', {'project': task, 'fab_content': fab_content})
        else:
            return HttpResponse("El archivo .fab del proyecto no existe")
    except Task.DoesNotExist:
        return HttpResponse("La tarea no existe")

