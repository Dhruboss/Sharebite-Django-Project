from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Include core URLs at root
    path('users/', include('users.urls')),
    path('food/', include('food.urls')),
    # path('donations/', include('donations.urls')),  # Keep commented for now
    # path('gamification/', include('gamification.urls')),  # Keep commented for now
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)