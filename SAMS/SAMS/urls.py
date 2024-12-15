from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authenticated/', include('core.urls')),
    path('', include('members.urls')),
]
