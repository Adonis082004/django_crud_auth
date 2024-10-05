from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Permission
from django.contrib.auth import login, logout
from django.db import IntegrityError
from django.contrib.auth import authenticate
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task,pk=task_id,user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request,"create_task.html",{'form':TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task=form.save(commit=False)
            new_task.user=request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request,"create_task.html",{
                'form':TaskForm,
                'error':'Ingrese tipos de datos correctos'
                })
@login_required
def delete_task(request, task_id):
    task=get_object_or_404(Task,pk=task_id,user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    
def home(request):
    return render(request,'home.html')
   
def signin(request):
    if request.method == 'GET':
        return render(request,'signin.html',{'form':AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request,'signin.html',{
                'form': AuthenticationForm,
                'error':'Username or password is incorrect'
            })
        else:
            login(request,user)
            return redirect('tasks')

def signout(request):
    logout(request)
    return redirect('home')


def signup(request):
    if request.method =='GET':
        return render(request,'signup.html',
            {'form':UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('tasks')
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {"form":UserCreationForm, "error":"Username already exists"},
                )
        return render(
            request,
                "signup.html",
                {"form":UserCreationForm, "error":"Password do not match"},
         )
        

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request,'tasks.html',{'tasks':tasks,'tipopagina':'Tareas Pendientes'})

@login_required
def tasks_completed(request):
    tasks=Task.objects.filter(user=request.user,datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'tasks.html',{'tasks':tasks,'tipopagina':'Tareas Completadas'})

@login_required
def task_detail(request, task_id):
   if request.method == 'GET':
        task = get_object_or_404(Task,pk=task_id,user=request.user)
        form = TaskForm(instance=task)
        return render(request,'task_detail.html',{
            'task':task,
            'form':form
            })
   else:
       try:
            task = get_object_or_404(Task,pk=task_id,user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
       except ValueError:
            return render(request,'task_detail.html',{
            'task':task,
            'form':form,
            'error':'Error updating tasks'
            })
       
def asignar_permisos_completos(request):
    user = User.objects.get(username='adonisquijije')  # Reemplazar con el nombre real del usuario

    # Lista de los codenames de los permisos que quieres agregar
    permisos = [
        'add_logentry', 'change_logentry', 'delete_logentry', 'view_logentry',
        'add_group', 'change_group', 'delete_group', 'view_group',
        'add_permission', 'change_permission', 'delete_permission', 'view_permission',
        'add_user', 'change_user', 'delete_user', 'view_user',
        'add_contenttype', 'change_contenttype', 'delete_contenttype', 'view_contenttype',
        'add_session', 'change_session', 'delete_session', 'view_session',
        'add_task', 'change_task', 'delete_task', 'view_task'
    ]

    # Filtramos y obtenemos los permisos basados en los codenames
    permisos_objetos = Permission.objects.filter(codename__in=permisos)

    # Agregamos los permisos al usuario
    user.user_permissions.add(*permisos_objetos)

    return render(request, 'tu_template.html', {'mensaje': 'Permisos asignados correctamente'})