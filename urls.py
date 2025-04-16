from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls', namespace='core')),  # URLs do app core com namespace explícito
    path('healthcare/', include('healthcare.urls')),  # URLs do app healthcare
    path('finances/', include('finances.urls')),  # URLs do app finances
    path('maintenance/', include('maintenance.urls')),  # URLs do app maintenance
    path('accounts/', include('accounts.urls')),  # URLs do app accounts
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 