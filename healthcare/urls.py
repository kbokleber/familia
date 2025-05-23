from django.urls import path
from . import views

app_name = 'healthcare'

urlpatterns = [
    path('', views.healthcare_dashboard, name='dashboard'),
    path('api/procedures-chart-data/', views.procedures_chart_data, name='procedures_chart_data'),
    path('api/chart-data/', views.chart_data, name='chart_data'),
    
    # Family Member URLs
    path('members/', views.family_member_list, name='family_member_list'),
    path('members/<int:pk>/', views.family_member_detail, name='family_member_detail'),
    path('members/create/', views.family_member_create, name='family_member_create'),
    path('members/<int:pk>/edit/', views.family_member_edit, name='family_member_edit'),
    path('members/<int:pk>/delete/', views.family_member_delete, name='family_member_delete'),
    path('members/save-order/', views.save_family_members_order, name='save_family_members_order'),
    
    # Medical Appointment URLs
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/create/', views.appointment_create, name='appointment_create'),
    path('appointments/<int:pk>/edit/', views.appointment_edit, name='appointment_edit'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
    
    # Medical Procedure URLs
    path('procedures/', views.procedure_list, name='procedure_list'),
    path('procedures/create/', views.procedure_create, name='procedure_create'),
    path('procedures/<int:pk>/edit/', views.procedure_edit, name='procedure_edit'),
    path('procedures/<int:pk>/delete/', views.procedure_delete, name='procedure_delete'),
    
    # Medication URLs
    path('medications/', views.medication_list, name='medication_list'),
    path('medications/create/', views.medication_create, name='medication_create'),
    path('medications/<int:pk>/', views.medication_detail, name='medication_detail'),
    path('medications/<int:pk>/edit/', views.medication_edit, name='medication_edit'),
    path('medications/<int:pk>/delete/', views.medication_delete, name='medication_delete'),
] 