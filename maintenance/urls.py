from django.urls import path
from .views import (
    CreateOrderView, CreateEquipmentView, DetailOrderView,
    DeleteOrderView, UpdateOrderView, MaintenanceOrderListView,
    MaintenanceDashboardView, EquipmentListView, EquipmentDetailView,
    EquipmentUpdateView, EquipmentDeleteView, DeleteMaintenanceImageView
)

app_name = 'maintenance'

urlpatterns = [
    path('', MaintenanceDashboardView.as_view(), name='dashboard'),
    path('order/create/', CreateOrderView.as_view(), name='order_create'),
    path('order/<int:pk>/', DetailOrderView.as_view(), name='order_detail'),
    path('order/<int:pk>/edit/', UpdateOrderView.as_view(), name='order_update'),
    path('order/<int:pk>/delete/', DeleteOrderView.as_view(), name='order_delete'),
    path('equipment/create/', CreateEquipmentView.as_view(), name='equipment_create'),
    path('equipment/', EquipmentListView.as_view(), name='equipment_list'),
    path('equipment/<int:pk>/', EquipmentDetailView.as_view(), name='equipment_detail'),
    path('equipment/<int:pk>/edit/', EquipmentUpdateView.as_view(), name='equipment_update'),
    path('equipment/<int:pk>/delete/', EquipmentDeleteView.as_view(), name='equipment_delete'),
    path('orders/', MaintenanceOrderListView.as_view(), name='order_list'),
    # As URLs serão adicionadas posteriormente
] 