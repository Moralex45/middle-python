"""config URL Configuration."""
from django.urls import path, include

urlpatterns = [
    path('v1/', include('movies.api.v1.urls')),
    path('v2/', include('movies.api.v2.urls')),
    path('v3/', include('movies.api.v3.urls')),
]
