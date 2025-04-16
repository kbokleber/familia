from django.urls import path
from . import views

app_name = 'finances'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
] 