from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('system/config/', views.system_config_list, name='system_config_list'),
    path('system/config/<int:pk>/edit/', views.system_config_edit, name='system_config_edit'),
    path('system/config/<int:pk>/delete/', views.system_config_delete, name='system_config_delete'),
] 