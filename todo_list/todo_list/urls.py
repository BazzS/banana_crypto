"""todo_list URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from tasks.views import register, user_login, task_view, \
    task_create, task_update, task_delete, home, user_logout
from bot.handlers import link_account, create_task, get_tasks

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('task/', task_view, name='task_view'),
    path('task/create/', task_create, name='task_create'),
    path('task/update/<int:pk>/', task_update, name='task_update'),
    path('task/delete/<int:pk>/', task_delete, name='task_delete'),
    path('logout/', user_logout, name='logout'),
    path('link-account/', link_account, name='link-account'),
    path('create-task/', create_task, name='create-task'),
    path('get-tasks/', get_tasks, name='get-tasks'),
]
