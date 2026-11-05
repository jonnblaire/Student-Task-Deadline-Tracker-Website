from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from tasks import views
from tasks.views import register_view # <-- Import para sa register

urlpatterns = [
    path('admin/', admin.site.urls),
    
  
    path('login/', auth_views.LoginView.as_view(template_name='tasks/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),

   
    path('', views.dashboard, name='dashboard'),
    path('my-tasks/', views.my_tasks, name='my_tasks'),
    path('calendar/', views.calendar, name='calendar'),
    path('subjects/', views.subjects, name='subjects'),
    path('settings/', views.settings, name='settings'),
    
   
    path('add-task/', views.add_task, name='add_task'),
    path('edit-task/<int:pk>/', views.edit_task, name='edit_task'),
    path('delete-task/<int:pk>/', views.delete_task, name='delete_task'), 
    path('toggle-task/<int:pk>/', views.toggle_task, name='toggle_task'),
    
    
    path('add-subject/', views.add_subject, name='add_subject'),
    path('edit-subject/<int:pk>/', views.edit_subject, name='edit_subject'),
    path('delete-subject/<int:pk>/', views.delete_subject, name='delete_subject'),
]