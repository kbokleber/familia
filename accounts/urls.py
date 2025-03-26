from django.urls import path
from .views import RegisterView, ProfileUpdateView, SettingsView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('settings/user/create/', SettingsView.as_view(), {'action': 'create_user'}, name='create_user'),
    path('settings/user/<int:pk>/update/', SettingsView.as_view(), {'action': 'update_user'}, name='update_user'),
    path('settings/user/<int:pk>/delete/', SettingsView.as_view(), {'action': 'delete_user'}, name='delete_user'),
] 