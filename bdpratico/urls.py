from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('precatory.urls')),
    path('precatory/', include('precatory.urls')),
    path('admin/', admin.site.urls),
]