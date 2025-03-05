from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path('', views.task_list, name='task-list'),
    path('create/', views.task_create, name='task-create'),
    path('<int:pk>/edit/', views.task_edit, name='task-edit'),
    path('<int:pk>/delete/', views.task_delete, name='task-delete'),
]
