# SchoolManagement/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('databaseData.urls')),  # Add this line
]
